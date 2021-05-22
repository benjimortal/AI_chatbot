import json


json_File = '../data/fixed_json/QoA_dialog.fixed_json'
answers = []
questions = []
with open('data/txt/questions.txt', 'r') as Qfile:
    readerQ = Qfile.readlines()

    for raw in readerQ:
        questions.append(raw)


with open('data/txt/answers.txt', 'r') as Afile:
    readerA= Afile.readlines()

    for raw in readerA:
        answers.append(raw)


z = zip(questions, answers)

zipped = list(z)
zipped_data = []


for i in zipped:
    zipped_data.append(i)

QoA_to_dict = []

for i in zipped_data:
    question = i[0].replace('\n','')
    answer = i[1].replace('\n','')
    QoA_to_dict.append(
        {
            'tag': question,
            'question': question,
            'answer': answer
        }
    )



with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps(QoA_to_dict, indent=4))
