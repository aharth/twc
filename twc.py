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
                    # remove mentions of The Web Conference 2022
                    pstring = pstring.replace("The Web Conference 2022", "")
                    pstring = pstring.replace("2022 World Wide Web Conference", "")
                    pstring = pstring.replace("WWW ’22", "")
                    pstring = pstring.replace("WWW 2022", "")
                    pstring = pstring.replace("WWW, FR", "")
                    pstring = pstring.replace("www ’22", "")
                    pstring = pstring.replace("WWW, April 25–29, 2022, Lyon, France", "")
                    pstring = pstring.replace("WWW ’2022", "")
                    # remove URIs (to exclude http://www.)
                    pstring = re.sub(r'http\S+', '', pstring)

                    # lowercase, tokenise, remove punctuation
                    ptokens = tokenise(remove_punct(pstring))

                    count = 0
                    count = count + ptokens.count("web")
                    count = count + ptokens.count("www")

#                    if (ptokens.count("web") and verbose):
#                        index = ptokens.index("web")
#                        print ("Single mention 'web':", ptokens[index-5:index+5])

#                    if (ptokens.count("www") and verbose):
#                        index = ptokens.index("www")
#                        print ("Single mention 'www':", ptokens[index-5:index+5])

                    if (verbose):
                        print(pname, "mention of the term 'web' or 'www':", count)

                    id = pname.replace("TheWebConf_2022_paper_", "")
                    id = id.replace(".pdf", "")
                    print(id, ",", count)

                    counter[count] = counter[count]+1
                except:
                    print("Error accessing", pname)

print(counter.most_common())
print("Of", papers, "papers, ", counter[0], "do not mention 'web' or 'www' at all, ", counter[1], " once, ", counter[2], "twice, ", counter[3], "three times")
