from haystack import Document
from haystack.components.routers.metadata_router import MetadataRouter

docs = [
    Document(content="There is a horse in town", meta={"language": "en"}),
    Document(content="Paris is the capital of France.", meta={"language": "en"}),
    Document(content="Berlin ist die Haupststadt von Deutschland.", meta={"language": "de"})
]
router = MetadataRouter(rules={"en": {"field": "meta.language", "operator": "==", "value": "en"}})
result = router.run(documents=docs)
print(result)

expected_result = """
{
   "en":[
      Document(id=afc731663f7dc8d2e41a0f7e8f1e4339e0657f3ae108c1a6e10d4e6ceb994b11,
      "content":"There is a horse in town",
      "meta":{
         "language":"en"
      }")",
      Document(id=c380769357349143109ca1d492d1af31932d058b58a980f47ae8ac15b392d58a,
      "content":"Paris is the capital of France.",
      "meta":{
         "language":"en"
      }")"
   ],
   "unmatched":[
      Document(id=83e1c68255d3424939927a366cab782bde4bd989168c2843092df2ae517c3f06,
      "content":"Berlin ist die Haupststadt von Deutschland.",
      "meta":{
         "language":"de"
      }")"
   ]
}
"""
