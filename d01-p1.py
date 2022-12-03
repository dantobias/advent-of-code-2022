def find_max_calories(filename):
    with open(filename) as infile:
        filedata = infile.readlines()
        maxcal = 0
        currcal = 0
        for line in filedata:
            line = line.rstrip()                       
            if line=='':
                if currcal > maxcal:
                    maxcal = currcal
                currcal = 0
            else:
                currcal += int(line)
    return maxcal

print(find_max_calories('d01-p1-data.txt'))
