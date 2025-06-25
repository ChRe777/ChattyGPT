from flask import Flask, request, Response, jsonify
from flask_cors import CORS

import requests
import json

from tool import is_valid_json, call_tool, need_tool_call_prompt
from tool import TOOL_CALL_PROMPT

# Init Flask
#
app = Flask(__name__)
CORS(app)

# Constants
#
OLLAMA_BASEURL = "http://localhost:11434/"
MODEL = "llama3.2"

## -CHAT--------------------------------------------------------------------------

@app.route('/api/generate', methods=['POST'])
def api_generate():

    data = request.json or {}
    user_prompt = data.get("prompt", "")
    model = data.get("model", MODEL)
    stream = data.get("stream", True)

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
def api_chat():

    data = request.json or {}
    messages = data.get("messages", [])
    model = data.get("model", MODEL)
    stream = data.get("stream", True)

    # Inject tool call prompt
    #
    if need_tool_call_prompt(messages):
        messages.insert(0, {"role":"system","content": TOOL_CALL_PROMPT})

    def generate(messages):
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }

        json_buffer = ''
        collecting_tool_call = False

        with requests.post(OLLAMA_BASEURL + "/api/chat", json=payload, stream=True) as r:
            for line in r.iter_lines():
                if not line:
                    continue

                try:
                    data = json.loads(line.decode("utf-8"))
                    content = data.get("message", {}).get("content", "")

                    if content.strip().startswith("{"):
                        collecting_tool_call = True
                        json_buffer += content
                    elif collecting_tool_call:
                        json_buffer += content
                    else:
                        yield f"data: {json.dumps(data)}\n\n"

                    if collecting_tool_call and is_valid_json(json_buffer):

                        call_info = json.loads(json_buffer)

                        print("call_info", call_info)

                        result = call_tool(call_info)

                        # Statt role: "tool", sende die Antwort als user-Nachricht:
                        messages += [
                            { "role": "assistant", "content": json.dumps(call_info) },
                            { "role": "user", "content": f"Toolantwort: {result}. Bitte antworte dem Nutzer entsprechend." }
                        ]

                        #tool_response = {
                        #    "role": "tool",
                        #    "name": call_info["name"],
                        #    "content": result
                        #}

                        # Folge-Konversation mit Tool-Antwort
                        followup_payload = {
                            "model": model,
                            "messages": messages,
                            #"messages": messages + [
                            #    {"role": "assistant", "content": json_buffer},
                            #    tool_response,
                            #],
                            "stream": True
                        }

                        print(followup_payload)

                        with requests.post(OLLAMA_BASEURL + "/api/chat", json=followup_payload, stream=True) as r2:
                            for line2 in r2.iter_lines():
                                if line2:
                                    try:
                                        d2 = json.loads(line2.decode("utf-8"))
                                        yield f"data: {json.dumps(d2)}\n\n"
                                    except Exception as e:
                                        print("Fehler in follow-up JSON:", e)

                        break  # Ursprünglichen Stream beenden

                except Exception as e:
                    print("Fehler beim Parsen:", e)

    return Response(generate(messages), mimetype='text/event-stream')

## -DOCS--------------------------------------------------------------------------

import chromadb

# Constants
#
COLLECTION_NAME = "docs"
CHROMA_PATH = "./chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

"""
curl http://localhost:5050/api/docs \
  -H "Content-Type: application/json" \
  -d '{
    "embeddings": [],
    "documents": [],
    "ids": []
  }'
"""
@app.route('/api/docs', methods=['POST'])
def api_docs():

    data = request.json or {}
    embeddings = data.get("embeddings", [])
    documents = data.get("documents", [])
    ids = data.get("ids", [])

    collection.add(documents=documents, ids=ids, embeddings=embeddings)

    return jsonify({"message": "docs added"}), 200

from search import getDocs

"""
curl http://localhost:5050/api/docs/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How much weight can a llama carry relative to its body weight?"
  }'
"""

@app.route('/api/docs/query', methods=['POST'])
def api_docs_query():
    data = request.json or {}
    query = data.get("query", [])

    results = getDocs(query)

    return jsonify(results), 200


if __name__ == '__main__':
    app.run(port=5050, debug=True)
