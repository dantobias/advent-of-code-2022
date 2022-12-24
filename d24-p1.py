def process(filename):

    def advance_blizzards():
        nonlocal blizzard
        for i in range(len(blizzard)):
            if blizzard[i][2] == '^':
                newrow = blizzard[i][0] - 1
                if newrow < 1:
                    newrow = len(map) - 2
                blizzard[i] = (newrow, blizzard[i][1], blizzard[i][2])
            elif blizzard[i][2] == 'v':
                newrow = blizzard[i][0] + 1
                if newrow > len(map) - 2:
                    newrow = 1
                blizzard[i] = (newrow, blizzard[i][1], blizzard[i][2])
            elif blizzard[i][2] == '<':
                newcol = blizzard[i][1] - 1
                if newcol < 1:
                    newcol = len(map[blizzard[i][0]]) - 2
                blizzard[i] = (blizzard[i][0], newcol, blizzard[i][2])
            elif blizzard[i][2] == '>':
                newcol = blizzard[i][1] + 1
                if newcol > len(map[blizzard[i][0]]) - 2:
                    newcol = 1
                blizzard[i] = (blizzard[i][0], newcol, blizzard[i][2])

    def check_move(row, col):
        if row == 0 and col != startcol:
            return False
        elif row < 0:
            return False
        elif row == len(map) - 1 and col != destcol:
            return False
        elif col < 1 or col > len(map[0]):
            return False
        else:
            for b in blizzard:
                if b[0] == row and b[1] == col:
                    return False
        return True

    def find_moves(row, col):
        upmove = check_move(row-1, col)
        downmove = check_move(row+1, col)
        leftmove = check_move(row, col-1)
        rightmove = check_move(row, col+1)
        wait = check_move(row, col)

        moves = []

        if downmove:
            moves.append((row + 1, col))
        if rightmove:
            moves.append((row, col + 1))
        if wait:
            moves.append((row, col))
        if leftmove:
            moves.append((row, col - 1))
        if upmove:
            moves.append((row - 1, col))

        return moves

    result = None

    map = []
    blizzard = []

    with open(filename) as infile:
        filedata = infile.readlines()

        for line in filedata:
            line = line.rstrip()
            map.append(line)

        for row in range(len(map)):
            for col in range(len(map[row])):
                if map[row][col] in '^v<>':
                    blizzard.append((row, col, map[row][col]))
                if row == 0 and map[row][col] == '.':
                    startrow = row
                    startcol = col
                if row == len(map)-1 and map[row][col] == '.':
                    destrow = row
                    destcol = col

    result = 0
    poslist = [(startrow, startcol)]

    while not (destrow, destcol) in poslist:
        advance_blizzards()

        newposlist = []

        for p in poslist:
            moves = find_moves(p[0], p[1])

            for m in moves:
                if not m in newposlist:
                    newposlist.append(m)

        poslist = newposlist

        result += 1
        #print(result, poslist)

    return result

result = process('d24-p1-data.txt')
#result = process('d24-p1-testdata.txt')

print(result)
