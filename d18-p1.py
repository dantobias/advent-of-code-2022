def process(filename):
    with open(filename) as infile:
        filedata = infile.readlines()

        cubes = []

        for line in filedata:
            line = line.rstrip()
            coords = [int(i) for i in line.split(',')]
            cubes.append(coords)

        result = 0
        for c in cubes:
            sides = 6
            for d in cubes:
                equal = 0
                oneoff = 0
                for i in range(3):
                    if c[i] == d[i]:
                        equal += 1
                    elif abs(c[i] - d[i]) == 1:
                        oneoff += 1
                if equal == 2 and oneoff == 1:
                    sides -= 1
            result += sides

    return result

result = process('d18-p1-data.txt')
#result = process('d18-p1-testdata.txt')

print(result)
