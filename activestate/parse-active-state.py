import json
from os import walk

class Brick():
    def __init__(self, full_path, name, files):
        self.full_path = full_path
        self.files = files
        self.name = name
        self._setFiles()
        self._setTitle()
        self._setDescription()

    def _setFiles(self):
        for file in files:
            if 'README.md' == file:
                with open(self.full_path +'/'+ file, 'r') as myfile:
                    self.readme = [line.strip() for line in myfile.readlines()]
            if file.endswith('.py'):
                with open(self.full_path +'/'+ file, 'r') as myfile:
                    self.script = myfile.read()

    def _setTitle(self):
        first_line = self.readme[0]
        i = first_line.find('## ')
        self.title = first_line[3:] if i != -1 else 'error: somethings wrong'

    def _setDescription(self):
        self.description = '\n'.join(self.readme[5:])

    def _firstcell(self):
        markdown_cell = {'cell_type': 'markdown',
            'metadata': {},
            'source': ['---\n',
            'title: "'+self.title+'"\n',
            'description: "'+self.description+'"\n',
            'tags: \n',
            'URL: https://github.com/ActiveState/code\n',
            'Licence: \n',
            'Creator: \n',
            'Meta: \n',
            '\n',
            '---']}

        return markdown_cell

    def write_to_file(self):
        with open ('./template.ipynb') as json_file:
            data = json.load(json_file)

            data['cells'].insert(0, self._firstcell())
            data['cells'][2]['source'] = self.script

        with open ('../inprogress/'+str(self.name)+'.ipynb', 'w') as outfile:
            json.dump(data, outfile)

##############
mypath='/Users/jimmydelano/active-state/code/recipes/Python/'

for (dirpath, _, files) in walk(mypath):
    if len(dirpath) == len(mypath):
        continue

    name = dirpath[len(mypath)+1:]

    b = Brick(dirpath, name, files)
    b.write_to_file()
