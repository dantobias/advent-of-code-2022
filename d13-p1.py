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

def checkpair(pairno, pair):
    if len(pair) == 2:
        leftside = pair[0]
        rightside = pair[1]
        if test(leftside, rightside):
            return pairno
        else:
            return 0             
    else:
        return 0

def process(filename):
    result = 0

    with open(filename) as infile:
        filedata = infile.readlines()

        pair = []
        pairno = 1

        for line in filedata:
            line = line.rstrip()
            if (line != ''):
                pair.append(json.loads(line))
            else:
                result += checkpair(pairno, pair)
                pair = []
                pairno += 1
        result += checkpair(pairno, pair)

    return result

result = process('d13-p1-data.txt')
print(result)
