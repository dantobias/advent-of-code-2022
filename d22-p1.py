def process(filename):

    def move(moves):
        nonlocal row
        nonlocal column
        for i in range(moves):
            if facing == 0:
                nextrow = row
                nextcolumn = column + 1
                if nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                    nextcolumn = 1
                    while board[nextrow-1][nextcolumn-1] == ' ':
                      nextcolumn += 1
            elif facing == 1:
                nextrow = row + 1
                nextcolumn = column
                if nextrow > len(board) or nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                    nextrow = 1
                    while nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                      nextrow += 1
            elif facing == 2:
                nextrow = row
                nextcolumn = column - 1
                if nextcolumn < 1 or board[nextrow-1][nextcolumn-1] == ' ':
                    nextcolumn = len(board[nextrow-1])
                    while board[nextrow-1][nextcolumn-1] == ' ':
                      nextcolumn -= 1
            elif facing == 3:
                nextrow = row - 1
                nextcolumn = column
                if nextrow < 1 or nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                    nextrow = len(board)
                    while nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                      nextrow -= 1
            if board[nextrow-1][nextcolumn-1] == '.':
                row = nextrow
                column = nextcolumn
            else:
                break
            #print(row, column, facing)

    def turn(dir):
        nonlocal facing
        if dir == 'R':
            facing = (facing + 1) % 4
        elif dir == 'L':
            facing = (facing - 1) % 4
        #print('Turn', facing)

    result = None

    board = []
    path = ''

    with open(filename) as infile:
        filedata = infile.readlines()

        section = 1
        for line in filedata:
            line = line.rstrip()
            if section == 1 and line == '':
                section = 2
            elif section == 1:
                board.append(line)
            elif section == 2:
                path = line

    row = 1
    column = 1
    facing = 0
    while board[row-1][column-1] != '.':
        column += 1

    currmoves = ''
    for m in path:
        if m == 'L':
            move(int(currmoves))
            turn(m)
            currmoves = ''
        elif m == 'R':
            move(int(currmoves))
            turn(m)
            currmoves = ''
        else:
            currmoves += m
    move(int(currmoves))

    result = 1000*row + 4*column + facing

    return result

result = process('d22-p1-data.txt')
#result = process('d22-p1-testdata.txt')

print(result)
