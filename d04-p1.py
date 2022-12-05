def cleanup(filename):
    with open(filename) as infile:
        filedata = infile.readlines()
        fully_contained = 0
        for line in filedata:
            line = line.rstrip()
            if len(line)>0:
                range = line.split(',')
                endpoints1 = range[0].split('-')
                endpoints2 = range[1].split('-')
                if (int(endpoints1[0]) <= int(endpoints2[0]) and int(endpoints1[1]) >= int(endpoints2[1])) or (int(endpoints2[0]) <= int(endpoints1[0]) and int(endpoints2[1]) >= int(endpoints1[1])):
                    fully_contained += 1
    return fully_contained

result = cleanup('d04-p1-data.txt')
print(result)
