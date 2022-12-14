import re

lineexpr = re.compile(r'\b([0-9]+)\,([0-9]+)\b')

def process(filename):

    def spaceopen(t):
        if t in location:
            return False
        else:
            return True

    with open(filename) as infile:
        filedata = infile.readlines()

        location = {}
        bottom = 0

        for line in filedata:
            line = line.rstrip()
            findresult = re.findall(lineexpr, line)
            findresult = [(int(t[0]), int(t[1])) for t in findresult]
            currloc = None
            for t in findresult:
                if t[1] > bottom:
                    bottom = t[1]
                if currloc != None:
                    if t[0] == currloc[0]:
                        if t[1] > currloc[1]:
                            for i in range(currloc[1], t[1]):
                                location[(currloc[0], i)] = '#'
                                #print((currloc[0], i))                            
                        else:
                            for i in range(currloc[1], t[1], -1):
                                location[(currloc[0], i)] = '#'
                                #print((currloc[0], i))                            
                    else:
                        if t[0] > currloc[0]:
                            for i in range(currloc[0], t[0]):
                                location[(i, currloc[1])] = '#'
                                #print((i, currloc[1]))
                        else:
                            for i in range(currloc[0], t[0], -1):
                                location[(i, currloc[1])] = '#'
                                #print((i, currloc[1]))

                currloc = t
                location[t] = '#'
                #print(t)
                #print()

    sandgrain = 0

    breakout = False
    while not breakout:
        sandgrain += 1        
        pos = (500, 0)
        movable = True
        while movable and pos[1] <= bottom:
            if spaceopen((pos[0], pos[1]+1)):
                pos = (pos[0], pos[1]+1)
            elif spaceopen((pos[0]-1, pos[1]+1)):
                pos = (pos[0]-1, pos[1]+1)
            elif spaceopen((pos[0]+1, pos[1]+1)):
                pos = (pos[0]+1, pos[1]+1)
            else:
                location[pos] = 'o'
                movable = False
        if movable:
            breakout = True
        #print(sandgrain, pos, movable)

    #print(location)
    return sandgrain - 1

result = process('d14-p1-data.txt')
print(result)
