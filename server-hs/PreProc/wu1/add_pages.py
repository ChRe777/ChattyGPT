def get_lines(filename):
    f = open(filename)
    content = f.read()
    lines = content.splitlines()
    return lines

def is_page_nr(line):
    try:
        x = int(line)
        return True, x
    except:
        return False, None

lines = get_lines("wu1.txt")
f1 = open("wu1_pages.txt", "a")
for line in lines:
    is_page, x = is_page_nr(line)
    if is_page:
        print(x)
        f1.write(f"/page({x})")
    else:
        f1.write(line)
    f1.write("\n")
