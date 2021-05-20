import re
import json

json_File = '../data/json/cornell_movie_first_clean.json'


lines = open('../data/cornell movie/movie_lines.txt', encoding='utf-8',
             errors='ignore').read().split('\n')
conversations = open('../data/cornell movie/movie_conversations.txt',
                     encoding='utf-8', errors='ignore').read().split('\n')


id2line = {}
for line in lines:
    _line = line.split(' +++$+++ ')
    if len(_line) == 5:
        id2line[_line[0]] = _line[4]


conversations_ids = []
for conversation in conversations[:-1]:
    _conversation = conversation.split(' +++$+++ ')[-1][1:-1].replace("'", "").replace(" ", "")
    conversations_ids.append(_conversation.split(','))


questions = []
answers = []
for conversation in conversations_ids:
    for i in range(len(conversation) - 1):
        questions.append(id2line[conversation[i]])
        answers.append(id2line[conversation[i + 1]])



def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
    return text



clean_questions = []
for question in questions:
    clean_questions.append(clean_text(question))


clean_answers = []
for answer in answers:
    clean_answers.append(clean_text(answer))


short_questions = []
short_answers = []
i = 0
for question in clean_questions:
    if 2 <= len(question.split()) <= 25:
        short_questions.append(question)
        short_answers.append(clean_answers[i])
    i += 1
clean_questions = []
clean_answers = []
i = 0
for answer in short_answers:
    if 2 <= len(answer.split()) <= 25:
        clean_answers.append(answer)
        clean_questions.append(short_questions[i])
    i += 1


z = zip(clean_questions, clean_answers)

zipped = list(z)

zipped_data = []

for line in zipped:
    i = line
    zipped_data.append(i)


QoA_to_dict = []

for i in zipped_data:
    question = i[0]
    answer = i[1]
    QoA_to_dict.append(
        {
            'tag': question,
            'question': question,
            'answer': answer
        }
    )

with open(json_File, 'w') as jsonFile:
    jsonFile.write(json.dumps(QoA_to_dict, indent=4))






















