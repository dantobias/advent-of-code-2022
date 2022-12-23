def process(filename):

    def checkpos(row, col):
        for f in elf:
            if (row, col) == f:
                return True
        return False

    result = None
    elf = []

    with open(filename) as infile:
        filedata = infile.readlines()

        row = 0
        for line in filedata:
            line = line.rstrip()
            for col in range(len(line)):
                if line[col] == '#':
                    elf.append((row, col))
            row += 1

    #print(elf, '\n')

    for round in range(10):
        proposed = []
        for f in elf:
            nw = checkpos(f[0]-1, f[1]-1)
            n = checkpos(f[0]-1, f[1])
            ne = checkpos(f[0]-1, f[1]+1)
            e = checkpos(f[0], f[1]+1)
            se = checkpos(f[0]+1, f[1]+1)
            s = checkpos(f[0]+1, f[1])
            sw = checkpos(f[0]+1, f[1]-1)
            w = checkpos(f[0], f[1]-1)

            move = None

            if (nw or n or ne or e or se or s or sw or w):
                if round%4 == 0:
                    if not n and not ne and not nw and move == None:
                        move = (f[0]-1, f[1])
                    if not s and not se and not sw and move == None:
                        move = (f[0]+1, f[1])
                    if not w and not nw and not sw and move == None:
                        move = (f[0], f[1]-1)
                    if not e and not ne and not se and move == None:
                        move = (f[0], f[1]+1)
                if round%4 == 1:
                    if not s and not se and not sw and move == None:
                        move = (f[0]+1, f[1])
                    if not w and not nw and not sw and move == None:
                        move = (f[0], f[1]-1)
                    if not e and not ne and not se and move == None:
                        move = (f[0], f[1]+1)
                    if not n and not ne and not nw and move == None:
                        move = (f[0]-1, f[1])
                if round%4 == 2:
                    if not w and not nw and not sw and move == None:
                        move = (f[0], f[1]-1)
                    if not e and not ne and not se and move == None:
                        move = (f[0], f[1]+1)
                    if not n and not ne and not nw and move == None:
                        move = (f[0]-1, f[1])
                    if not s and not se and not sw and move == None:
                        move = (f[0]+1, f[1])
                if round%4 == 3:
                    if not e and not ne and not se and move == None:
                        move = (f[0], f[1]+1)
                    if not n and not ne and not nw and move == None:
                        move = (f[0]-1, f[1])
                    if not s and not se and not sw and move == None:
                        move = (f[0]+1, f[1])
                    if not w and not nw and not sw and move == None:
                        move = (f[0], f[1]-1)

            proposed.append(move)

        for i in range(len(elf)):
            move = proposed[i]
            if move != None:
                ok = True
                for j in range(len(elf)):
                    if j != i and proposed[j] == move:
                        ok = False
                        break
                if ok:
                    elf[i] = move

        #print(elf, '\n')

    result = 0

    minrow = None
    maxrow = None
    mincol = None
    maxcol = None
    for e in elf:
        if minrow == None or e[0] < minrow:
            minrow = e[0]
        if maxrow == None or e[0] > maxrow:
            maxrow = e[0]
        if mincol == None or e[1] < mincol:
            mincol = e[1]
        if maxcol == None or e[1] > maxcol:
            maxcol = e[1]

    for row in range(minrow, maxrow+1):
        for col in range(mincol, maxcol+1):
            if not checkpos(row, col):
                result += 1
 
    return result

result = process('d23-p1-data.txt')
#result = process('d23-p1-testdata.txt')

print(result)
