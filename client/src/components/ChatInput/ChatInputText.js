import 'components/ChatInput.css';

// Libs
//
import React, { useRef } from 'react';

// Store
//
import useChatMessageStore from 'stores/chatMessageStore';

// Component
//
function ChatInputText({ onSubmit }) {

    // State
    const { isAnswering, setText, text } = useChatMessageStore();

    // Ref to textarea tag
    const textareaRef = useRef(null);

    // On Typing
    //
    const handleChange = (e) => {
        const el = textareaRef.current;
        el.style.height = 'auto';
        el.style.height = el.scrollHeight + 'px';
        //setValue(e.target.value);
        setText(e.target.value);
    };

    // On ENTER without SHIFT
    //
    const handleKeyDown = async (e) => {
        if (e.key === 'Enter' && !e.shiftKey && isAnswering === false) {
            e.preventDefault(); // prevent newline
            if (text.trim() !== '') {
                textareaRef.current.style.height = 'auto';
                await onSubmit(text);
            }
        }
    };

    return (
        <textarea
            ref={textareaRef}
            value={text}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder="Stelle irgendeine Frage…"
            className="input-textarea ml-1 mt-2"
            rows={1}
        />
    )
}

export default ChatInputText;
