def process(filename):

    def clearcell(x, y, z):
        if clear[x][y][z] == '*':
            return False
        elif clear[x][y][z] != None:
            return clear[x][y][z]

        clear[x][y][z] = '*' # Temporary marker to prevent infinite recursion

        if space[x][y][z]:
            clear[x][y][z] = False
            return False
        elif x<=1 or x>=maxnum or y<=1 or y>=maxnum or z<=1 or z>=maxnum:
            clear[x][y][z] = True
            return True
        else:
            #print(x, y, z)
            if clearcell(x-1, y, z):
                clear[x][y][z] = True
                return True
            if clearcell(x, y-1, z):
                clear[x][y][z] = True
                return True
            if clearcell(x, y, z-1):
               clear[x][y][z] = True
               return True
            if clearcell(x+1, y, z):
                clear[x][y][z] = True
                return True
            if clearcell(x, y+1, z):
                clear[x][y][z] = True
                return True
            if clearcell(x, y, z+1):
                clear[x][y][z] = True
                return True

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
        for c in cubes:
            sides = 6
            if space[c[0]-1][c[1]][c[2]]:
                sides -= 1
            if space[c[0]][c[1]-1][c[2]]:
                sides -= 1
            if space[c[0]][c[1]][c[2]-1]:
                sides -= 1
            if space[c[0]+1][c[1]][c[2]]:
                sides -= 1
            if space[c[0]][c[1]+1][c[2]]:
                sides -= 1
            if space[c[0]][c[1]][c[2]+1]:
                sides -= 1
            result += sides

        for x in range(1, len(space)-1):
            for y in range(1, len(space[x])-1):
                for z in range(1, len(space[x][y])-1):
                    if not space[x][y][z]:
                        sides = 0
                        if space[x-1][y][z]:
                            sides += 1
                        if space[x][y-1][z]:
                            sides += 1
                        if space[x][y][z-1]:
                            sides += 1
                        if space[x+1][y][z]:
                            sides += 1
                        if space[x][y+1][z]:
                            sides += 1
                        if space[x][y][z+1]:
                            sides += 1

                        if not clearcell(x, y, z):
                            result -= sides
                        
    return result

result = process('d18-p1-data.txt')
#result = process('d18-p1-testdata.txt')

print(result)
