import re

lineexpr = re.compile(r'Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)')

def process(filename, rangemin, rangemax):

    with open(filename) as infile:
        filedata = infile.readlines()

        data = []

        for line in filedata:
            line = line.rstrip()
            cmatch = lineexpr.match(line)

            if cmatch:
                sensorx = int(cmatch.group(1))
                sensory = int(cmatch.group(2))
                beaconx = int(cmatch.group(3))
                beacony = int(cmatch.group(4))

                distance = abs(sensorx-beaconx) + abs(sensory-beacony)
                yrangelow = sensory - distance
                yrangehigh = sensory + distance

                data.append((sensorx, sensory, distance))

    #target_ranges.sort()
    #print(target_ranges)


    possible_value = None

    for i in range(rangemin, rangemax+1):
    #for i in range(3349056, 3349057):
        target_ranges = []

        for item in data:
            targetdiff = abs(item[1] - i)
            rowdistance = item[2] - targetdiff
            xrangelow = item[0] - rowdistance
            xrangehigh = item[0] + rowdistance

            target_ranges.append((xrangelow, xrangehigh))

        target_ranges.sort()

        lastrange = None
        highx = rangemin
        for xrange in target_ranges:
            #print('R', xrange)
            if xrange[0] < rangemin:
                if xrange[1] >= rangemin:
                    xrange = (rangemin, xrange[1])
                else:
                    xrange = None
            if xrange[0] > rangemax:
                xrange = None
            elif xrange[1] > rangemax:
                xrange = (xrange[0], rangemax)

            if xrange != None:
                if xrange[1] > highx:
                    highx = xrange[1]
                if lastrange == None:
                    if xrange[0] > rangemin:
                        possible_value = (rangemin, i)
                        #print(possible_value)
                    newcells = xrange[1]-xrange[0]
                    lastrange = xrange
                    #print(newcells, xrange, lastrange)
                elif xrange[0] > lastrange[1]:
                    if xrange[0] > lastrange[1]+1:
                        possible_value = (lastrange[1]+1, i)
                        #print(possible_value)
                    newcells = xrange[1]-xrange[0]
                    lastrange = xrange
                    #print(newcells, xrange, lastrange)
                elif xrange[1] > lastrange[1]:
                    newcells = xrange[1] - lastrange[1]
                    lastrange = xrange
                    #print(newcells, xrange, lastrange)
                else:
                    newcells = 0
                    #print(newcells, xrange, lastrange)
            else:
                newcells = 0

        if highx < rangemax:
            possible_value = (rangemax, i)
            #print(possible_value)

        if possible_value:
            #print(possible_value)
            return possible_value[0]*4000000 + possible_value[1]

result = process('d15-p1-data.txt', 0, 4000000)
print(result)
