import re

lineexpr = re.compile(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\,\s]+)')

def process(filename):

    cache = {}

    def try_valve(minute, valve, valvesopen):
        if (minute, valve, str(valvesopen)) in cache:
            return cache[(minute, valve, str(valvesopen))]

        #print(minute, valve, valvesopen)
        pressure_released = 0
        for v in valvesopen:
            pressure_released += flow[v]
        if minute == 30:
            #print(minute, valve, pressure_released)
            cache[(minute, valve, str(valvesopen))] = pressure_released
            #print(cache)
            return pressure_released
        else:
            maxval = 0
            if not valve in valvesopen and flow[valve] > 0:
                #print(minute, 'Trying opening', valve, maxval)
                maxval = try_valve(minute+1, valve, valvesopen+[valve])
            for v in tunnels[valve]:
                #print(minute, 'Trying tunnel', v, 'from', valve, maxval)
                testval = try_valve(minute+1, v, valvesopen)
                if testval > maxval:
                    maxval = testval
            #print(minute, valve, pressure_released+maxval)
            cache[(minute, valve, str(valvesopen))] = pressure_released+maxval
            return pressure_released + maxval

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

    result = try_valve(1, 'AA', [])

    return result

result = process('d16-p1-data.txt')
#result = process('d16-p1-testdata.txt')
print(result)
