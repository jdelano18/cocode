import json
import os
import sys

def getNotebooks(rootdir):
	''' get all the notebooks in the rootdir '''
	files = []
	for filename in os.listdir(rootdir):
		if filename.endswith(".ipynb"):
			files.append(filename)
		else:
			continue
	return files

def getInfo(cell):
	''' get the title and description from the top cell '''
	info = ()
	for item in cell['source'][1:3]:
		index = item.find(':')
		item = item.strip().replace('\"', '')

		info += (item[index+2:],)

	return info


def updateNotebook(rootdir, filename):
	''' update 1 notebook with title and description and new cells '''
	with open(rootdir+filename) as json_file:
		data = json.load(json_file)

		title, description = getInfo(data["cells"][0])

		# add new title and description
		html = [''' <div>
    	<img src="./coco.png" style="float: left;height: 55px">
    	<div style="height: 150px;text-align: center; padding-top:5px">
        <h1>
      	'''+ title + '''
        </h1>
        <p>'''+ description +'''</p>
    	</div>
		</div> ''']
		newInfo = {'cell_type': 'markdown', 'metadata': {}, 'source': html}
		data['cells'].insert(1, newInfo)

		for cell in data["cells"]:
			updateCell(cell)

	return data


def updateCell(cell):
	''' replace markdown cells with the keyword with a new markdown cell '''
	if cell['cell_type'] == 'markdown':
		if '# Key Code&' in cell['source']:
			cell['source'] = [''' <div style="height:40px">
		<div style="width:100%; text-align:center; border-bottom: 1px solid #000; line-height:0.1em; margin:40px 0 20px;">
    	<span style="background:#fff; padding:0 10px; font-size:25px; font-family: 'Open Sans', sans-serif;">
        Key Code
    	</span>
		</div>
		</div>
			''']

		if '# Example&' in cell['source']:
			cell['source'] = [''' <div style="height:40px">
		<div style="width:100%; text-align:center; border-bottom: 1px solid #000; line-height:0.1em; margin:40px 0 20px;">
    	<span style="background:#fff; padding:0 10px; font-size:25px; font-family: 'Open Sans', sans-serif;">
        Example
    	</span>
		</div>
		</div>
			''']

		if '# Learn More&' in cell['source']:
			cell['source'] = [''' <div style="height:40px">
		<div style="width:100%; text-align:center; border-bottom: 1px solid #000; line-height:0.1em; margin:40px 0 20px;">
    	<span style="background:#fff; padding:0 10px; font-size:25px; font-family: 'Open Sans', sans-serif;">
        Learn More
    	</span>
		</div>
		</div>
			''']

# here's the code
try:
	dir_to_convert = sys.argv[1]
	try:
		dir_to_dump_to = sys.argv[2]
	except IndexError:
		print(f"WARNING: You didn't enter a dir_to_dump_to. By default, it is now {dir_to_convert}")
		dir_to_dump_to = dir_to_convert
except IndexError:
	print("WARNING: You didn't enter a dir_to_convert or dir_to_dump_to. By default, both are now ../inprogress/")
	dir_to_convert = dir_to_dump_to = "../inprogress/"

## FORMAT CHECK
if dir_to_dump_to[-1] != '/':
	dir_to_dump_to += '/'

try:
	files = getNotebooks(dir_to_convert)
except FileNotFoundError:
	print(f"ERROR: The dir_to_convert  {dir_to_convert}  doesn't exist")
	sys.exit()

for filename in files:
	data = updateNotebook(dir_to_convert, filename)
	try:
		with open(dir_to_dump_to+filename, 'w') as outfile:
			json.dump(data, outfile)
	except FileNotFoundError:
		print(f"ERROR: The dir_to_dump_to {dir_to_dump_to} doesn't exist")
		break
