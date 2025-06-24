import './ChatInput.css';

// Libs
//
import React, { useState, useRef, useEffect } from 'react';

// Store
//
import useChatMessageStore from 'stores/chatMessageStore';

// Components
//
import ChatInputFiles from 'components/ChatInput/ChatInputFiles';
import ChatInputToolbar from 'components/ChatInput/ChatInputToolbar';
import ChatInputText from 'components/ChatInput/ChatInputText';

// Actions
//
import { streamChat2 } from 'actions/getAnswer';
import { queryDocs } from 'actions/getDocs';

// Component
//
function ChatInput() {

    // State
    //
    const { addUserMessage, addAssistantMessage, appendToLastMessage, messages, texts, isAnswering, setIsAnswering, setText } = useChatMessageStore();
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

    // Actions
    //
    const doSubmit = async (query) => {
        if (query !== '' && isAnswering === false) {

            setStopAnswering(false); // Reset stop flag
            setText('');             // Reset text

            addUserMessage(query);
            addAssistantMessage('');

            setIsAnswering(true);

            const messages_ = [...messages];

            console.log("texts:", texts);
            if (texts.length > 0) {
                const context = texts
                    .map(doc => `Filename: ${doc.filename}\nText:\n${doc.text.trim()}`)
                    .join("\n\n---\n\n");
                messages_.push(
                    { "role": "system", "content": `You are a helpful assistant. Use the following context:\n\n${context}` }
                );
            }

            const documents = await queryDocs(query);

            console.log("docs:", documents)

            if (documents.length > 0) {
                const context = documents.join("\n\n");
                messages_.push(
                    { "role": "system", "content": `You are a helpful assistant. Use only the following context:\n\n${context}` }
                );
            }

            messages_.push(
                { "role": "user", "content": query }
            );

            await streamChat2(messages_, appendToLastMessage, shouldStopFn);

            setIsAnswering(false);
        }
    }

    const doStop = () => {
        console.log("doStop called");
        setStopAnswering(true);
        setIsAnswering(false);
    }

    return (
        <div>
            <div className="input-box">
                <ChatInputFiles></ChatInputFiles>
                <ChatInputText onSubmit={doSubmit} />
                <ChatInputToolbar onSubmit={doSubmit} onStop={doStop} />
            </div>
            <center>
                <small>ChattyGPT kann Fehler machen. Überprüfe wichtige Informationen. Siehe Cookie-Voreinstellungen.</small>
            </center>
        </div >
    );
}

export default ChatInput;
