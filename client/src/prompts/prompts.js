const Prompts = {
    //
    // Default
    //
    "default": ({ query }) => `
You are a helpful assistant. I answer the given query:
Query:
${query}`,
    //
    // Compare
    //
    "compare": ({ text1, text2 }) => `
You are a helpful assistant. I give you two texts please give me the difference:
        Text1:
${text1}

Text2:
${text2}

Context:
`,


}

export function getPrompt(key, props) {
    const template = Prompts[key]
    return template(props)
}
