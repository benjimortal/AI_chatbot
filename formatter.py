data = []

with open('data/cornell movie/movie_lines.txt') as fd:
    for line in fd.readlines():
        data.append(line)

for line in data:
    i = line
    print(i)
    break
