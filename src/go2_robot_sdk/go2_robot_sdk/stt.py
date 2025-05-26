import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from unitree_go.msg import WebRtcReq
import socket
import wave
import whisper
import openai
import json
import requests
from datetime import datetime
import difflib
import os
import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ───── 설정 ─────
PORT = 5050
SAVE_PATH = "/tmp/received.wav"
TRIGGER_SERVER_URL = "http://10.8.0.2:9000/destination"  # 꼭 실제 Xavier IP로 변경!
# TRIGGER_SERVER_URL = "http://192.168.0.27:9000/destination" # 꼭 실제 Xavier IP로 변경!
CAMERA_SERVER_HOST = "10.8.0.2"   # 카메라 제어 서버 IP
CAMERA_SERVER_PORT = 8001             # 카메라 제어 포트
POST_TIMEOUT = 10

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ---- 앱 건물 json 기반 건물 정보 로드 ----
curdir = os.path.dirname(os.path.abspath(__file__))
BUILDING_JSON_PATH = "/home/hiwilab/Project/DOG/ros2_ws/src/go2_robot_sdk/go2_robot_sdk/buildingData.json"
try:
    with open(BUILDING_JSON_PATH, "r", encoding="utf-8") as f:
        building_data = json.load(f)
    BUILDING_LIST = [b["name"]["ko"] for b in building_data if b.get("name") and b["name"].get("ko")]
except Exception as e:
    print("[❌ BUILDING_LIST 생성 실패]", e)
    building_data = []
    BUILDING_LIST = []

try:
    with open("stt_correction_map.json", "r", encoding="utf-8") as f:
        stt_correction_map = json.load(f)
except FileNotFoundError:
    stt_correction_map = {}

# 🟢 추가: 임베딩 모델/FAISS 인덱스/문서 불러오기
try:
    embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")
    index = faiss.read_index("rag_index_local.faiss")
    with open("rag_docs_local.json", "r", encoding="utf-8") as f:
        rag_docs = json.load(f)
except Exception as e:
    print("[❌ 임베딩 시스템 로드 실패]", e)
    embedding_model, index, rag_docs = None, None, []

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

# 🟢 추가: 텍스트 임베딩 + FAISS 검색
def get_embedding_local(text):
    return embedding_model.encode(["query: " + text], convert_to_numpy=True)[0]

def retrieve_docs_faiss(query, top_k=7):
    if embedding_model is None or index is None or not rag_docs:
        return []
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

# ───── 건물 전체 정보 추출 함수 ─────
def normalize(text):
    return re.sub(r'\s+', '', text).lower()

def find_building_info_by_ko_name(text):
    norm_text = normalize(text)
    for entry in building_data:
        bname = entry.get("name", {}).get("ko", "")
        if bname and normalize(bname) in norm_text:
            return entry
    return None
    
# ───── 카메라 트리거 전송 (전역 함수) ─────
def send_camera_trigger(logger):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CAMERA_SERVER_HOST, CAMERA_SERVER_PORT))
            s.sendall(b"camera")
        logger.info("📸 카메라 트리거 ‘CAMERA’ 전송 성공")
    except Exception as e:
        logger.warn(f"❌ 카메라 트리거 전송 실패: {e}")

        
# ───── 앱 트리거 전송 함수 (전체 정보 전송) ─────
def send_navigation_trigger_to_app(logger, building_info=None):
    if building_info:
        msg = {
            "id": building_info.get("id", ""),
            "name": building_info.get("name", {}),
            "target": building_info.get("position"),
            "description": building_info.get("description", {}),
            "image": building_info.get("image", ""),
            "trigger": True
        }
    else:
        msg = {"trigger": True}
    try:
        res = requests.post(TRIGGER_SERVER_URL, json=msg, timeout=POST_TIMEOUT)
        if res.status_code == 200:
            logger.info(f"📨 목적지 데이터 전송 성공 (status 200, target={msg.get('target')})")
        else:
            logger.warn(f"❌ 목적지 데이터 전송 실패 (status {res.status_code})")
    except Exception as e:
        logger.warn(f"❌ 목적지 데이터 전송 실패: {e}")
    send_camera_trigger(logger)
    
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
                if audio_data:
                    self.tts_pub.publish(String(data="네"))
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
        building_info = None
        cmd = text.replace(" ", "")
        # 🟢 길안내 트리거 감지 시 buildingData.json에서 전체 정보 추출해서 앱에 전송
        if "길안내" in cmd or "길 안내" in cmd or "가는길" in cmd:
            building_info = find_building_info_by_ko_name(text)
            if building_info:
                send_navigation_trigger_to_app(self.get_logger(), building_info=building_info)
                if building_info.get("name", {}).get("ko"):
                    self.tts_pub.publish(String(data=f"{building_info['name']['ko']}까지 안내를 시작할게요. 저를 따라와 주세요!"))
                else:
                    self.tts_pub.publish(String(data="목적지까지 길 안내를 시작할게요. 저를 따라와 주세요!"))
            else:
                self.tts_pub.publish(String(data="죄송해요, 해당 건물을 찾을 수 없어요. 다시 말씀해주시겠어요?"))
                self.get_logger().warn("❌ 데이터에 없는 건물명 → 안내 미실행")
            return

        # 이하 기존 명령어/대화 응답 등 유지 + ★임베딩 기반 RAG 답변 복구
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

    # 🟢 RAG + 임베딩 기반 답변 복구
    def generate_rag_response(self, raw_text):
        corrected = apply_stt_corrections(raw_text, stt_correction_map)
        weather_info = get_weather_openweather(OPENWEATHER_API_KEY) if is_weather_related(corrected) else None
        # ✅ FAISS+임베딩 검색 반영 (없을 때는 빈 리스트 fallback)
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

