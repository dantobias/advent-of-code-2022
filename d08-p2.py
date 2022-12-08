def process(filename):
    result = 0
    with open(filename) as infile:
        filedata = infile.readlines()

        currline = 0
        treearray = []

        for line in filedata:
            line = line.rstrip()
            treearray.append([])
            for i in range(len(line)):
                value = int(line[i])
                treearray[currline].append(value)
            currline += 1

        maxscore = 0
        
        for i in range(1, len(treearray)-1):
            for j in range(1, len(treearray[i])-1):
                # up
                curri = i - 1
                while curri>0 and treearray[curri][j] < treearray[i][j]:
                    curri -= 1
                upscore = i - curri

                # down
                curri = i + 1
                while curri<len(treearray)-1 and treearray[curri][j] < treearray[i][j]:
                    curri += 1
                downscore = curri - i

                # left
                currj = j - 1
                while currj>0 and treearray[i][currj] < treearray[i][j]:
                    currj -= 1
                leftscore = j - currj

                # right
                currj = j + 1
                while currj<len(treearray[i])-1 and treearray[i][currj] < treearray[i][j]:
                    currj += 1
                rightscore = currj - j

                score = upscore * downscore * leftscore * rightscore
                if score > maxscore:
                    maxscore = score
                    #print(i, j, score, maxscore, leftscore, rightscore, upscore, downscore)

    return maxscore

result = process('d08-p1-data.txt')
print(result)
