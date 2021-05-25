import yaml
import json

json_File = '../data/fixed_json/trivia.json'

with open('../data/yml/trivia.yml', 'r') as file:
    reader = yaml.load(file)
    reader = reader['conversations']

    first_step = []
    for line in reader:
        first_step.append(line)

    QoA = []
    for line in first_step:
        question = line[0]
        answer = line[1]
        QoA.append(
            {
                'tag': question,
                'question': question,
                'answer': answer
            }
        )

with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps(QoA, indent=4))


