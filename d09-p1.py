def process(filename):
    result = None
    with open(filename) as infile:
        filedata = infile.readlines()

        headpos = (0, 0)
        tailpos = (0, 0)
        positions = {}

        for line in filedata:
            line = line.rstrip()
            move = line.split()
            for i in range(int(move[1])):
                if move[0] == 'L':
                    headpos = (headpos[0]-1, headpos[1])
                elif move[0] == 'R':
                    headpos = (headpos[0]+1, headpos[1])
                elif move[0] == 'U':
                    headpos = (headpos[0], headpos[1]-1)
                elif move[0] == 'D':
                    headpos = (headpos[0], headpos[1]+1)

                if abs(tailpos[0] - headpos[0]) > 1 or abs(tailpos[1] - headpos[1]) > 1:
                    xdir = headpos[0] - tailpos[0]
                    if xdir > 1:
                        xdir = 1
                    elif xdir < -1:
                        xdir = -1
                    ydir = headpos[1] - tailpos[1]
                    if ydir > 1:
                        ydir = 1
                    elif ydir < -1:
                        ydir = -1
                    tailpos = (tailpos[0]+xdir, tailpos[1]+ydir)

                positions[tailpos] = True

            #print(move, headpos, tailpos)
            result = len(positions)
    return result

result = process('d09-p1-data.txt')
print(result)
