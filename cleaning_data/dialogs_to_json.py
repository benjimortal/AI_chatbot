import json


json_File = '../data/json/dialogs.json'
data = []
with open('data/txt/dialogs.txt', 'r') as file:
    reader = file.readlines()

    for raw in reader:
        data.append(raw)


QoA = []
for line in data:
    line = line.split('\t')
    question = line[0]
    answer = line[1]
    answer = answer.replace('\n', '')
    QoA.append(
        {
            'tag': question,
            'question': question,
            'answer': answer
        }
    )

with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps(QoA, indent=4))





