import json
from pathlib import Path


data = []

json_path = Path(__file__).parent.joinpath('data/json')
files = json_path.glob('*.json')
for file in files:
    with file.open('r', encoding='utf-8') as f:
        try:
            data.extend(json.load(f))

        except (KeyError, json.JSONDecodeError):
            pass

dict_to_json = {
    'intents':[]
}
for line in data:
    tag = line['tag']
    question = line['question']
    answer = line['answer']
    to_dict = {
        'tag': tag,
        'question': question,
        'answer': answer
    }
    dict_to_json['intents'].append(to_dict)

out_file = 'clean_data_to_train/data.json'
with open(out_file,'w', encoding='utf-8') as f:
    json.dump(dict_to_json, f, indent=4)