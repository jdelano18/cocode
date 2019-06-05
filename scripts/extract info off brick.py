import os
import json
import pandas as pd

rootdir = "."
files = []
output = [["title", "description", "tags", "url", "licence"]]

#get a list of files ending with .ipynb
for filename in os.listdir(rootdir):
    if filename.endswith(".ipynb"): 
    	files.append(filename)
    else:
        continue

#open each notebook in JSON format
for name in files:
    with open(name) as json_file:
        data = json.load(json_file)
        nextfile = []
        #if the header is in same format at the beginning of file, this will work
        #0'th one is the top cell that's the header. Source is the list of stuff we want
        #slice out first and last 2 to get rid of spaces and ---
        for item in data["cells"][0]["source"][1:-2]:
            item = item.strip().replace("\"","") #get rid of \n and "
            index = item.find(":")
            nextfile.append(item[index+2:]) #only keep what's after the : 
        output.append(nextfile)

df = pd.DataFrame(output)
df.to_csv("out.csv", index = False, header = False)