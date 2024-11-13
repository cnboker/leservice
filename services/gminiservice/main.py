import os
import google.generativeai as genai
import asyncio
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

os.environ["GOOGLE_API_KEY"] = "AIzaSyCKf7OmRz8qRZPB_q5VG-iGaVnh3OKOuqc"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-pro")
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=5)
tasks = {}
loop = asyncio.get_event_loop()

async def fetch_gemini_response(input_text, task_id):
    timeout = 15
    response_text = ""
    try:
        print('begin call gemini...')
        # Instead of asyncio.run, we use the event loop to directly await the result
        response = await asyncio.wait_for(
            model.generate_content_async(input_text), timeout=timeout
        )
        response_text = response.text.replace("*", "")
        tasks[task_id] = {"status": "complete", "payload": response_text}
    except RuntimeError as e:
        print(f"runtimeerror:{e}")
    except asyncio.exceptions.TimeoutError:
        print("it's timeout")
    except ValueError:
        response_text = "这个问题我无法回复"

 

def call_gemini_service(input_text, task_id):  
    loop.run_until_complete(fetch_gemini_response(input_text,task_id))


@app.route("/start_chat", methods=["POST"])
def start_chat():
    task_id = str(len(tasks) + 1)
    tasks[task_id] = {"status": "start"}
    input_text = request.get_json().get("input_text", "")   
    print("input_text->", input_text)
    executor.submit(call_gemini_service, input_text, task_id)
    return jsonify({"task_id": task_id})


# 假设我们要调用Google Gemini LLMs或类似服务的API
@app.route("/chat/<task_id>", methods=["GET"])
def get_chat_response(task_id):
    task = tasks.get(task_id, {"status":"task not found"})
    print("response->", task)
    return jsonify(task)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
