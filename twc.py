import pdftotext
def get_paper(f):
    pdf = pdftotext.PDF(f)
    return "\n\n".join(pdf)

import string
def remove_punct(text):
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    return text

def tokenise(text):
    return text.lower().split()

##############

import sys
import zipfile
import os
from collections import Counter

if len(sys.argv) <= 1:
    print("Usage: twc.py [-v] archive1.zip archive2.zip ...")
    sys.exit(1)

index = 1
verbose = False
if sys.argv[1] == "-v":
    verbose = True
    index = 2

counter = Counter()
papers = 0

for i in range(index, len(sys.argv)):
    with zipfile.ZipFile(sys.argv[i]) as zip:
        for pname in zip.namelist():
            papers = papers+1
            with zip.open(pname) as pfile:
                try:
                    pstring = get_paper(pfile)
                    # remove mentions of The Web Conference 2022
                    pstring = pstring.replace('\r', ' ').replace('\n', ' ')
                    pstring = pstring.replace("The Web Conference 2022", "")
                    pstring = pstring.replace("2022 World Wide Web Conference", "")
                    ptokens = tokenise(remove_punct(pstring))
                    count = ptokens.count("web")
                    print(pname, "mention of the term 'web':", count)
                    counter[count] = counter[count]+1
                    if (count == 1 and verbose):
                        index = ptokens.index("web")
                        print ("Single mention:", ptokens[index-5:index+5])
                except:
                    print("Error accessing", pname)

print(counter.most_common())
print("Of", papers, "papers, ", counter[0], "do not mention 'web' at all, ", counter[1], " once and ", counter[2], "twice")
