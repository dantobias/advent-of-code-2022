def process(filename):
    result = None
    currpos = 0
    last4 = "    "
    with open(filename) as infile:
        filedata = infile.readlines()

        for line in filedata:
            line = line.rstrip()
            for c in line:
                currpos += 1
                last4 += c
                last4 = last4[1:]
                if currpos >= 4 and last4.count(last4[0]) == 1 and last4.count(last4[1]) == 1 and last4.count(last4[2]) == 1 and last4.count(last4[3]) == 1:
                    result = currpos
                    break
    return result

result = process('d06-p1-data.txt')
print(result)
