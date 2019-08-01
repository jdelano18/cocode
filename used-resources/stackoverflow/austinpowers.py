import pandas as pd
import json
import sys

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

        data['cells'][2]['source'] = question
        data['cells'][4]['source'] = answer

        data['cells'][6]['source'][0] = data['cells'][6]['source'][0].replace(
            'answerer&', answerer).replace('questioner&', questioner).replace(
            'qlink&', qlink).replace('alink&', alink)
        data['cells'][7]['source'][0] = data['cells'][7]['source'][0].replace(
            'answerer&', answerer).replace('questioner&', questioner).replace('orig&', url)

        dump_to_file(data, ID)

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
# only do this once
# with open('so-error-table.csv', 'w') as f:
#    f.write('File Id \n')

for i, row in df.iterrows():
    try:
        clean_n_write(row)
    except:
        print("something went wrong with row "+str(i))
        with open('so-error-table.csv','a') as fd:
            fd.write(str(row['PostId'])+'\n')
