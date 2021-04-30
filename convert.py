import yaml
import json

json_File = 'data/json_test/trivia_test.json'

with open('data/yml/trivia.yml', 'r') as file:
    reader = yaml.load(file)
    reader = reader['conversations']


    first_step = []
    for line in reader:
        first_step.append(line)

    ai_dict = {
        'tags': 'trivia',
        'question': [],
        'answer': []
    };

    for line in first_step:
        question = line[0]
        answer = line[1]
        ai_dict['question'].append(question)
        ai_dict['answer'].append(answer)

with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps({'intents':[ai_dict]}, indent=4))


