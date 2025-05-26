# tts_ws_server.py


import asyncio
import websockets
import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TTSBridgeNode(Node):
    def __init__(self):
        super().__init__('tts_ws_bridge')
        self.publisher_ = self.create_publisher(String, '/tts', 10)

    def publish_tts(self, text):
        msg = String()
        msg.data = text
        self.publisher_.publish(msg)
        self.get_logger().info(f"TTS 발행: {text}")

tts_node = None  # 글로벌 선언

async def ws_handler(websocket, path):
    global tts_node
    async for message in websocket:
        try:
            data = json.loads(message)
            if data.get('type') == 'tts' and 'text' in data:
                tts_node.publish_tts(data['text'])
        except Exception as e:
            print("TTS WebSocket 처리 에러:", e)

async def main():
    global tts_node
    rclpy.init()
    tts_node = TTSBridgeNode()
    # 웹소켓 서버 시작
    ws_server = await websockets.serve(ws_handler, "0.0.0.0", 7777)
    print("✅ TTS WebSocket Server started on port 7777")
    try:
        await asyncio.get_running_loop().run_in_executor(None, rclpy.spin, tts_node)
    finally:
        tts_node.destroy_node()
        rclpy.shutdown()
        ws_server.close()
        await ws_server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())

