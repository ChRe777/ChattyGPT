import "./ChatInput.css";

// Libs
//
import React, { useState, useRef, useEffect } from "react";

// Store
//
import useChatMessageStore from "stores/chatMessageStore";

// Components
//
import ChatInputFiles from "components/ChatInput/ChatInputFiles";
import ChatInputToolbar from "components/ChatInput/ChatInputToolbar";
import ChatInputText from "components/ChatInput/ChatInputText";

// Actions
//
import { streamChat2 } from "actions/getQuery";
import { queryDocs } from "actions/getDocs";

// Component
//
function ChatInput() {
    // State
    //
    const {
        addUserMessage,
        addAssistantMessage,
        appendToLastMessage,
        messages,
        attachedTexts,
        isAnswering,
        setIsAnswering,
        setFoundDocs,
        setText,
    } = useChatMessageStore();
    const [stopAnswering, setStopAnswering] = useState(false);

    // Functions
    //
    const stopRef = useRef(false); // 🧠 this tracks the real-time value

    // Keep ref in sync with state
    useEffect(() => {
        stopRef.current = stopAnswering;
    }, [stopAnswering]);

    // Always returns the latest value
    const shouldStopFn = () => stopRef.current;

    const attachTextsToMessages = (messages) => {
        if (attachedTexts.length > 0) {
            const context = attachedTexts
                .map(
                    (doc) =>
                        `Filename: ${doc.filename}\nText:\n${doc.text.trim()}`,
                )
                .join("\n\n---\n\n");
            messages.push({
                role: "system",
                content: `You are a helpful assistant. Use the following context:\n\n${context}`,
            });
        }
    };

    const addQueryDocs = async (messages, query) => {
        const documents = await queryDocs(query);
        if (documents.length > 0) {
            setFoundDocs(documents.length);
            const context = documents.join("\n\n");
            messages.push({
                role: "system",
                content: `You are a helpful assistant. Use only the following context:\n\n${context}`,
            });
        } else {
            setFoundDocs(0);
        }
    };

    const addQuery = (messages, query) => {
        messages.push({ role: "user", content: query });
    };

    // Actions
    //
    const doSubmit = async (query) => {
        if (query !== "" && isAnswering === false) {
            setStopAnswering(false); // Reset stop flag
            setText(""); // Reset text

            addUserMessage(query);
            addAssistantMessage("");

            setIsAnswering(true);

            const messages_ = [...messages];
            attachTextsToMessages(messages_);
            await addQueryDocs(messages_, query);
            addQuery(messages_, query);

            await streamChat2(messages_, appendToLastMessage, shouldStopFn);

            setIsAnswering(false);
        }
    };

    const doStop = () => {
        setStopAnswering(true);
        setIsAnswering(false);
    };

    return (
        <div>
            <div className="input-box">
                <ChatInputFiles></ChatInputFiles>
                <ChatInputText onSubmit={doSubmit} />
                <ChatInputToolbar onSubmit={doSubmit} onStop={doStop} />
            </div>
            <center>
                <small>
                    ChattyGPT kann Fehler machen. Überprüfe wichtige
                    Informationen. Siehe Cookie-Voreinstellungen.
                </small>
            </center>
        </div>
    );
}

export default ChatInput;
