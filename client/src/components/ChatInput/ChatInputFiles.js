// Store
//
import useChatMessageStore from "stores/chatMessageStore";

// Component
//
function ChatInputFiles() {
    const { attachedTexts } = useChatMessageStore();

    return (
        <div className="mx-1">
            {attachedTexts.map((item, index) => {
                return (
                    <span
                        key={index}
                        className="label label-rounded label-secondary mr-2"
                    >
                        {item.filename}
                        <i
                            className="icon icon-cross ml-1"
                            style={{
                                fontSize: "0.5rem",
                                position: "relative",
                                top: "-1px",
                            }}
                        ></i>
                    </span>
                );
            })}
        </div>
    );
}

export default ChatInputFiles;
