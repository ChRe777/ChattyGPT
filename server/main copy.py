from flask import Flask, request, Response, jsonify
from flask_cors import CORS

import requests
import json

from tool import is_valid_json, call_tool
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

    def get_last_user_input(messages):
        for message in reversed(messages):
            if message["role"] == "user":
                return message["content"]
        return None  # Falls keine user-Nachricht vorhanden ist

    def needs_tool_response(user_input: str) -> bool:
        keywords = ["Wetter", "heute", "aktuell", "jetzt", "suchen", "im Internet", "News", "Temperatur"]
        user_input_lower = user_input.lower()
        return any(keyword.lower() in user_input_lower for keyword in keywords)

    user_input = get_last_user_input(messages)

    print("user_input", user_input)

    if user_input and needs_tool_response(user_input):
        messages = [TOOL_CALL_PROMPT] + messages
    else:
        # Normale Konversation ohne Tool-Prompt
        messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent."}] + messages

    print(messages)

    def generate2():
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }

        #print("messages:", messages)

        # For tool call detection
        json_buffer = ''
        collecting_tool_call = False

        with requests.post(OLLAMA_BASEURL+"/api/chat", json=payload, stream=True) as r:
            for line in r.iter_lines():

                # print("")
                # print("line:", line)

                # b'{"model":"llama3.2","created_at":"2025-06-22T21:28:28.742295Z","message":{"role":"assistant","content":"?"},"done":false}'
                # b'{"model":"llama3.2","created_at":"2025-06-22T21:28:28.823326Z","message":{"role":"assistant","content":""},"done_reason":"stop","done":true,"total_duration":3551200583,"load_duration":1090000583,"prompt_eval_count":29,"prompt_eval_duration":1796870042,"eval_count":8,"eval_duration":661512583}'

                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))

                        message_part = data.get("message", {}).get("content", "")
                        if message_part.strip().startswith("{"):
                            collecting_tool_call = True
                            json_buffer += message_part
                        elif collecting_tool_call:
                            json_buffer += message_part
                        else:
                            str = json.dumps(data)
                            yield f"data: {str}\n\n"

                        if collecting_tool_call and is_valid_json(json_buffer):
                            call_info = json.loads(json_buffer)
                            result = call_tool(call_info)

                            print("TOOL CALL:", result) # {'tool': 'get_weather', 'parameters': {'location': 'Berlin'}}

                            # Gib Tool-Output ans LLM zurück
                            tool_response = {
                                "role": "tool",
                                "name": call_info["tool"],
                                "content": result
                            }

                            # Neues Prompt erstellen
                            followup_payload = {
                                "model": model,
                                "messages": messages + [{"role": "assistant", "content": json_buffer}, tool_response],
                                "stream": stream
                            }


                            # Neues Gespräch mit Antwort vom Tool
                            with requests.post(OLLAMA_BASEURL+"/api/chat", json=followup_payload, stream=True) as request2:
                                for line2 in request2.iter_lines():
                                    print("line2", line2)
                                    if line2:
                                        try:
                                            d2 = json.loads(line2.decode('utf-8'))
                                            yield f"data: {json.dumps(d2)}\n\n"
                                        except:
                                            continue
                            break  # Beende ersten Stream

                    except Exception as e:
                        print("Fehler beim Parsen:", e)

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

                        # Folge-Konversation mit Tool-Antwort
                        followup_payload = {
                            "model": model,
                            "messages": messages,
                            "stream": True
                        }
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
