"""
This is a script to take a file of bricks and split them up into their own files

How to run this file:
$ python splitter.py <path/to/file_to_split.ipynb> <path/to/directory_name>
"""
import json
import pandas as pd
import re
import os
import sys

def getTitle(title):
    """
    getTitle takes title cell and parses out the name after
    title: "pandas csv or whatever"
    and gets the name of the title so we can name the file
    """
    index = title.find("title:")
    title = title[index:]
    parens = [pos for pos, char in enumerate(title) if char == '\"']
    return title[ parens[0]+1 : parens[1] ]

def writeToNotebook(filename, file, out_dir):
    """
    writeToNotebook takes string file (turn to dict with eval)
    and string filename and write to filename.ipynb
    """
    with open(out_dir+filename+".ipynb", 'w') as outfile:
        json.dump(eval(file), outfile)



def makeNext(data, stop, out_dir):
    """
    makeNext adds to the nextNotebook until it finds a title brick
    """
    # concat a string with the cells until we reach the next header cell
    endFile = "], 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}, 'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3}, 'file_extension': '.py', 'mimetype': 'text/x-python', 'name': 'python', 'nbconvert_exporter': 'python', 'pygments_lexer': 'ipython3', 'version': '3.6.7'}}, 'nbformat': 4, 'nbformat_minor': 2}"
    file = "{'cells': [" + str(data[0]) + ", "
    count = 0;
    filename = getTitle(str(data[0])) # make filename the title

    for thing in data[1:]:
        # if we see a header cell as the next one, stop.
        if "URL" in str(thing) and "Licence" in str(thing):
            if "STOP" in str(thing):
                stop = True
            break
        count += 1
        file += str(thing) + ", "

    file = file[:len(file)-2] + endFile #cut off last comma and add stuff for end
    writeToNotebook(filename, file, out_dir)
    return data[count+1:],stop


try:
    # enter relative path or absolute path for file_to_split
    # will raise the IndexError if not entered
    file_to_split  = str(sys.argv[1])

except IndexError:
    print('''ERROR: Enter a file you want to split from the command line as a relative path or absolute path.''')
    file_to_split = ""
else:
    try:
        out_dir = str(sys.argv[2])
    except IndexError:
        print("# WARNING: You didn't enter an out_dir, bricks will be dumped into ../inprogress/")
        out_dir = "../inprogress/"

    ## FORMAT CHECK
    if out_dir[-1] != '/':
        out_dir += '/'

    # enter name of file that contains the series of bricks
    try:
        with open(file_to_split) as json_file:
            data = json.load(json_file)
            stop = False

            data = list(data["cells"])
            while (len(data) != 0) and (not stop):
                try:
                    data,stop = makeNext(data, stop, out_dir)
                except FileNotFoundError:
                    print("ERROR: The directory you're dumping files into doesn't exist")
                    stop = True
    except FileNotFoundError:
        print("ERROR: The notebook was not found. Check that the path you entered is correct.")
