import re

lineexpr = re.compile(r'Sensor at x=([0-9-]+), y=([0-9-]+): closest beacon is at x=([0-9-]+), y=([0-9-]+)')

def process(filename, targetrow):

    with open(filename) as infile:
        filedata = infile.readlines()

        target_ranges = []

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

                if yrangelow <= targetrow and yrangehigh >= targetrow:
                    targetdiff = abs(sensory - targetrow)
                    rowdistance = distance - targetdiff
                    xrangelow = sensorx - rowdistance
                    xrangehigh = sensorx + rowdistance
                    target_ranges.append((xrangelow, xrangehigh))

    target_ranges.sort()
    #print(target_ranges)

    result = 0
    lastrange = None
    for range in target_ranges:
        if lastrange == None or range[0] > lastrange[1]:
            newcells = range[1]-range[0]
            lastrange = range
            #print(newcells, range, lastrange)
        elif range[1] > lastrange[1]:
            newcells = range[1] - lastrange[1]
            lastrange = range
            #print(newcells, range, lastrange)
        else:
            newcells = 0
            #print(newcells, range, lastrange)
        result += newcells

    return result

result = process('d15-p1-data.txt', 2000000)
print(result)
