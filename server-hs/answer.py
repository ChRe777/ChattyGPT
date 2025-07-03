from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.utils import Secret
from haystack.dataclasses import ChatMessage

prompt_template = [
    ChatMessage.from_system("You are a helpful assistant."),
    ChatMessage.from_user(
        "Given these documents, answer the question.\nDocuments:\n"
        "{% for doc in documents %}{{ doc.content }}{% endfor %}\n"
        "Question: {{query}}\nAnswer:"
    )
]

p = Pipeline()
p.add_component(instance=InMemoryBM25Retriever(document_store=InMemoryDocumentStore()), name="retriever")
p.add_component(instance=ChatPromptBuilder(template=prompt_template, required_variables={"query", "documents"}), name="prompt_builder")
p.add_component(instance=OpenAIChatGenerator(api_key=Secret.from_env_var("OPENAI_API_KEY")), name="llm")
p.add_component(instance=AnswerBuilder(), name="answer_builder")
p.connect("retriever", "prompt_builder.documents")
p.connect("prompt_builder", "llm.messages")
p.connect("llm.replies", "answer_builder.replies")
p.connect("llm.meta", "answer_builder.meta")
p.connect("retriever", "answer_builder.documents")

query = "What is the capital of France?"
result = p.run(
    {
        "retriever": {"query": query},
        "prompt_builder": {"query": query},
        "answer_builder": {"query": query},
    }
)

print(result)

example = """ {
   "joiner":{
      "answers":[
         "GeneratedAnswer(data=""Natural Language Processing (NLP) is the interaction between computers and humans in natural language, enabling machines to understand, interpret, and generate human-like text. It involves techniques like text analysis, sentiment analysis, machine translation, and speech recognition.",
         "query=""What's Natural Language Processing?",
         "documents="[

         ],
         "meta="{
            "model":"llama3.2",
            "done":true,
            "total_duration":6153099875,
            "load_duration":1051589417,
            "prompt_eval_duration":1837044625,
            "eval_duration":3260314375,
            "finish_reason":"stop",
            "completion_start_time":"2025-06-28T20:01:41.030039Z",
            "usage":{
               "completion_tokens":49,
               "prompt_tokens":45,
               "total_tokens":94
            },
            "all_messages":[
               "ChatMessage(_role=<ChatRole.ASSISTANT":"assistant"">",
               "_content="[
                  "TextContent(text=""Natural Language Processing (NLP) is the interaction between computers and humans in natural language, enabling machines to understand, interpret, and generate human-like text. It involves techniques like text analysis, sentiment analysis, machine translation, and speech recognition."")"
               ],
               "_name=None",
               "_meta="{
                  "model":"llama3.2",
                  "done":true,
                  "total_duration":6153099875,
                  "load_duration":1051589417,
                  "prompt_eval_duration":1837044625,
                  "eval_duration":3260314375,
                  "finish_reason":"stop",
                  "completion_start_time":"2025-06-28T20:01:41.030039Z",
                  "usage":{
                     "completion_tokens":49,
                     "prompt_tokens":45,
                     "total_tokens":94
                  }
               }")"
            ]
         }")",
         "GeneratedAnswer(data=""<think>\nOkay, so I need to explain what Natural Language Processing (NLP) is in as simple terms as possible. Let me start by thinking about what NLP means. It must be related to how computers handle language—so the way humans understand and communicate.\n\nMaybe I can think of it like this: humans read and write sentences, but computers don't usually do that on their own. So NLP is the field where machines learn to process human language in a way that helps them perform tasks like reading, understanding messages, or generating new ones.\n\nI should make sure to cover some key aspects without getting too technical. First, it's about understanding natural language, which means any form of communication using a living, organic organism (like speech or written words).\n\nThen, NLP uses techniques from machine learning and statistics to analyze data. That makes sense because computers are good at recognizing patterns and making predictions based on data.\n\nSo, the main goal of NLP is probably to improve how machines understand, read, write, and generate human language. It's used in a variety of applications like chatbots, translation services, sentiment analysis, and even content creation tools.\n\nI need to make sure my explanation flows well and covers these points without getting too detailed. I should keep it friendly and clear so that anyone, regardless of their background, can understand what NLP is about.\n</think>\n\nNatural Language Processing (NLP) is the field where machines learn to process human language in a way that allows them to perform tasks such as reading, understanding messages, or generating new ones. It involves using techniques from machine learning and statistics to analyze data related to natural language. The primary goal of NLP is to enhance how machines understand, read, write, and generate human language across various applications like chatbots, translation services, sentiment analysis, and content creation tools.",
         "query=""What's Natural Language Processing?",
         "documents="[

         ],
         "meta="{
            "model":"deepseek-r1:1.5b",
            "done":true,
            "total_duration":15382624000,
            "load_duration":1039162333,
            "prompt_eval_duration":1038125667,
            "eval_duration":13302394208,
            "finish_reason":"stop",
            "completion_start_time":"2025-06-28T20:01:34.863536Z",
            "usage":{
               "completion_tokens":374,
               "prompt_tokens":23,
               "total_tokens":397
            },
            "all_messages":[
               "ChatMessage(_role=<ChatRole.ASSISTANT":"assistant"">",
               "_content="[
                  "TextContent(text=""<think>\nOkay, so I need to explain what Natural Language Processing (NLP) is in as simple terms as possible. Let me start by thinking about what NLP means. It must be related to how computers handle language—so the way humans understand and communicate.\n\nMaybe I can think of it like this: humans read and write sentences, but computers don't usually do that on their own. So NLP is the field where machines learn to process human language in a way that helps them perform tasks like reading, understanding messages, or generating new ones.\n\nI should make sure to cover some key aspects without getting too technical. First, it's about understanding natural language, which means any form of communication using a living, organic organism (like speech or written words).\n\nThen, NLP uses techniques from machine learning and statistics to analyze data. That makes sense because computers are good at recognizing patterns and making predictions based on data.\n\nSo, the main goal of NLP is probably to improve how machines understand, read, write, and generate human language. It's used in a variety of applications like chatbots, translation services, sentiment analysis, and even content creation tools.\n\nI need to make sure my explanation flows well and covers these points without getting too detailed. I should keep it friendly and clear so that anyone, regardless of their background, can understand what NLP is about.\n</think>\n\nNatural Language Processing (NLP) is the field where machines learn to process human language in a way that allows them to perform tasks such as reading, understanding messages, or generating new ones. It involves using techniques from machine learning and statistics to analyze data related to natural language. The primary goal of NLP is to enhance how machines understand, read, write, and generate human language across various applications like chatbots, translation services, sentiment analysis, and content creation tools."")"
               ],
               "_name=None",
               "_meta="{
                  "model":"deepseek-r1:1.5b",
                  "done":true,
                  "total_duration":15382624000,
                  "load_duration":1039162333,
                  "prompt_eval_duration":1038125667,
                  "eval_duration":13302394208,
                  "finish_reason":"stop",
                  "completion_start_time":"2025-06-28T20:01:34.863536Z",
                  "usage":{
                     "completion_tokens":374,
                     "prompt_tokens":23,
                     "total_tokens":397
                  }
               }")"
            ]
         }")"
      ]
   }
}
"""
