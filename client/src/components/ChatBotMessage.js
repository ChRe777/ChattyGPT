// Styles
//
import "./ChatMessage.css"

// Components
//
import Markdown from 'markdown-to-jsx';

// Component
//
function ChatBotMessage({ message }) {
    return (
        <div className="bot-message chat-message">
            {message === ''
                ? <progress className="progress" max="100"></progress>
                : <Markdown>{message}</Markdown>}
        </div>
    );
}

export default ChatBotMessage;
