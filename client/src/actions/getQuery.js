// Libs
//
import { getPrompt } from "prompts/prompts";

// Constants
//
const API_GENERATE = 'http://localhost:5050/api/generate';
const API_CHAT = 'http://localhost:5050/api/chat';

// Functions
//
export async function streamAnswer(query, callbackFn, shouldStopFn) {

    const prompt = getPrompt("default", { "query": query })
    // const prompt = getPrompt("compare", { "text1": "foo", "text2": "bar" })

    const response = await fetch(API_GENERATE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // Stream output
    //
    while (true) {
        if (shouldStopFn()) {
            reader.cancel("canceled by user")
            break;
        }

        const { value, done } = await reader.read();
        if (done) {
            break;
        }

        const chunk = decoder.decode(value, { stream: true });
        callbackFn(chunk);
    }

}

export async function streamChat(messages, callbackFn, shouldStopFn) {

    console.log("streamChat");

    // const prompt = getPrompt("default", { "query": query })
    // const prompt = getPrompt("compare", { "text1": "foo", "text2": "bar" })

    const response = await fetch(API_CHAT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(
            {
                messages: messages
            }
        ),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    // Stream output
    //
    while (true) {
        if (shouldStopFn()) {
            reader.cancel("canceled by user")
            break;
        }

        // b'{"model":"llama3.2","created_at":"2025-06-22T21:28:28.742295Z","message":{"role":"assistant","content":"?"},"done":false}'
        // b'{"model":"llama3.2","created_at":"2025-06-22T21:28:28.823326Z","message":{"role":"assistant","content":""},"done_reason":"stop","done":true,"total_duration":3551200583,"load_duration":1090000583,"prompt_eval_count":29,"prompt_eval_duration":1796870042,"eval_count":8,"eval_duration":661512583}'

        const { value, done } = await reader.read();

        console.log("bytes:", value);
        console.log("done:", done);

        if (done) {
            break;
        }
        const data = decoder.decode(value, { stream: true });
        console.log("data:", data)

        // text: – "data: {'model': 'llama3.2', 'created_at': '2025-06-23T08:29:15.789416Z', 'message': {'role': 'assistant', 'content': ''}, 'done_reason'…" (bundle.js, line 24583)
        const text = data.replace("data:", "").trimStart();
        const obj = JSON.parse(text);

        console.log("obj:", obj)
    }

}



// Streaming with fetch and ReadableStream
/*
export async function streamText(url: string, onToken: (token: string) => void) {
    const res = await fetch(url)
    const reader = res.body?.getReader()
    const decoder = new TextDecoder()

    while (true) {
        const { value, done } = await reader!.read()
        if (done) break
        const chunk = decoder.decode(value, { stream: true })
        onToken(chunk)
    }
}
*/

export async function streamChat2(messages, onData, shouldStop) {

    const response = await fetch(API_CHAT, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            messages: messages,
            stream: true
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {

        // User request stop streaming
        //
        const stop = shouldStop();
        console.log("stop", stop);
        if (stop) {
            reader.cancel();
            break;
        }

        const { value, done } = await reader.read();
        if (done) {
            break;
        }

        buffer += decoder.decode(value, { stream: true });

        // Split on newlines (SSE messages are line-based)
        const lines = buffer.split(/\r?\n/);
        buffer = lines.pop(); // Keep partial line

        for (let line of lines) {
            line = line.trim();
            if (!line || !line.startsWith("data:")) continue;

            try {
                const jsonStr = line.slice(5).trim(); // Remove "data:" prefix
                const data = JSON.parse(jsonStr);

                // TODO
                // console.log("data ->", data);

                if (data?.message?.content) {
                    onData(data.message.content);
                }

                if (data.done) {
                    console.log("Streaming complete.");
                    break;
                }

            } catch (err) {
                console.error("JSON parse error:", err, "Line:", line);
            }
        }
    }

    // Optionally handle last partial buffer
    if (buffer.trim().startsWith("data:")) {
        try {
            const jsonStr = buffer.slice(5).trim();
            const data = JSON.parse(jsonStr);

            //console.log("data -> ", data);
            if (data?.message?.content) {
                onData(data.message.content);
            }

        } catch (err) {
            console.warn("Final chunk parse error:", err);
        }
    }
}
