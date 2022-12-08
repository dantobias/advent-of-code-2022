def process(filename):
    result = 0
    with open(filename) as infile:
        filedata = infile.readlines()

        currline = 0
        maxnum = []
        visiblearray = []
        treearray = []

        for line in filedata:
            line = line.rstrip()
            visiblearray.append([])
            treearray.append([])
            if currline == 0:
                result += len(line)
                for i in range(len(line)):
                    value = int(line[i])
                    maxnum.append(value)
                    visiblearray[currline].append(True)
                    treearray[currline].append(value)
            else:
                maxinline = -1
                for i in range(len(line)):
                    value = int(line[i])
                    visible = False
                    if i == 0 or i == len(line)-1:
                        visible = True
                    if value > maxnum[i]:
                        visible = True
                        maxnum[i] = value
                    if value > maxinline:
                        visible = True
                        maxinline = value
                    visiblearray[currline].append(visible)
                    treearray[currline].append(value)
                    if visible:
                        result += 1
            currline += 1

        maxnum = []
        
        for i in range(len(treearray)-1, -1, -1):
            maxinline = -1
            if i == len(treearray)-1:
                for j in range(len(treearray[i])):
                    maxnum.append(-1)
            for j in range(len(treearray[i])-1, -1, -1):
                if treearray[i][j] > maxinline:
                    maxinline = treearray[i][j]
                    if not visiblearray[i][j]:
                        visiblearray[i][j] = True
                        result += 1
                if treearray[i][j] > maxnum[j]:
                    maxnum[j] = treearray[i][j]
                    if not visiblearray[i][j]:
                        visiblearray[i][j] = True
                        result += 1

    for i in range(len(visiblearray)):
        s = ''
        for j in range(len(visiblearray[i])):
            if visiblearray[i][j]:
                s += 'V'
            else:
                s += ' '
        print(s)

    return result

        

result = process('d08-p1-data.txt')
print(result)
