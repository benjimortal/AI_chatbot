import json
from pathlib import Path
from nltk.corpus import stopwords

data = []

json_path = Path(__file__).parent.joinpath('../data/fixed_json')
files = json_path.glob('*.json')
for file in files:
    with file.open('r', encoding='utf-8') as f:
        try:
            data.extend(json.load(f))

        except (KeyError, json.JSONDecodeError):
            pass

dict_to_json = {
    'intents': []
}

for line in data:
    question = line['question']
    answer = line['answer']
    to_dict = {
        'tag': question,
        'question': [question],
        'answer': answer
    }
    dict_to_json['intents'].append(to_dict)

out_file = '../cleaned_data/cleaned_data.json'
with open(out_file,'w', encoding='utf-8') as f:
    json.dump(dict_to_json, f, indent=4)


