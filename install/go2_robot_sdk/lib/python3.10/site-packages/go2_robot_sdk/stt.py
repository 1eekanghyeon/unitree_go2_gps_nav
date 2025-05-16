import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from unitree_go.msg import WebRtcReq
import socket
import wave
import whisper
import openai
import json
import faiss
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
from datetime import datetime
import difflib

# ───── 설정 ─────
PORT = 5050
SAVE_PATH = "/tmp/received.wav"

client = openai.OpenAI(api_key="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")
embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")
index = faiss.read_index("rag_index_local.faiss")
with open("rag_docs_local.json", "r", encoding="utf-8") as f:
    rag_docs = json.load(f)

try:
    with open("stt_correction_map.json", "r", encoding="utf-8") as f:
        stt_correction_map = json.load(f)
except FileNotFoundError:
    stt_correction_map = {}

OPENWEATHER_API_KEY = "a5b9e7179ee7c8c5169549d8add05a8b"

# ───── 유틸 함수 ─────
def apply_stt_corrections(text, correction_map, similarity_threshold=0.8):
    words = text.split()
    corrected = []
    for word in words:
        if word in correction_map:
            corrected.append(correction_map[word])
        else:
            match = difflib.get_close_matches(word, correction_map.keys(), n=1, cutoff=similarity_threshold)
            corrected.append(correction_map[match[0]] if match else word)
    return " ".join(corrected)

def get_embedding_local(text):
    return embedding_model.encode(["query: " + text], convert_to_numpy=True)[0]

def retrieve_docs_faiss(query, top_k=7):
    q_emb = get_embedding_local(query).reshape(1, -1).astype(np.float32)
    D, I = index.search(q_emb, top_k)
    return [rag_docs[i] for i in I[0]]

def is_weather_related(text):
    keywords = ["날씨", "기온", "비", "우산", "더워", "추워", "습도", "눈", "바람"]
    return any(k in text for k in keywords)

def get_weather_openweather(api_key, lat=34.7766, lon=127.7009):
    url = "https://api.openweathermap.org/data/2.5/weather"
    res = requests.get(url, params={
        "lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "kr"
    })
    if res.status_code != 200:
        print("[OpenWeather 오류]", res.status_code)
        return None

    data = res.json()
    temp = data["main"]["temp"]
    hum = data["main"]["humidity"]
    desc = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    return f"현재 기온은 {round(temp)}도, 습도는 {hum}%, 하늘 상태는 '{desc}', 바람은 초속 {wind}미터입니다."

def ask_gpt_with_rag(query, context_docs, weather_info=None):
    context_str = "\n\n".join(context_docs)
    weather_context = f"""You have received the following up-to-date weather information from a trusted external source. Use it to answer the user's question naturally and conversationally.

[Weather Info]
{weather_info}

""" if weather_info else ""

    prompt = f"""{weather_context}You are an AI assistant named "Jarvis".

You specialize in university information but can also answer casual questions like weather, greetings, and general facts.

Respond clearly, naturally, and conversationally in Korean.

When answering, always use complete and coherent sentences that sound smooth when read aloud. Avoid special characters, emojis, or awkward punctuation.

Write numbers in words when appropriate. Prefer clarity over formality.

If the question is general (e.g., "What is the department about?"), keep your answer under 100 tokens—two or three sentences max.

If the question involves multiple people, names, or research areas (e.g., "Which professors are in this department?"), you may extend up to 180 tokens—but still prioritize brevity and clarity.

Avoid overexplaining or offering unnecessary suggestions. Do not exceed 200 tokens total.

[Context]
{context_str}

[Question]
{query}

[Answer in Korean]:
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# ───── ROS2 노드 ─────
class WhisperGPTNode(Node):
    def __init__(self):
        super().__init__('whisper_gpt_node')
        self.tts_pub = self.create_publisher(String, '/tts', 10)
        self.motion_pub = self.create_publisher(WebRtcReq, '/webrtc_req', 10)

        self.get_logger().info("🧠 WhisperGPTNode 시작됨 (포트 5050 대기 중)")
        self.model = whisper.load_model("large")
        self.start_socket_server()

    def start_socket_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", PORT))
        server.listen(1)

        def listen():
            while rclpy.ok():
                conn, addr = server.accept()
                self.get_logger().info(f"📡 연결됨: {addr}")
                self.tts_pub.publish(String(data="[SFX_BEEP]"))

                audio_data = b""
                conn.settimeout(1.0)
                try:
                    while True:
                        try:
                            chunk = conn.recv(1024)
                            if not chunk:
                                break
                            audio_data += chunk
                        except socket.timeout:
                            break
                finally:
                    conn.close()
                if audio_data:  # 수신된 오디오가 있을 때만 "Okay" 전송
                    confirmation_tts_message = "Okay"  # "네" 또는 "알겠습니다" 등으로 변경 가능
                    self.tts_pub.publish(String(data=confirmation_tts_message))
                self.save_audio(audio_data)
                text = self.transcribe_audio()
                self.get_logger().info(f"📝 인식 결과: {text}")
                if text:
                    self.send_command_or_gpt(text)
                else:
                    self.get_logger().warn("⚠️ 인식된 텍스트 없음")
                    self.tts_pub.publish(String(data="다시 말씀해주시겠어요?"))

        import threading
        threading.Thread(target=listen, daemon=True).start()

    def save_audio(self, data):
        with wave.open(SAVE_PATH, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(data)

    def transcribe_audio(self):
        result = self.model.transcribe(SAVE_PATH, language="ko")
        return result["text"].strip()

    def send_command_or_gpt(self, text):
        cmd = text.replace(" ", "")
        if "앉아" in cmd:
            self.send_motion_command(api_id=1009)
        elif "엎드려" in cmd:
            self.send_motion_command(api_id=1005)
        elif "일어서" in cmd:
            self.send_motion_command(api_id=1006)
        elif "손" in cmd:
            self.send_motion_command(api_id=1016)
        elif "하트" in cmd:
            self.send_motion_command(api_id=1036)
        elif "춤" in cmd:
            self.send_motion_command(api_id=1023)
        elif "점프" in cmd:
            self.send_motion_command(api_id=1031)
        else:
            reply = self.generate_rag_response(text)
            self.get_logger().info(f"🗣 GPT 응답: {reply}")
            self.tts_pub.publish(String(data=reply))

    def send_motion_command(self, api_id, parameter="{}", topic='rt/api/sport/request'):
        msg = WebRtcReq()
        msg.id = 0
        msg.topic = topic
        msg.api_id = api_id
        msg.parameter = parameter
        msg.priority = 0
        self.motion_pub.publish(msg)

    def generate_rag_response(self, raw_text):
        corrected = apply_stt_corrections(raw_text, stt_correction_map)
        weather_info = get_weather_openweather(OPENWEATHER_API_KEY) if is_weather_related(corrected) else None
        top_docs = retrieve_docs_faiss(corrected, top_k=5)
        return ask_gpt_with_rag(corrected, [f"passage: {doc['text']}" for doc in top_docs], weather_info)

def main(args=None):
    rclpy.init(args=args)
    node = WhisperGPTNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("🛑 종료됨.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
