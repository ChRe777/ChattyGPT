// Libraries
//
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

// Constants
//
const USER = "user"; // User
const ASSISTANT = "assistant"; // Bot
const SYSTEM = "system"; // Anweisung an Bot

// Store
//
const useChatMessageStore = create(
    immer((set) => ({
        // Data
        //
        messages: [],

        /* TODO:
    {
      "model": "llama3",
      "messages": [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": "Who was the first president of the USA?" },
        { "role": "assistant", "content": "George Washington." },
        { "role": "user", "content": "What year was he born?" }
      ],
      "stream": false
    }
    */

        isAnswering: false,
        text: "", // text entered by user
        attachedTexts: [], // added text files
        foundDocuments: 0,

        // Actions
        //
        //
        addMessage: (role, content) =>
            set((state) => {
                state.messages.push({ role: role, content: content });
            }),
        addUserMessage: (content) =>
            set((state) => {
                state.messages.push({ role: USER, content: content });
            }),
        addSystemMessage: (content) =>
            set((state) => {
                state.messages.push({ role: SYSTEM, content: content });
            }),
        addAssistantMessage: (content) =>
            set((state) => {
                state.messages.push({ type: ASSISTANT, content: content });
            }),
        appendToLastMessage: (text) =>
            set((state) => {
                const lastMessage = state.messages[state.messages.length - 1];
                if (lastMessage) {
                    lastMessage.content += text;
                }
            }),
        clearMessages: () =>
            set((state) => {
                state.messages = [];
            }),

        setIsAnswering: (isAnswering) =>
            set((state) => {
                state.isAnswering = isAnswering;
            }),

        // Input Text
        setText: (text) =>
            set((state) => {
                state.text = text;
            }),

        // Texts
        //
        addToTexts: (text) =>
            set((state) => {
                state.attachedTexts.push(text);
            }),

        clearTexts: () =>
            set((state) => {
                state.attachedTexts = [];
            }),

        setFoundDocs: (foundDocuments) =>
            set((state) => {
                state.foundDocuments = foundDocuments;
            }),
    })),
);

export default useChatMessageStore;
