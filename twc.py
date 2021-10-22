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

zip = zipfile.ZipFile(sys.argv[1])
for pname in zip.namelist():
    pfile = zip.open(pname)
    pstring = get_paper(pfile)
    # remove mentions of The Web Conference 2022
    pstring = pstring.replace("The Web Conference 2022", "")
    ptokens = tokenise(remove_punct(pstring))
    print(pname, "mention of the term 'web':", ptokens.count("web"))

