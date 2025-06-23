import './ChatMessage.css';

// Component
//
function ChatMessage({ html }) {
    const processedHtml = html.replaceAll("\\n", "<br>");
    return (
        <div
            className="chat-message"
            dangerouslySetInnerHTML={{ __html: processedHtml }}
        />
    );
}

export default ChatMessage;
