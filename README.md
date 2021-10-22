# The Web Checker

The small Python script checks ZIP files with papers in PDF format for the mention of the term "web".

The script excludes mention of the string "The Web Conference 2022", which is part of the template.

The check includes the references of the papers, i.e., with zero hits the papers do presumably not cite any papers from The Web Conference.

## Usage

Simple mode:

````$ python3 twc.py {ZIP archives}````

or verbose mode to print surrounding words of the mention:

````$ python3 twc.py -v {ZIP archives}````