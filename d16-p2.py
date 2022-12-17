import re

lineexpr = re.compile(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\,\s]+)')

def process(filename, minutes):

    def try_valve(minute, valve, path):
        print(minute, path, flow[valve])
        if minute == minutes:
            return True
        for t in tunnels[valve]:
            try_valve(minute+1, t, path+' -> '+t)
        return True
    result = None

    with open(filename) as infile:
        filedata = infile.readlines()

        flow = {}
        tunnels = {}

        for line in filedata:
            line = line.rstrip()
            cmatch = lineexpr.match(line)
            if cmatch:
                flow[cmatch.group(1)] = int(cmatch.group(2))
                tunnels[cmatch.group(1)] = cmatch.group(3).split(', ')

    result = try_valve(1, 'AA', 'AA')

    return result

result = process('d16-p1-data.txt', 9)
#result = process('d16-p1-testdata.txt', 26)
print(result)
