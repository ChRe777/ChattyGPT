import useChatMessageStore from "stores/chatMessageStore";

export function subscribeChatMessagesChanged() {
    useChatMessageStore.subscribe(
        (items) => {
            console.log("nix");
        },
        (state) => state.messages,
    );
}
