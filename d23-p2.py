def process(filename):

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

    for round in range(99999999):
        elfpos = {}
        for e in elf:
            elfpos[e] = True

        moves = 0
        proposed = []
        for f in elf:
            nw = (f[0]-1, f[1]-1) in elfpos
            n = (f[0]-1, f[1]) in elfpos
            ne = (f[0]-1, f[1]+1) in elfpos
            e = (f[0], f[1]+1) in elfpos
            se = (f[0]+1, f[1]+1) in elfpos
            s = (f[0]+1, f[1]) in elfpos
            sw = (f[0]+1, f[1]-1) in elfpos
            w = (f[0], f[1]-1) in elfpos

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

        props = {}
        for i in range(len(elf)):
            move = proposed[i]
            if move != None:
                if move in props:
                    props[move] += 1
                else:
                    props[move] = 1

        for i in range(len(elf)):
            move = proposed[i]
            if move != None:
                if props[move] == 1:
                    moves += 1
                    elf[i] = move

        #print(elf, '\n')
        print(round+1, moves)
        if moves == 0:
            result = round+1
            break
 
    return result

result = process('d23-p1-data.txt')
#result = process('d23-p1-testdata.txt')

print(result)
