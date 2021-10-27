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
import re
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
                    # remove newlines
                    pstring = pstring.replace('\r', ' ').replace('\n', ' ')
                    # remove mentions of The Web Conference 2022 in different variations
                    pstring = pstring.replace("Web Conference 2022", "")
                    pstring = pstring.replace("The Web Conference, Apr 25–29, 2022", "")
                    pstring = pstring.replace("2022 World Wide Web Conference", "")
                    pstring = pstring.replace("The WebConf ’22", "")
                    pstring = pstring.replace("The WebConf, Lyon, France", "")
                    pstring = re.sub(r'[wW][wW][wW]..?22', '', pstring)
                    pstring = re.sub(r'[wW][wW][wW]..?.?.?.?22', '', pstring)
                    pstring = pstring.replace("WWW, FR", "")
                    pstring = pstring.replace("WWW, April 25–29, 2022, Lyon, France", "")
                    # remove URIs (to exclude http://www.)
                    pstring = re.sub(r'http\S+', '', pstring)
                    # remove URIs without HTTP but starting with www. - not sure that is needed
#                    pstring = re.sub(r'www\.\S+', '', pstring)

                    # lowercase, tokenise, remove punctuation
                    ptokens = tokenise(remove_punct(pstring))

                    count = 0
                    count = count + ptokens.count("web")
                    count = count + ptokens.count("www")

                    if (verbose):
                        print(pname, "mention of the term 'web' or 'www':", count)
                        indices = [i for i, x in enumerate(ptokens) if x == "web" or x == "www"]
                        print(indices)
                        for i in indices:
                            print(ptokens[i-5:i+5])

                    id = pname.replace("TheWebConf_2022_paper_", "")
                    id = id.replace(".pdf", "")
                    print(id, ",", count)

                    counter[count] = counter[count]+1
                except:
                    print("Error accessing", pname)

print(counter.most_common())
print("Of", papers, "papers, ", counter[0], "do not mention 'web' or 'www' at all, ", counter[1], " once, ", counter[2], "twice, ", counter[3], "three times")
