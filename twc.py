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

if len(sys.argv) <= 1:
    print("Usage: twc.py [-v] archive1.zip archive2.zip ...")
    sys.exit(1)

index = 1
verbose = False
if sys.argv[1] == "-v":
    verbose = True
    index = 2

for i in range(index, len(sys.argv)):
    zip = zipfile.ZipFile(sys.argv[i])
    for pname in zip.namelist():
        pfile = zip.open(pname)
        pstring = get_paper(pfile)
        # remove mentions of The Web Conference 2022
        pstring = pstring.replace('\r', ' ').replace('\n', ' ')
        pstring = pstring.replace("The Web Conference 2022", "")
        pstring = pstring.replace("2022 World Wide Web Conference", "")
        ptokens = tokenise(remove_punct(pstring))
        count = ptokens.count("web")
        print(pname, "mention of the term 'web':", count)
        if (count == 1 and verbose):
            index = ptokens.index("web")
            print ("Single mention:", ptokens[index-5:index+5])

    
