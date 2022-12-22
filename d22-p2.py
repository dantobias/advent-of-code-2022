def process(filename):

    def offtheend(row, column, facing):
        nextrow = row
        nextcolumn = column
        nextfacing = facing

        if filename == 'd22-p1-testdata.txt':
            if facing == 0: # right
                if row <= 4:
                    nextfacing = 2
                    nextrow = 13 - row
                    nextcolumn = 16
                elif row <= 8:
                    nextfacing = 1
                    nextrow = 9
                    nextcolumn = 21 - row
                else:
                    nextfacing = 2
                    nextrow = 13 - row
                    nextcolumn = 12
            elif facing == 1: # down
                if column <= 4:
                    nextfacing = 3
                    nextrow = 13 - row
                    nextcolumn = 12
                elif column <= 8:
                    nextfacing = 0
                    nextrow = 17 - column
                    nextcolumn = 9
                elif column <= 12:
                    nextfacing = 3
                    nextrow = 8
                    nextcolumn = 13 - column
                else:
                    nextfacing = 3
                    nextrow = 8
                    nextcolumn = 13 - column
            elif facing == 2: # left
                if row <= 4:
                    nextfacing = 1
                    nextrow = 5
                    nextcolumn = row + 4
                elif row <= 8:
                    nextfacing = 1
                    nextrow = 9
                    nextcolumn = 21 - row
                else:
                    nextfacing = 3
                    nextrow = 8
                    nextcolumn = 17 - row
            elif facing == 3: # up
                if column <= 4:
                    nextfacing = 1
                    nextrow = 9
                    nextcolumn = 13 - column
                elif column <= 8:
                    nextfacing = 0
                    nextrow = column - 4
                    nextcolumn = 9
                elif column <= 12:
                    nextfacing = 1
                    nextrow = 5
                    nextcolumn = 13 - column
                else:
                    nextfacing = 2
                    nextrow = 21 - column
                    nextcolumn = 12
        else:
            if facing == 0: # right
                if row <= 50:
                    nextfacing = 2
                    nextrow = 151 - row
                    nextcolumn = 100
                elif row <= 100:
                    nextfacing = 3
                    nextrow = 50
                    nextcolumn = row + 50
                elif row <= 150:
                    nextfacing = 2
                    nextrow = 151 - row
                    nextcolumn = 150
                else:
                    nextfacing = 3
                    nextrow = 150
                    nextcolumn = row - 100
            elif facing == 1: # down
                if column <= 50:
                    nextfacing = 1
                    nextrow = 1
                    nextcolumn = column + 100
                elif column <= 100:
                    nextfacing = 2
                    nextrow = column + 100
                    nextcolumn = 50
                else:
                    nextfacing = 2
                    nextrow = column - 50
                    nextcolumn = 100
            elif facing == 2: # left
                if row <= 50:
                    nextfacing = 0
                    nextrow = 151 - row
                    nextcolumn = 1
                elif row <= 100:
                    nextfacing = 1
                    nextrow = 101
                    nextcolumn = row-50
                elif row <= 150:
                    nextfacing = 0
                    nextrow = 51 - row
                    nextcolumn = 51
                else:
                    nextfacing = 1
                    nextrow = 51
                    nextcolumn = row - 100
            elif facing == 3: # up
                if column <= 50:
                    nextfacing = 0
                    nextrow = column + 50
                    nextcolumn = 51
                elif column <= 100:
                    nextfacing = 0
                    nextrow = column + 100
                    nextcolumn = 1
                else:
                    nextfacing = 3
                    nextrow = 200
                    nextcolumn = column - 100

        if nextfacing == 0: # right
            while board[nextrow-1][nextcolumn-1] == ' ':
                nextcolumn += 1
        elif nextfacing == 1: # down
            while nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                nextrow += 1
        elif nextfacing == 2: # left
            while board[nextrow-1][nextcolumn-1] == ' ':
                nextcolumn -= 1
        elif nextfacing == 3: # up
            while nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                nextrow -= 1
        
        return (nextrow, nextcolumn, nextfacing)

    def move(moves):
        nonlocal row
        nonlocal column
        nonlocal facing
        for i in range(moves):
            if facing == 0: # right
                nextrow = row
                nextcolumn = column + 1
                nextfacing = facing
                if nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                    newstatus = offtheend(nextrow, nextcolumn, facing)
                    nextrow = newstatus[0]
                    nextcolumn = newstatus[1]
                    nextfacing = newstatus[2]
            elif facing == 1: # down
                nextrow = row + 1
                nextcolumn = column
                nextfacing = facing
                if nextrow > len(board) or nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                    newstatus = offtheend(nextrow, nextcolumn, facing)
                    nextrow = newstatus[0]
                    nextcolumn = newstatus[1]
                    nextfacing = newstatus[2]
            elif facing == 2: # left
                nextrow = row
                nextcolumn = column - 1
                nextfacing = facing
                if nextcolumn < 1 or board[nextrow-1][nextcolumn-1] == ' ':
                    newstatus = offtheend(nextrow, nextcolumn, facing)
                    nextrow = newstatus[0]
                    nextcolumn = newstatus[1]
                    nextfacing = newstatus[2]
            elif facing == 3: # up
                nextrow = row - 1
                nextcolumn = column
                nextfacing = facing
                if nextrow < 1 or nextcolumn > len(board[nextrow-1]) or board[nextrow-1][nextcolumn-1] == ' ':
                    newstatus = offtheend(nextrow, nextcolumn, facing)
                    nextrow = newstatus[0]
                    nextcolumn = newstatus[1]
                    nextfacing = newstatus[2]

            if board[nextrow-1][nextcolumn-1] == '.':
                row = nextrow
                column = nextcolumn
                facing = nextfacing
            else:
                break
            #print(row, column, facing)

    def turn(dir):
        nonlocal facing
        fromfacing = facing
        if dir == 'R':
            facing = (facing + 1) % 4
        elif dir == 'L':
            facing = (facing - 1) % 4
        #print('Turn', fromfacing, facing)

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

    #print(row, column, facing)
    result = 1000*row + 4*column + facing

    return result

result = process('d22-p1-data.txt')
#result = process('d22-p1-testdata.txt')

print(result)
