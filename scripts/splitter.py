# script to take a file of bricks and split them up into their own files
import json
import pandas as pd
import re
import os

def getTitle(title):
    # takes title cell and parses out the name after title: "pandas csv or whatever"
    # and gets the name of the title so we can name the file
    index = title.find("title:")
    title = title[index:]
    parens = [pos for pos, char in enumerate(title) if char == '\"']
    return title[ parens[0]+1 : parens[1] ]

def writeToNotebook(filename, file):
    # take string file (turn to dict with eval) 
    # and string filename and write to filename.ipynb
    with open("../inprogress/"+filename+".ipynb", 'w') as outfile:
        json.dump(eval(file), outfile)


def makeNext(data, stop):
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
    writeToNotebook(filename, file)
    return data[count+1:],stop


# enter name of file that contains the series of bricks
with open("../basics.ipynb") as json_file:
    data = json.load(json_file)
    stop = False

    data = list(data["cells"])
    while (len(data) != 0) and (not stop):
        data,stop = makeNext(data, stop)

