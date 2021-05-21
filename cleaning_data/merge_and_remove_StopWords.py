import json
from pathlib import Path
from nltk.corpus import stopwords
en_stops = set(stopwords.words('english'))

data = []
remove_stopW = []
tags = []
answers = []

json_path = Path(__file__).parent.joinpath('../data/json')
files = json_path.glob('*.json')
for file in files:
    with file.open('r', encoding='utf-8') as f:
        try:
            data.extend(json.load(f))

        except (KeyError, json.JSONDecodeError):
            pass

for line in data:
    answer = line['answer']
    answers.append(answer)

for line in data:
    tag = line['tag']
    tag = str(tag)
    tag = tag.split()
    temp = []
    for i in tag:
        if i not in en_stops:
            temp.append(i)
    remove_stopW.append(temp)

for line in remove_stopW:
    line = str(line)
    line = line.replace(',', '').replace("'", '')
    tags.append(line)

z = zip(tags, answers)
zipped = list(z)
zipped_data = []

for i in zipped:
    zipped_data.append(i)

dict_to_json = {
    'intents': []
}
for line in zipped_data:
    tag = line[0]
    tag = tag.replace('[', '').replace(']', '')
    answer = line[1]
    to_dict = {
        'tag': tag,
        'question': [tag],
        'answer': [answer]
    }
    dict_to_json['intents'].append(to_dict)

out_file = '../cleaned_data/data_remove_stop.json'
with open(out_file,'w', encoding='utf-8') as f:
    json.dump(dict_to_json, f, indent=4)
