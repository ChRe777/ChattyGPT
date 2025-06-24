// Libs
//
import { useEffect, useRef } from "react";

// Stores
//
import useChatMessageStore from "stores/chatMessageStore";

// Components
//
import ChatUserMessage from "./ChatUserMessage";
import ChatBotMessage from "./ChatBotMessage";

// Component
//
function ChatMessages() {
    const { messages } = useChatMessageStore();
    const bottomRef = useRef(null);

    useEffect(() => {
        // Scroll to bottom on new messages
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]); // runs every time messages change

    return (
        <div className="chat-messages">
            {messages.map((item, index, all) => {
                if (item.role === "user") {
                    console.log(all);
                    return (
                        <ChatUserMessage
                            key={index}
                            message={item.content}
                        ></ChatUserMessage>
                    );
                } else {
                    return (
                        <ChatBotMessage
                            key={index}
                            message={item.content}
                        ></ChatBotMessage>
                    );
                }
            })}
            {/* Invisible anchor to scroll to */}
            <div ref={bottomRef} />
        </div>
    );
}

export default ChatMessages;
