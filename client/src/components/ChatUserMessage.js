import "./ChatMessage.css"

function ChatUserMessage({ message }) {
    return <div className="user-message-right">
        <div className="user-message chat-message">{message}</div>
    </div>
}

export default ChatUserMessage;
