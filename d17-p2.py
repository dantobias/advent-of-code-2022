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

    lastno = 0
    lasttop = 0

    rockmod = []

    for rockno in range(rocks):
        x = 3
        y = 4 + toprock
        stopped = False
        rocktype = rock[rockno % len(rock)]
        xx = x + len(rocktype[0]) - 1
        yy = y + len(rocktype) - 1

        while len(chamber)<yy+1:
            chamber.append('|.......|')

        #pprint(rocktype)
        #print('Starting: x', x, xx, 'y:', y, yy)

        while not stopped:
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
                    #print('Moving Right: x', x, xx, 'y:', y, yy)
            elif direction == '<':
                nomove = False
                for i in range(len(rocktype)):
                    for j in range(len(rocktype[i])):
                        if rocktype[i][j] != '.' and chamber[yy-i][x+j-1] != '.':
                            nomove = True
                if not nomove:
                    x -= 1
                    xx -= 1
                    #print('Moving Left: x', x, xx, 'y:', y, yy)

            for i in range(len(rocktype)):
                for j in range(len(rocktype[i])):
                    if rocktype[i][j] != '.' and chamber[yy-i-1][x+j] != '.':
                        stopped = True
            if not stopped:
                y -= 1
                yy -= 1
                #print('Falling: x', x, xx, 'y:', y, yy)
            else:
                if yy > toprock:
                    toprock = yy

                if rockno >= 1738 and rockno <= 3467:
                    index = (rockno-1738)%1730
                    topindex = (toprock-2675)%2644
                    #print(rockno+1, index, toprock, topindex)
                    rockmod.append(topindex)

                if rockno > 3467:
                    index = (rockno-1738)%1730
                    topindex = rockmod[index]
                    calcrock = 2675+int((rockno-1738)/1730)*2644+topindex
                    #print(rockno+1, index, toprock, topindex, calcrock)

                #if turn%len(pattern) < 10:
                #    print(rockno+1, rockno-lastno, toprock, toprock-lasttop, int((rockno+1-1739)/1730), (rockno+1-1739)%1730, turn%len(pattern), rockno%len(rocktype))
                #    lastno = rockno
                #    lasttop = toprock

                for i in range(len(rocktype)):
                        newstring = chamber[yy-i][0:x]
                        for j in range(len(rocktype[i])):
                            if rocktype[i][j] == '.':
                                newstring += chamber[yy-i][x+j]
                            else:
                                newstring += rocktype[i][j]
                        newstring += chamber[yy-i][xx+1:]
                        chamber[yy-i] = newstring

                #pprint(chamber)

            turn += 1

    rockno = 1000000000000 - 1
    index = (rockno-1738)%1730
    #print(rockno, index, rockmod[index])
    result = 2675+int((rockno-1738)/1730)*2644+rockmod[index]
    return result

result = process('d17-p1-data.txt', 5000)
#result = process('d17-p1-testdata.txt', 5000)

print(result)
