import React, { useRef } from "react";

// Store
//
import useChatMessageStore from "stores/chatMessageStore";

// Component
//
function ChatInputToolbar({ onSubmit, onStop }) {
    const { isAnswering, text, addToTexts, clearTexts } = useChatMessageStore();

    const fileInputRef = useRef(null);

    const handleAddClick = () => {
        fileInputRef.current.click(); // Triggers the hidden file input
    };

    const handleFileChange = async (event) => {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                const text_file = event.target.result;
                addToTexts({ filename: file.name, text: text_file });
            };

            reader.readAsText(file);
        }

        // Reset Input for next file
        //
        fileInputRef.current.value = "";
    };

    return (
        <div className="input-toolbar">
            <div>
                <button
                    onClick={handleAddClick}
                    className="btn btn-sm btn-primary ml-2 mr-2"
                >
                    <i className="icon icon-plus"></i> Anfügen
                </button>
                <button
                    onClick={clearTexts}
                    className="btn btn-sm btn-secondary"
                >
                    <i className="icon icon-delete"></i> Clear
                </button>
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    style={{ display: "none" }} // Hide the input
                />
            </div>
            <div>
                {isAnswering === false ? (
                    <button
                        onClick={() => onSubmit(text)}
                        disabled={text === ""}
                        className="btn btn-action btn-primary s-circle"
                    >
                        <i className="icon icon-upward"></i>
                    </button>
                ) : (
                    <button
                        onClick={() => onStop()}
                        disabled={false}
                        className="btn btn-action btn-primary s-circle"
                    >
                        ■
                    </button>
                )}
            </div>
        </div>
    );
}

export default ChatInputToolbar;
