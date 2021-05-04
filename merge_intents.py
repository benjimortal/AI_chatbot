import json
from pathlib import Path


data = {
    'intents': [],
}
json_path = Path(__file__).parent.joinpath('data/json')
files = json_path.glob('*.json')
for file in files:
    with file.open('r', encoding='utf-8') as f:
        try:
            data['intents'].append(json.load(f))

        except (KeyError, json.JSONDecodeError):
            pass

out_file = json_path.joinpath('data.json')
with out_file.open('w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)


