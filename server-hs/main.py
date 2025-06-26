from flask import Flask, request, Response, jsonify
from flask_cors import CORS

# Init Flask
#
app = Flask(__name__)
CORS(app)

# Constants
#
DEFAULT_MODEL = "llama3.2"

# Routes
#

from chat import chat
import queue
import threading

def generate_response(messages, chat):
    def generate():
        q = queue.Queue()

        def callback_fn(chunk: str):
            print("callback_fn", chunk)
            q.put(chunk)

        # Run `chat` in a separate thread so it doesn't block `generate`
        def run_chat():
            chat(messages, callback_fn=callback_fn)
            q.put(None)  # Sentinel to signal completion

        threading.Thread(target=run_chat, daemon=True).start()

        while True:
            chunk = q.get()
            if chunk is None:
                break
            yield f"data: {chunk}\n\n"  # SSE format

    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/chat', methods=['POST'])
def api_chat():

    data = request.json or {}
    messages = data.get("messages", [])
    #model = data.get("model", DEFAULT_MODEL)
    #stream = data.get("stream", True)

    return generate_response(messages, chat)

test = """
curl http://localhost:5070/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2"}'
"""

if __name__ == '__main__':
    app.run(port=5070, debug=True)
