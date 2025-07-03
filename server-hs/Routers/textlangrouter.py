# pip install langdetect
#
from haystack.components.routers.text_language_router import TextLanguageRouter

router = TextLanguageRouter(languages=["en"])
result = router.run(text="What's your query?")
print(result)

# {'unmatched': "What's your query?"}
#  or
# {'en': "What's your query?"}
#

# p = Pipeline()
# p.add_component(instance=TextLanguageRouter(), name="text_language_router")
# p.add_component(instance=InMemoryBM25Retriever(document_store=document_store), name="retriever")
# p.connect("text_language_router.en", "retriever.query")
# p.run({"text_language_router": {"text": "What's your query?"}})
