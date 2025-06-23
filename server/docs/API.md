# Ollama API

Here are the **main HTTP API endpoints** that Ollama serves at `http://localhost:11434`:

---

## 🧠 1. Text Generation / Completions

* \*\*Generate a completion\*\*
  **`POST /api/generate`**
  Single-turn text generation with streaming enabled by default. Supports parameters like `model`, `prompt`, `options` (temperature, top\_p…), `suffix`, `stream`, `format`, `images`, `keep_alive`, etc. ([ollama.readthedocs.io][1])

* \*\*Chat-completion (multi-turn)\*\*
  **`POST /api/chat`**
  Multi-message conversation with roles (`system`, `user`, `assistant`), streaming response. ([deepwiki.com][2], [deepwiki.com][3])

---

## 🧩 2. Embeddings

* **Batch embeddings**
  **`POST /api/embed`**
  Returns embeddings for multiple inputs. ([deepwiki.com][2])

* \*\*Single embedding (legacy alias)\*\*
  **`POST /api/embeddings`**
  Similar to above, but for a single input request. ([deepwiki.com][2])

---

## 📦 3. Model Management

* **Create a model**
  **`POST /api/create`**
  Create or quantize a model using a Modelfile or path; streams status updates. ([ollama.readthedocs.io][1], [ollama.icu][4])

* **Pull a model**
  **`POST /api/pull`**
  Download a model from Ollama registry. ([deepwiki.com][5], [ollama.icu][4])

* **Delete a model**
  **`DELETE /api/delete`**
  Remove a local model. ([ollama.icu][4], [github.com][6])

* **Copy a model**
  **`POST /api/copy`**
  Duplicate a model locally. ([ollama.readthedocs.io][1], [notes.kodekloud.com][7], [docs.openwebui.com][8])

* \*\*Show model info\*\*
  **`GET /api/show`**
  Retrieve metadata about a specific model. ([ollama.readthedocs.io][1], [notes.kodekloud.com][7])

* \*\*List local models\*\*
  **`GET /api/tags`**
  Returns a list of all locally available models. ([ollama.readthedocs.io][1], [github.com][6])

---

## 🧪 4. System & Utility

* **List running model processes**
  **`GET /api/ps`**
  Debug tool showing currently loaded/in-memory models. ([deepwiki.com][5], [notes.kodekloud.com][7])

* **Version info**
  **`GET /api/version`**
  Returns Ollama’s server version details. ([deepwiki.com][2], [ollama.readthedocs.io][1])

* **Health check**
  **`GET /api/health`**
  Endpoint to verify service is up (some docs reference this). ([ollama.zone][9], [reddit.com][10])

---

## ⚡ 5. OpenAI-compatible `/v1` endpoints

Ollama supports the OpenAI-compatible API surface via:

* `POST /v1/completions`
* `POST /v1/chat/completions`
* `GET /v1/models`

These use the same underlying functionality, letting you use OpenAI clients with `api_base = "http://localhost:11434"`. ([reddit.com][11], [mirror.osredm.com][12])

---

## 🔄 Example REST Calls

* **Generate completion** (single-turn, non-streaming):

```bash
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "prompt": "Compose a poem",
    "stream": false
  }'
```

([notes.kodekloud.com][7])

* **Chat completion**:

```bash
curl http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role":"user","content":"Hi!"},
      {"role":"assistant","content":"Hello!"}
    ],
    "stream": false
  }'
```

curl http://localhost:5050/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role":"user","content":"Hi!"},
      {"role":"assistant","content":"Hello!"}
    ]
  }'

---

### ✅ Summary

Ollama’s HTTP API is rich and versatile, supporting:

* 🧠 **Generations** (`/generate`, `/chat`)
* 📦 **Embeddings** (`/embed`, `/embeddings`)
* 🔧 **Model management** (`/create`, `/pull`, `/delete`, `/copy`, `/show`, `/tags`, `/ps`)
* 🧩 **System info** (`/version`, `/health`)
* 🔄 **OpenAI-compatible** endpoints under `/v1/*`

Let me know if you'd like example code (JavaScript, Python, etc.) or help integrating any of these into your app 😄

[1]: https://ollama.readthedocs.io/en/api/?utm_source=chatgpt.com "API Reference - Ollama English Documentation"
[2]: https://deepwiki.com/ollama/ollama/3-api-reference?utm_source=chatgpt.com "API Reference | ollama/ollama | DeepWiki"
[3]: https://deepwiki.com/ollama/ollama/3.2-generation-and-chat-api?utm_source=chatgpt.com "Generation and Chat API | ollama/ollama | DeepWiki"
[4]: https://ollama.icu/api/?utm_source=chatgpt.com "API - Ollama"
[5]: https://deepwiki.com/ollama/ollama-python/3-api-reference?utm_source=chatgpt.com "API Reference | ollama/ollama-python | DeepWiki"
[6]: https://github.com/LewisBroadhurst/ollama.ai/blob/main/docs/api.md?utm_source=chatgpt.com "ollama.ai/docs/api.md at main · LewisBroadhurst/ollama.ai · GitHub"
[7]: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Building-AI-Applications/Demo-Using-Ollama-API-and-Interacting-With-It?utm_source=chatgpt.com "Demo Using Ollama API and Interacting With It - KodeKloud Notes"
[8]: https://docs.openwebui.com/getting-started/api-endpoints/?utm_source=chatgpt.com "🔗 API Endpoints | Open WebUI"
[9]: https://ollama.zone/using-and-consuming-ollama-server-api/?utm_source=chatgpt.com "Ollama.zone - Using and Consuming Ollama Server API"
[10]: https://www.reddit.com/r/ollama/comments/1cocn3a?utm_source=chatgpt.com "Unable to access Ollama API on AWS EC2 instance from local computer despite allowing inbound traffic"
[11]: https://www.reddit.com/r/LocalLLaMA/comments/1du4ddy?utm_source=chatgpt.com "Ollama adds /v1/models and /v1/completions OpenAI compatible APIs"
[12]: https://mirror.osredm.com/root/ollama/src/branch/main/docs/api.md?utm_source=chatgpt.com "ollama/api.md at main - ollama - Gitea: Git with a cup of tea"
