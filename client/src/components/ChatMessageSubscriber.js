// Libs
//
import { useEffect } from 'react';

// Store
//
import useChatMessageStore from 'stores/chatMessageStore';

// Component
//
function ChatMessagesSubscriber() {
    useEffect(() => {
        const unsubscribe = useChatMessageStore.subscribe(
            (state) => {
                console.log('Messages changed:', state.messages.length);
            },
            (state) => state.messages,
        );

        // Wichtig: Aufräumen bei Unmount
        return () => unsubscribe();
    }, []); // Leeres Array = nur 1x beim Mount

    return null;
}

export default ChatMessagesSubscriber;
