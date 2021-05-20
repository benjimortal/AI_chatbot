import yaml
import json


json_File = '../data/json/computers.json'

with open('../data/yml/computers.yml', 'r') as file:
    reader = yaml.load(file)


    questions_answers = []
    for q, a in reader['conversations']:
        question = q
        answer = a

        questions_answers.append(
            {
                'Tag': 'Computers',
                'patterns': question,
                'responses': answer
            }
        )


with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps({'intents': questions_answers}, indent=4))
