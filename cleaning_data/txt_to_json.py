
import json

json_File = '../data/json/Question_answer2.json'

QoA = []
with open('data/txt/Question answer2.txt', 'r') as file:
    reader = file.readlines()

    for raw in reader:
        QoA.append(raw)


QoA_to_dict = []

for line in QoA:
    line = line.split('\t')
    question = line[0]
    answer = line[1]
    answer = answer.replace('\n', '')
    QoA_to_dict.append(
        {
            'tag': question,
            'question': question,
            'answer': answer
        }
    )


with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps(QoA_to_dict, indent=4))





