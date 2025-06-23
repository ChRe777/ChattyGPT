from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

OLLAMA_BASEURL = "http://localhost:11434/"
MODEL = "llama3.2"

@app.route('/api/generate', methods=['POST'])
def generate():

    user_prompt = request.json.get("prompt", "")
    model = request.json.get("model", MODEL)
    stream = request.json.get("stream", True)

    def generate():
        payload = {
            "model": model,
            "prompt": user_prompt,
            "stream": stream
        }

        with requests.post(OLLAMA_BASEURL+"/api/generate", json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        token = data.get("response", "")
                        yield f"{token}"
                    except Exception as e:
                        print("Fehler beim Parsen:", e)

    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/chat', methods=['POST'])
def chat():

    messages = request.json.get("messages", [])
    model = request.json.get("model", MODEL)
    stream = request.json.get("stream", True)

    def generate():
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }

        with requests.post(OLLAMA_BASEURL+"/api/chat", json=payload, stream=True) as r:
            for line in r.iter_lines():
                print("")
                print("line:", line)
                # b'{"model":"llama3.2","created_at":"2025-06-22T21:28:28.742295Z","message":{"role":"assistant","content":"?"},"done":false}'
                # b'{"model":"llama3.2","created_at":"2025-06-22T21:28:28.823326Z","message":{"role":"assistant","content":""},"done_reason":"stop","done":true,"total_duration":3551200583,"load_duration":1090000583,"prompt_eval_count":29,"prompt_eval_duration":1796870042,"eval_count":8,"eval_duration":661512583}'

                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        str = json.dumps(data)
                        yield f"data: {str}\n\n"
                    except Exception as e:
                        print("Fehler beim Parsen:", e)

    return Response(generate(), mimetype='text/event-stream')

example = """
{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.2753Z",
   "message":{
      "role":"assistant",
      "content":" How"
   },
   "done":false
}

{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.309157Z",
   "message":{
      "role":"assistant",
      "content":" can"
   },
   "done":false
}

{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.345553Z",
   "message":{
      "role":"assistant",
      "content":" I"
   },
   "done":false
}

{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.384337Z",
   "message":{
      "role":"assistant",
      "content":" assist"
   },
   "done":false
}

{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.428658Z",
   "message":{
      "role":"assistant",
      "content":" you"
   },
   "done":false
}

{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.479856Z",
   "message":{
      "role":"assistant",
      "content":" today"
   },
   "done":false
}

{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.545697Z",
   "message":{
      "role":"assistant",
      "content":"?"
   },
   "done":false
}

{
   "model":"llama3.2",
   "created_at":"2025-06-22T21:21:59.673128Z",
   "message":{
      "role":"assistant",
      "content":""
   },
   "done_reason":"stop",
   "done":true,
   "total_duration":958319333,
   "load_duration":35102500,
   "prompt_eval_count":29,
   "prompt_eval_duration":516852292,
   "eval_count":8,
   "eval_duration":398079708
}

curl http://localhost:5050/api/chat2 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role":"user","content":"Hi!"},
      {"role":"assistant","content":"Hello!"}
    ],
    "stream": false
  }'

  -->

  {
    "created_at": "2025-06-23T11:34:43.772891Z",
    "done": true,
    "done_reason": "stop",
    "eval_count": 8,
    "eval_duration": 511952125,
    "load_duration": 32924667,
    "message": {
      "content": " How can I assist you today?",
      "role": "assistant"
    },
    "model": "llama3.2",
    "prompt_eval_count": 29,
    "prompt_eval_duration": 691856250,
    "total_duration": 1238660667
  }

curl http://localhost:5050/api/chat2 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role":"user","content":"Hi!"},
      {"role":"assistant","content":"Hello!"}
    ],
    "stream": true
  }'

-->

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:15.681288Z", "message": {"role": "assistant", "content": " How"}, "done": false}

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:15.689043Z", "message": {"role": "assistant", "content": " can"}, "done": false}

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:15.731235Z", "message": {"role": "assistant", "content": " I"}, "done": false}

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:15.781609Z", "message": {"role": "assistant", "content": " assist"}, "done": false}

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:15.839559Z", "message": {"role": "assistant", "content": " you"}, "done": false}

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:15.915675Z", "message": {"role": "assistant", "content": " today"}, "done": false}

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:16.03975Z", "message": {"role": "assistant", "content": "?"}, "done": false}

data: {"model": "llama3.2", "created_at": "2025-06-23T11:43:16.166643Z", "message": {"role": "assistant", "content": ""}, "done_reason": "stop", "done": true, "total_duration": 4457747667, "load_duration": 1078256958, "prompt_eval_count": 29, "prompt_eval_duration": 2834613500, "eval_count": 8, "eval_duration": 538990041}

"""




@app.route('/api/chat2', methods=['POST'])
def chat2():
    messages = request.json.get("messages", [])
    model = request.json.get("model", MODEL)
    stream = request.json.get("stream", True)

    payload = {
        "model": model,
        "messages": messages,
        "stream": stream  # Pass this to OLLAMA as-is
    }

    if stream:
        # --- Streamed response using SSE ---
        def generate():
            with requests.post(OLLAMA_BASEURL + "/api/chat", json=payload, stream=True) as r:
                if r.status_code != 200:
                    yield f"data: {{\"error\": \"Upstream error {r.status_code}\"}}\n\n"
                    return

                for line in r.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            json_str = json.dumps(data)
                            yield f"data: {json_str}\n\n"
                        except Exception as e:
                            print("Fehler beim Parsen:", e)
                            yield f"data: {{\"error\": \"Parse error: {str(e)}\"}}\n\n"

        return Response(generate(), mimetype='text/event-stream', headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Content-Type': 'text/event-stream',
            'Connection': 'keep-alive',
        })

    else:
        # --- Non-streamed response: wait for full result ---
        r = requests.post(OLLAMA_BASEURL + "/api/chat", json=payload)
        if r.status_code != 200:
            return jsonify({"error": f"Upstream error {r.status_code}"}), r.status_code

        try:
            return jsonify(r.json())
        except Exception as e:
            print("JSON parse error:", e)
            return jsonify({"error": "Failed to parse OLLAMA response"}), 500


if __name__ == '__main__':
    app.run(port=5050, debug=True)
