from haystack import Document
from haystack.components.samplers.top_p import TopPSampler

sampler = TopPSampler(top_p=0.99, score_field="similarity_score")
docs = [
    Document(content="Berlin", meta={"similarity_score": -10.6}),
    Document(content="Belgrade", meta={"similarity_score": -8.9}),
    Document(content="Sarajevo", meta={"similarity_score": -4.6}),
]
output = sampler.run(documents=docs)
docs = output["documents"]
print(docs)
