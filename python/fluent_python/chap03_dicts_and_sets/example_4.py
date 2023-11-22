import re
import sys

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            # wrong way to do it
            # occurencies = index.get(word, [])
            # occurencies.append(location)
            # index[word] = occurencies
            
            # right way to do it (seems like a gambiarra)
            index.setdefault(word, []).append(location)
            # it is the same as
            # if key no in my_dict:
            #     my_dict[key] = []
            # my_dict[key].append(new_value)
            # but with only one search for the key in the dict

for word in sorted(index, key=str.upper):
    print(word, index[word])