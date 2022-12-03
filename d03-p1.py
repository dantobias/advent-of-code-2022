itemtypes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def rucksacks(filename):
    with open(filename) as infile:
        filedata = infile.readlines()
        sum = 0
        for line in filedata:
            line = line.rstrip()
            splitpos = int(len(line)/2)
            typefound = {}
            if splitpos>0:
                matchtype = None
                for i in range(0, splitpos):
                    typefound[line[i]] = True
                for i in range(splitpos, len(line)):
                    if line[i] in typefound and typefound[line[i]] == True:
                        matchtype = line[i]
                priority = itemtypes.rfind(matchtype)+1
                sum += priority
    return sum

sum = rucksacks('d03-p1-data.txt')
print(sum)
