# The Web Checker

The small Python script checks ZIP files with papers in PDF format for the mention of the term "web".

The script excludes mention of the string "The Web Conference 2022" or "2022 World Wide Web Conference", which is part of the template.

The check includes the references of the papers, i.e., papers with zero hits do not cite any papers from The Web Conference.

## Usage

Simple mode:

````$ python3 twc.py {ZIP archives}````

or verbose mode to print surrounding words of single mentions:

````$ python3 twc.py -v {ZIP archives}````