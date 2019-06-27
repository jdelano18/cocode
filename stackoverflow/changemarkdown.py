import pandas as pd
import json
import sys
import re

try:
    file = sys.argv[1]
except IndexError:
    print('You must enter a filepath (to the .csv) to convert')
    sys.exit()

def convert(ID, title, tags, url, question, answer, questioner, answerer, qlink, alink):
    with open ('./austinpowers-template.ipynb') as json_file:
        data = json.load(json_file)

        data['cells'][0]['source'][1] = 'title: "'+title+'"\n'
        data['cells'][0]['source'][3] = 'tags: "'+tags+'"\n'
        data['cells'][0]['source'][4] = 'URL: '+url+'\n'

        q = update_markdown(data, question, 2)
        a = update_markdown(data, answer, q+2)
        # data['cells'][2]['source'] = question
        # data['cells'][4]['source'] = answer

        data['cells'][a+2]['source'][0] = data['cells'][a+2]['source'][0].replace(
            'answerer&', answerer).replace('questioner&', questioner).replace(
            'qlink&', qlink).replace('alink&', alink)
        data['cells'][a+3]['source'][0] = data['cells'][a+3]['source'][0].replace(
            'answerer&', answerer).replace('questioner&', questioner).replace('orig&', url)

        dump_to_file(data, ID)

def update_markdown(data, content, i):
    splitted = re.split('<pre><code>|</code></pre>',content)

    for new_index, snippet in zip(range(i, i+len(splitted)), splitted):
        cell = {"metadata" : {}}
        if '<p>' in snippet:
            cell['cell_type'] = "markdown"
        else:
            cell["cell_type"] = "code"
            cell['execution_count'] : null
            cell['outputs'] : []

        cell['source'] = snippet
        data['cells'].insert(new_index, cell)

    print('------------------------------')
    print(i+len(splitted))
    print('------------------------------')

    return i+len(splitted)


def dump_to_file(data, ID):
    with open ('../sobricks/'+str(ID)+'.ipynb', 'w') as outfile:
        json.dump(data, outfile)

def clean_n_write(row):
    tags = str(row['Tags']).replace('><',', ')[1:-1]
    url = f"https://stackoverflow.com/questions/{row['PostId']}"
    qlink = f"https://stackoverflow.com/users/{row['Id.3']}"
    alink = f"https://stackoverflow.com/users/{row['Id.4']}"
    convert(ID = row['PostId'], title = row['Title'], tags = tags, url = url, question = row['Body'],
                  answer = row['Body.1'], questioner = row['DisplayName'], answerer = row['DisplayName.1'],
                  qlink = qlink, alink = alink)


df = pd.read_csv(file, low_memory = False)
for i, row in df.iterrows():
    if i == 10:
        break
    print(row['PostId'])
    try:
        clean_n_write(row)
    except:
        #print(str(row['PostId']))
        # error table of Id's
        with open('so-error-table.csv','a') as fd:
            fd.write(str(row['PostId'])+'\n')
