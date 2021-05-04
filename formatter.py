data = []

with open('../../../Desktop/Cleaning-Cornell-Movie-Corpus-Data-master/movie_lines.txt') as fd:
    for line in fd.readlines():
        data.append(line)

for line in data:
    i = line
    print(i)
    break
