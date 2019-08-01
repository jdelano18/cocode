import json
import os
import sys

def getNotebooks():
	''' get all the notebooks in the rootdir '''
	files = []
	for filename in os.listdir('./'):
		if filename.endswith(".ipynb"):
			files.append(filename)
		else:
			continue
	return files

def updateNotebook(filename):
	if '-mpl' in str(filename):
		tags = "Visualisations, Matplotlib"
	else:
		tags = "Visualisations, Bokeh"
	with open('./'+filename) as json_file:
		data = json.load(json_file)
		print(filename)
		title = {
			   "cell_type": "markdown",
			   "metadata": {},
			   "source": [
			    "---\n",
			    "title: \"title\"\n",
			    "description: \"desc\"\n",
			    "tags: "+ tags +"\n",
			    "URL: http://holoviews.org/gallery/index.html \n",
			    "Licence: \n",
			    "Creator: \n",
			    "Meta: \"\"\n",
			    "\n",
			    "---"
			   ]
			  }
		prelim = {
			   "cell_type": "markdown",
			   "metadata": {},
			   "source": ["## Preliminaries"]
			  }

		data['cells'].insert(0, title)
		data['cells'].insert(1, prelim)

	return data

files = getNotebooks()

for filename in files:
	data = updateNotebook(filename)
	with open('./'+filename, 'w') as outfile:
		json.dump(data, outfile)
