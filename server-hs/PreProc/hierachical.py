import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath('..'))

# HierarchicalDocumentSplitter works together with
#
# See https://docs.haystack.deepset.ai/docs/automergingretriever
#
# Use AutoMergingRetriever to improve search results by returning complete parent documents
# instead of fragmented chunks when multiple related pieces match a query.

from haystack_ import Document
from haystack_ import HierarchicalDocumentSplitter

# chunk 200-300 words
# overlap 50 words
#
# [             full text           ]
# [           ]
#          [             ]
#                     [             ]

doc = Document(content="This is a simple test document")
splitter = HierarchicalDocumentSplitter(block_sizes={3, 2}, split_overlap=0, split_by="word")
result = splitter.run([doc])
print(result)

expect = """{
   "documents":[
      Document(id=3f7e91e9a775ed0815606a0bc2f732b38b7682a84d5b23c06997a8dcfa849a0d,
      "content":"This is a simple test document",
      "meta":{
         "__block_size":0,
         "__parent_id":"None",
         "__children_ids":[
            "bb013b16cc32e42a19f85b509e99068f091b73b656bf3de35339c8102d8b491e",
            "a96433ddb7017a1acd758c58ddc1908ee23c22977cfd2789d2154c80cbe8ab93"
         ],
         "__level":0
      }")",
      Document(id=bb013b16cc32e42a19f85b509e99068f091b73b656bf3de35339c8102d8b491e,
      "content":"This is a ",
      "meta":{
         "__block_size":3,
         "__parent_id":"3f7e91e9a775ed0815606a0bc2f732b38b7682a84d5b23c06997a8dcfa849a0d",
         "__children_ids":[
            "db5c1bb5d5248ad5c424d425358026e4d5695114d20b4b64ed19132fa4ab2d71",
            "b727a8ddd216114732955d1eb9a36a6901e22fcdcdd7cec9fca574327aa59fdd"
         ],
         "__level":1,
         "source_id":"3f7e91e9a775ed0815606a0bc2f732b38b7682a84d5b23c06997a8dcfa849a0d",
         "page_number":1,
         "split_id":0,
         "split_idx_start":0
      }")",
      Document(id=a96433ddb7017a1acd758c58ddc1908ee23c22977cfd2789d2154c80cbe8ab93,
      "content":"simple test document",
      "meta":{
         "__block_size":3,
         "__parent_id":"3f7e91e9a775ed0815606a0bc2f732b38b7682a84d5b23c06997a8dcfa849a0d",
         "__children_ids":[
            "6189c3e8b3884004829722d7ba6c368ae5cd0b9c32ef2f3b0bf3112ba9c70910",
            "643cc080114410f42456b0d9d739c39ffcf04f557a130f8db9ec801d5fe318e5"
         ],
         "__level":1,
         "source_id":"3f7e91e9a775ed0815606a0bc2f732b38b7682a84d5b23c06997a8dcfa849a0d",
         "page_number":1,
         "split_id":1,
         "split_idx_start":10
      }")",
      Document(id=db5c1bb5d5248ad5c424d425358026e4d5695114d20b4b64ed19132fa4ab2d71,
      "content":"This is ",
      "meta":{
         "__block_size":2,
         "__parent_id":"bb013b16cc32e42a19f85b509e99068f091b73b656bf3de35339c8102d8b491e",
         "__children_ids":[

         ],
         "__level":2,
         "source_id":"bb013b16cc32e42a19f85b509e99068f091b73b656bf3de35339c8102d8b491e",
         "page_number":1,
         "split_id":0,
         "split_idx_start":0
      }")",
      Document(id=b727a8ddd216114732955d1eb9a36a6901e22fcdcdd7cec9fca574327aa59fdd,
      "content":"a ",
      "meta":{
         "__block_size":2,
         "__parent_id":"bb013b16cc32e42a19f85b509e99068f091b73b656bf3de35339c8102d8b491e",
         "__children_ids":[

         ],
         "__level":2,
         "source_id":"bb013b16cc32e42a19f85b509e99068f091b73b656bf3de35339c8102d8b491e",
         "page_number":1,
         "split_id":1,
         "split_idx_start":8
      }")",
      Document(id=6189c3e8b3884004829722d7ba6c368ae5cd0b9c32ef2f3b0bf3112ba9c70910,
      "content":"simple test ",
      "meta":{
         "__block_size":2,
         "__parent_id":"a96433ddb7017a1acd758c58ddc1908ee23c22977cfd2789d2154c80cbe8ab93",
         "__children_ids":[

         ],
         "__level":2,
         "source_id":"a96433ddb7017a1acd758c58ddc1908ee23c22977cfd2789d2154c80cbe8ab93",
         "page_number":1,
         "split_id":0,
         "split_idx_start":0
      }")",
      Document(id=643cc080114410f42456b0d9d739c39ffcf04f557a130f8db9ec801d5fe318e5,
      "content":"document",
      "meta":{
         "__block_size":2,
         "__parent_id":"a96433ddb7017a1acd758c58ddc1908ee23c22977cfd2789d2154c80cbe8ab93",
         "__children_ids":[

         ],
         "__level":2,
         "source_id":"a96433ddb7017a1acd758c58ddc1908ee23c22977cfd2789d2154c80cbe8ab93",
         "page_number":1,
         "split_id":1,
         "split_idx_start":12
      }")"
   ]
}
"""
