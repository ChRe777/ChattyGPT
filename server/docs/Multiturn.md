# 🧠 How Multi-Turn Works (e.g. in Ollama or OpenAI Chat API)

**Multi-turn** conversation means the model maintains **context across multiple messages**, simulating a back-and-forth dialogue.

This is done by sending a **history of messages** (with roles) to the API.

---

## ✅ Structure: `messages` Array

Each message has:

* `role`: `"system"`, `"user"`, or `"assistant"`
* `content`: the actual message text

---

### 🗂️ Example: Multi-Turn Chat API Request (Ollama / OpenAI-style)

```json
POST /api/chat
Content-Type: application/json

{
  "model": "llama3",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Who was the first president of the USA?" },
    { "role": "assistant", "content": "George Washington." },
    { "role": "user", "content": "What year was he born?" }
  ],
  "stream": false
}
```

> 🔁 The model uses all previous messages to generate a response to the **last user message**.

---

## 🧠 How Context Is Maintained

* Each time you call `/api/chat`, you include the **entire conversation history**.
* The model doesn't have memory — **you provide the memory manually**.
* This lets it “remember” what was said and respond appropriately.

---

## ⚠️ Important Tips

* ✂️ Keep the message history concise — too many messages may hit context limits.
* 🧹 Optionally summarize older messages to save space.
* 🧱 Use `system` prompts to define assistant behavior ("You are a math tutor…").

---

## 🧪 Example in JavaScript

```js
const messages = [
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: 'Tell me a joke.' },
  { role: 'assistant', content: 'Why did the chicken cross the road?' },
  { role: 'user', content: 'I don’t know, why?' }
];

fetch('http://localhost:11434/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ model: 'llama3', messages, stream: false })
})
  .then(res => res.json())
  .then(data => console.log(data.message.content));
```

---

Would you like help building a front-end component to manage multi-turn chat?
