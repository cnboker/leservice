import os
import google.generativeai as genai
import asyncio
from flask import Flask, request, jsonify

os.environ["GOOGLE_API_KEY"] = "AIzaSyCKf7OmRz8qRZPB_q5VG-iGaVnh3OKOuqc"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

# 假设我们要调用Google Gemini LLMs或类似服务的API
@app.route("/chat", methods=["POST"])
async def chat_with_Gemin():
    data = request.get_json()
    input_text = data.get("input_text", "")
    text = ""
    timeout = 15
    if not input_text:
        return jsonify({"error", "No input text provided"})
    try:
        response = await asyncio.wait_for(
            model.generate_content_async(input_text),
            timeout=timeout,
        )
        text = response.text.replace("*", "")
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    except asyncio.exceptions.TimeoutError:
        pass
    except ValueError:
        text = "这个问题我无法回复"
    return jsonify({"response_text": text})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)