from datetime import datetime
from flask import Flask
from flask_socketio import SocketIO, emit
import numpy as np
import torch
import time
from segmentParser import synthese
import eventlet
# Initialize Flask and SocketIO
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app, cors_allowed_origins="*")
# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


def print_time():
    # 获取当前时间
    current_time = datetime.now()

    # 格式化时间到毫秒
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S') + f'.{current_time.microsecond // 1000:03d}'

    print(formatted_time)


# WebSocket endpoint for TTS live streaming
@socketio.on("start_tts")
def start_tts(data):
    def response(bytes):
        print_time()
        emit("audio_chunk", bytes,)
        eventlet.sleep(0.2)  # 确保发送是非阻塞的,这行非常关键，否则消息堵塞，等全部完成客户端才接收

    text = data.get('text', '')
    synthese(text, response)


@socketio.on("connect")
def on_connect():
    print("Client connected")


@socketio.on("disconnect")
def on_disconnect():
    print("Client disconnected")


# Start the Flask-SocketIO app
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
