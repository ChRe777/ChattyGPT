
f = open("docs.txt")
content = f.read()
lines = content.splitlines()
current_page_number = 1

def parse_page_nr(line):
    s = line
    start = s.find('(') + 1
    end = s.find(')')
    page_number = int(s[start:end])
    return page_number

import json
def parse_meta(line):
    meta = json.loads(line)
    return meta

import re
def remove_page_info(line):
    cleaned = re.sub(r'/page\(\d+\)', '', line)
    return cleaned

buffer = []
for line in lines:
    if line.startswith("---"):
        print("new page")
    if line.startswith("/page"):
        old = current_page_number
        current_page_number = parse_page_nr(line) + 1
        line = remove_page_info(line)
    if line.startswith("{"):
        meta = parse_meta(line)
        meta["page_number"] = current_page_number
        line = json.dumps(meta)
    if line != "":
        buffer.append(line)


f2 = open("docs2.txt", "w")
for line in buffer:
    f2.write(line + "\n")
