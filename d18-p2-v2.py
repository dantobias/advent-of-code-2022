def process(filename):

    def set_clear_status(x, y, z):
        nonlocal clear

        if clear[x][y][z] == None:
            if space[x][y][z]:
                clear[x][y][z] = False
                #print(x,y,z,'Occupied: not clear')
            elif x<=1 or x>=maxnum-1 or y<=1 or y>=maxnum-1 or z<=1 or z>=maxnum-1:
                clear[x][y][z] = True
                #print(x,y,z,'At edge: clear')
            elif clear[x-1][y][z] or clear[x][y-1][z] or clear[x][y][z-1] or clear[x+1][y][z] or clear[x][y+1][z] or clear[x][y][z+1]:
                clear[x][y][z] = True
                #print(x,y,z,'Has clear neighbors: clear')
            elif clear[x-1][y][z] != None and clear[x][y-1][z] != None and clear[x][y][z-1] != None and clear[x+1][y][z] != None and clear[x][y+1][z] != None and clear[x][y][z+1]!= None:
                clear[x][y][z] = False
                #print(x,y,z,'Not clear')
            #else:
                #print(x,y,z,'Undecided')

            #print(x, y, z, clear[x][y][z])

    with open(filename) as infile:
        filedata = infile.readlines()

        cubes = []
        maxnum = 0

        for line in filedata:
            line = line.rstrip()
            coords = [int(i) for i in line.split(',')]
            if coords[0] > maxnum:
                maxnum = coords[0]
            if coords[1] > maxnum:
                maxnum = coords[1]
            if coords[2] > maxnum:
                maxnum = coords[2]
            cubes.append(coords)

        space = [[[False for x in range(maxnum+2)] for y in range(maxnum+2)] for z in range(maxnum+2)]
        clear = [[[None for x in range(maxnum+2)] for y in range(maxnum+2)] for z in range(maxnum+2)]

        for c in cubes:
            space[c[0]][c[1]][c[2]] = True

        result = 0

        for x in range(0, maxnum+2):
            for y in range(0, maxnum+2):
                for z in range(0, maxnum+2):
                    set_clear_status(x, y, z)
                    set_clear_status(y, z, x)
                    set_clear_status(z, x, y)
                    set_clear_status(x, z, y)
                    set_clear_status(y, x, z)
                    set_clear_status(z, y, x)
                    set_clear_status(maxnum+1-x, maxnum+1-y, maxnum+1-z)
                    set_clear_status(maxnum+1-y, maxnum+1-z, maxnum+1-x)
                    set_clear_status(maxnum+1-z, maxnum+1-x, maxnum+1-y)
                    set_clear_status(maxnum+1-x, maxnum+1-z, maxnum+1-y)
                    set_clear_status(maxnum+1-y, maxnum+1-x, maxnum+1-z)
                    set_clear_status(maxnum+1-z, maxnum+1-y, maxnum+1-x)

        for x in range(1, len(space)-1):
            for y in range(1, len(space[x])-1):
                for z in range(1, len(space[x][y])-1):
                    if space[x][y][z]:
                        sidecount = 0
                        sidestr = ''
                        if clear[x-1][y][z]:
                            sidecount += 1
                            sidestr += 'x-'
                        if clear[x][y-1][z]:
                            sidecount += 1
                            sidestr += 'y-'
                        if clear[x][y][z-1]:
                            sidecount += 1
                            sidestr += 'z-'
                        if clear[x+1][y][z]:
                            sidecount += 1
                            sidestr += 'x+'
                        if clear[x][y+1][z]:
                            sidecount += 1
                            sidestr += 'y+'
                        if clear[x][y][z+1]:
                            sidecount += 1
                            sidestr += 'z+'
                        #print('S1', x, y, z, sidecount, sidestr)
                        result += sidecount
                    #else:
                        #print('S1', x, y, z, space[x][y][z], clear[x][y][z])

#        for x in range(0, maxnum+2):
#            for y in range(0, maxnum+2):
#                outstr = ''
#                for z in range(0, maxnum+2):
#                    if clear[x][y][z] == None:
#                        outstr += '%'
#                    elif space[x][y][z]:
#                        outstr += '*'
#                    elif clear[x][y][z]:
#                        outstr += ' '
#                    else:
#                        outstr += '.'
#                print(outstr)
#        print()

    #print(space)
    #print(clear)        
    return result

result = process('d18-p1-data.txt')
#result = process('d18-p1-testdata.txt')

print(result)
