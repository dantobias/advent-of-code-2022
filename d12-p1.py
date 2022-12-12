def validmove(map, currplace, nextplace):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    if nextplace[0] < 0 or nextplace[1] < 0 or nextplace[0] >= len(map[0]) or nextplace[1] >= len(map):
        return False

    currheight = map[currplace[1]][currplace[0]]
    if currheight == 'S':
        currheight = 'a'
    elif currheight == 'E':
        currheight = 'z'
    currheight = alphabet.find(currheight)
    nextheight = map[nextplace[1]][nextplace[0]]
    if nextheight == 'S':
        nextheight = 'a'
    elif nextheight == 'E':
        nextheight = 'z'
    nextheight = alphabet.find(nextheight)

    if nextheight <= currheight + 1:
        return True
    else:
        return False

def process(filename):

    map = []
    startpos = None
    endpos = None
    currplaces = set()
    nextplaces = set()
    beenthere = set()

    with open(filename) as infile:
        filedata = infile.readlines()

        y = 0
        for line in filedata:
            line = line.rstrip()
            map.append(line)
            if line.find('S') >= 0:
                startpos = (line.find('S'), y)
                currplaces.add(startpos)
            if line.find('E') >= 0:
                endpos = (line.find('E'), y)
            y += 1    

    moves = 0
    foundpath = False
    while not foundpath:
        #print(moves, currplaces)
        for place in currplaces:
            #print(moves, place, map[place[1]][place[0]])
            beenthere.add(place)
            if place == endpos:
                foundpath = True
                break
            # up
            if validmove(map, place, (place[0], place[1]-1)) and not (place[0], place[1]-1) in beenthere:
                nextplaces.add((place[0], place[1]-1))
            # down
            if validmove(map, place, (place[0], place[1]+1)) and not (place[0], place[1]+1) in beenthere:
                nextplaces.add((place[0], place[1]+1))
            # left
            if validmove(map, place, (place[0]-1, place[1])) and not (place[0]-1, place[1]) in beenthere:
                nextplaces.add((place[0]-1, place[1]))
            # right
            if validmove(map, place, (place[0]+1, place[1])) and not (place[0]+1, place[1]) in beenthere:
                nextplaces.add((place[0]+1, place[1]))
        currplaces = nextplaces
        nextplaces = set()
        if not foundpath:
            moves += 1

    return moves

result = process('d12-p1-data.txt')
print(result)
