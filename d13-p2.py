import json

def test(leftside, rightside):
    if isinstance(leftside, int) and isinstance(rightside, list):
        leftside = [leftside]
    elif isinstance(leftside, list) and isinstance(rightside, int):
        rightside = [rightside]
    if isinstance(leftside, int):
        if leftside < rightside:
            return True
        elif rightside < leftside:
            return False
        else:
            return None
    else:
        leftlen = len(leftside)
        rightlen = len(rightside)
        if leftlen <= rightlen:
            minlen = leftlen
        else:
            minlen = rightlen
        for i in range(minlen):
            result = test(leftside[i], rightside[i])
            if result != None:
                return result
        if leftlen > minlen:
            return False
        elif rightlen > minlen:
            return True
        else:
            return None

def process(filename):
    result = 1
    outpackets = [[[2]], [[6]]]

    with open(filename) as infile:
        filedata = infile.readlines()

        for line in filedata:
            line = line.rstrip()
            if (line != ''):
                outpackets.append(json.loads(line))

    keepgoing = True
    while keepgoing:
        keepgoing = False
        for i in range(1, len(outpackets)):
            if not test(outpackets[i-1], outpackets[i]):
                temp = outpackets[i-1]
                outpackets[i-1] = outpackets[i]
                outpackets[i] = temp
                keepgoing = True

    for i in range(len(outpackets)):
        #print(i+1, outpackets[i])
        if outpackets[i] == [[2]] or outpackets[i] ==  [[6]]:
            result *= (i+1)

    return result

result = process('d13-p1-data.txt')
print(result)
