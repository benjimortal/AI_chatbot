import yaml
import json

json_File = 'data/json/food.json'

with open(r'data\ai.yml', 'r') as file:
    reader = yaml.load(file)


    questions_answers = []
    for q, a in reader['conversations']:
        question = q
        answer = a

        questions_answers.append(
            {
                'Tags': 'Food',
                'patterns': question,
                'responses': answer
            }
        )


with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps({'intents': questions_answers}, indent=4))
