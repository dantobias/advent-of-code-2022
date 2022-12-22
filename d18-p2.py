def process(filename):

    def cell_check(x, y, z):
        if x<0 or x>maxnum+1 or y<0 or y>maxnum+1 or z<0 or z>maxnum+1:
            return False
        elif clear[x][y][z] == None:
            if space[x][y][z]:
                return False
            else:
                return True
        else:
            return False

            #print(x, y, z, clear[x][y][z])

    def set_clear_status():
        nonlocal clear
        searchlist = [(0, 0, 0)]
        while (searchlist):
            c = searchlist.pop()
            if c[0] >= 0 and c[1] >= 0 and c[2] >= 0:
                clear[c[0]][c[1]][c[2]] = True
            if cell_check(c[0]-1, c[1], c[2]):
                searchlist.append((c[0]-1, c[1], c[2]))
            if cell_check(c[0], c[1]-1, c[2]):
                searchlist.append((c[0], c[1]-1, c[2]))
            if cell_check(c[0], c[1], c[2]-1):
                searchlist.append((c[0], c[1], c[2]-1))
            if cell_check(c[0]+1, c[1], c[2]):
                searchlist.append((c[0]+1, c[1], c[2]))
            if cell_check(c[0], c[1]+1, c[2]):
                searchlist.append((c[0], c[1]+1, c[2]))
            if cell_check(c[0], c[1], c[2]+1):
                searchlist.append((c[0], c[1], c[2]+1))

    with open(filename) as infile:
        filedata = infile.readlines()

        cubes = []
        maxnum = 0

        for line in filedata:
            line = line.rstrip()
            coords = [int(i)+1 for i in line.split(',')]
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

        set_clear_status()

        result = 0
        cubecount = 0

        cubes1 = {}

        for x in range(1, len(space)-1):
            for y in range(1, len(space[x])-1):
                for z in range(1, len(space[x][y])-1):
                    if space[x][y][z]:
                        cubecount += 1
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
                        cubes1[(x, y, z)] = sidecount
                    #else:
                        #print('S1', x, y, z, space[x][y][z], clear[x][y][z])

        #print(result, cubecount)

        cubes2 = {}

        result = 0
        cubecount = 0
        for c in cubes:
            cubecount += 1
            sidecount = 0
            sidestr = ''
            if clear[c[0]-1][c[1]][c[2]]:
                sidecount += 1
                sidestr += 'x-'
            if clear[c[0]][c[1]-1][c[2]]:
                sidecount += 1
                sidestr += 'y-'
            if clear[c[0]][c[1]][c[2]-1]:
                sidecount += 1
                sidestr += 'z-'
            if clear[c[0]+1][c[1]][c[2]]:
                sidecount += 1
                sidestr += 'x+'
            if clear[c[0]][c[1]+1][c[2]]:
                sidecount += 1
                sidestr += 'y+'
            if clear[c[0]][c[1]][c[2]+1]:
                sidecount += 1
                sidestr += 'z+'
            #print('S2', c[0], c[1], c[2], sidecount, sidestr)
            result += sidecount
            cubes2[(c[0], c[1], c[2])] = sidecount

        #print(result, cubecount)

        #for c in cubes1:
        #    if not c in cubes2:
        #        print ("Missing from cubes2:", c, cubes1[c])

        #for c in cubes2:
        #    if not c in cubes1:
        #        print ("Missing from cubes1:", c, cubes2[c])

        #for x in range(0, maxnum+2):
        #    for y in range(0, maxnum+2):
        #        outstr = ''
        #        for z in range(0, maxnum+2):
        #            if space[x][y][z]:
        #                outstr += '*'
        #            elif clear[x][y][z] == None:
        #                outstr += '%'
        #            elif clear[x][y][z]:
        #                outstr += ' '
        #            else:
        #                outstr += '.'
        #        print(outstr)
        #print()

    #print(space)
    #print(clear)        
    return result

result = process('d18-p1-data.txt')
#result = process('d18-p1-testdata.txt')

print(result)
