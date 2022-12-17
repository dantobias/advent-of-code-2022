import re
from pprint import pprint

def process(filename, rocks):
    with open(filename) as infile:
        pattern = infile.readline().rstrip()

    rock = [None, None, None, None, None]
    rock[0] = ['####']
    rock[1] = ['.#.', '###', '.#.']
    rock[2] = ['..#', '..#', '###']
    rock[3] = ['#', '#', '#', '#']
    rock[4] = ['##', '##']

    toprock = 0
    turn = 0
    chamber = ['+-------+']

    for rockno in range(rocks):
        x = 3
        y = 4 + toprock
        stopped = False
        rocktype = rock[rockno % len(rock)]
        xx = x + len(rocktype[0]) - 1
        yy = y + len(rocktype) - 1

        while len(chamber)<yy+1:
            chamber.append('|.......|')

        while not stopped:
            #print('Start', x, xx, y, yy)
            direction = pattern[turn % len(pattern)]
            if direction == '>':
                nomove = False
                for i in range(len(rocktype)):
                    for j in range(len(rocktype[i])):
                        if rocktype[i][j] != '.' and chamber[yy-i][x+j+1] != '.':
                            nomove = True
                if not nomove:
                    x += 1
                    xx += 1
            elif direction == '<':
                nomove = False
                for i in range(len(rocktype)):
                    for j in range(len(rocktype[i])):
                        if rocktype[i][j] != '.' and chamber[yy-i][x+j-1] != '.':
                            nomove = True
                if not nomove:
                    x -= 1
                    xx -= 1

            #print('Moved', x, xx, y, yy)

            for i in range(len(rocktype)):
                for j in range(len(rocktype[i])):
                    if rocktype[i][j] != '.' and chamber[yy-i-1][x+j] != '.':
                        stopped = True
            if not stopped:
                y -= 1
                yy -= 1
                #print('Falling', x, xx, y, yy)
            else:
                if yy > toprock:
                    toprock = yy

                #print('Chamber Pre:')
                #pprint(chamber)
                #print('Top Rock', toprock)
                for i in range(len(rocktype)):
                    chamber[yy-i] = chamber[yy-i][0:x] + rocktype[i] + chamber[yy-i][xx+1:]
                #print('Chamber Post:')
                #pprint(chamber)
                #print('End')

            turn += 1
 
    #pprint(chamber)

    result = toprock
    return result

result = process('d17-p1-data.txt', 2022)
#result = process('d17-p1-testdata.txt', 2022)
print(result)
