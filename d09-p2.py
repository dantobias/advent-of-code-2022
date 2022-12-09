def process(filename, knots):
    result = None
    with open(filename) as infile:
        filedata = infile.readlines()

        knotpos = []
        for i in range(knots):
            knotpos.append((0, 0))
        positions = {}

        for line in filedata:
            line = line.rstrip()
            move = line.split()
            for i in range(int(move[1])):
                if move[0] == 'L':
                    knotpos[0] = (knotpos[0][0]-1, knotpos[0][1])
                elif move[0] == 'R':
                    knotpos[0] = (knotpos[0][0]+1, knotpos[0][1])
                elif move[0] == 'U':
                    knotpos[0] = (knotpos[0][0], knotpos[0][1]-1)
                elif move[0] == 'D':
                    knotpos[0] = (knotpos[0][0], knotpos[0][1]+1)

                for j in range(1, knots):
                    if abs(knotpos[j-1][0] - knotpos[j][0]) > 1 or abs(knotpos[j-1][1] - knotpos[j][1]) > 1:
                        xdir = knotpos[j-1][0] - knotpos[j][0]
                        if xdir > 1:
                            xdir = 1
                        elif xdir < -1:
                            xdir = -1
                        ydir = knotpos[j-1][1] - knotpos[j][1]
                        if ydir > 1:
                            ydir = 1
                        elif ydir < -1:
                            ydir = -1
                        knotpos[j] = (knotpos[j][0]+xdir, knotpos[j][1]+ydir)

                positions[knotpos[knots-1]] = True

            #print(move, knotpos[0], knotpos[knots-1])
            result = len(positions)
    return result

result = process('d09-p1-data.txt', 10)
print(result)
