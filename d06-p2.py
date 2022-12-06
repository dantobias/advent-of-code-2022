def process(filename):
    result = None
    currpos = 0
    last14 = "              "
    with open(filename) as infile:
        filedata = infile.readlines()

        for line in filedata:
            line = line.rstrip()
            for c in line:
                currpos += 1
                last14 += c
                last14 = last14[1:]
                if currpos >= 14:
                    diff = True
                    for i in range(14):
                        if last14.count(last14[i]) != 1:
                            diff = False
                    if diff:
                        result = currpos
                        break
    return result

result = process('d06-p1-data.txt')
print(result)
