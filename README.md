# The Web Checker

The small Python script checks ZIP files with papers in PDF format for the mention of the term "web".

The script excludes mention of the string "The Web Conference 2022" or "2022 World Wide Web Conference", which is part of the template.

The check includes the references of the papers, i.e., papers with zero hits do not cite any papers from The Web Conference.

## Installation

On Debian-based systems, do:

````# apt-get install pip build-essential libpoppler-cpp-dev pkg-config python3-dev````

````$ git clone https://github.com/aharth/twc.git````

````$ pip install pdftotext````

## Usage

Simple mode:

````$ python3 twc.py {ZIP archives}````

or verbose mode to print surrounding words of single mentions:

````$ python3 twc.py -v {ZIP archives}````