# Readme

- Level 0 - Split by chapter
  - Level 1 - Split chapter by 200/50 words

[Doc id=1, children=[2,3]]
  [Doc id=2, parent-id=1]
  [Doc id=3, parent-id=1]
[Doc id=4, children=[5,6]]
  [Doc id=5, parent-id=4]
  [Doc id=6, parent-id=4]

Document
(
  "id": "ba135cd5213ac46e453a4b8ebe37de14853398788f1ccbeb269ee47b53dc8c5f",
  "content": "dlfgjdlkjfg ..",
  "score": 1.125553846359253,
  "embedding": vector of size 768,
  "meta" : {

    "chapter_name": "Introduction",
    "chapter_number": 1,
    "page_number": 1,
    "file_path": 'wu1.pdf",

    # Hierachical

    "__block_size":333,
    "__children_ids":"['e148533987..', '69ee47b53dc..']",
    "__parent_id":"e453a4b8ebe37...",
    "__level":2,
  }
)
