import re

lineexpr = re.compile(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\,\s]+)')

def process(filename):

    cache = {}

    def try_valve(minute, yourvalve, elephantvalve, valvesopen):
        if (minute, yourvalve, elephantvalve, str(valvesopen)) in cache:
            return cache[(minute, yourvalve, elephantvalve, str(valvesopen))]

        #print(minute, yourvalve, elephantvalve, valvesopen)
        pressure_released = 0
        for v in valvesopen:
            pressure_released += flow[v]

        valvesleft = 0
        for v in flow:
            if flow[v] > 0 and not v in valvesopen:
                valvesleft += 1

        if valvesleft == 0:
            for v in valvesopen:
                pressure_released += flow[v] * (26-minute)
            #cache[(minute, yourvalve, elephantvalve, str(valvesopen))] = pressure_released
            return pressure_released

        if minute == 26:
            #print(minute, yourvalve, elephantvalve, pressure_released)
            #cache[(minute, yourvalve, elephantvalve, str(valvesopen))] = pressure_released
            #print(cache)
            return pressure_released
        else:
            maxval = 0
            if not yourvalve in valvesopen and flow[yourvalve] > 0:
                if not elephantvalve in valvesopen and flow[elephantvalve] > 0:
                    maxval = try_valve(minute+1, yourvalve, elephantvalve, valvesopen+[yourvalve, elephantvalve])

                    for v in tunnels[yourvalve]:
                        testval = try_valve(minute+1, v, elephantvalve, valvesopen+[elephantvalve])
                        if testval > maxval:
                            maxval = testval

                    for w in tunnels[elephantvalve]:
                        testval = try_valve(minute+1, yourvalve, w, valvesopen+[yourvalve])
                        if testval > maxval:
                            maxval = testval

                else:
                    for w in tunnels[elephantvalve]:
                        testval = try_valve(minute+1, yourvalve, w, valvesopen+[yourvalve])
                        if testval > maxval:
                            maxval = testval
            elif not elephantvalve in valvesopen and flow[elephantvalve] > 0:
                for v in tunnels[yourvalve]:
                    testval = try_valve(minute+1, v, elephantvalve, valvesopen+[elephantvalve])
                    if testval > maxval:
                        maxval = testval

            for v in tunnels[yourvalve]:
                for w in tunnels[elephantvalve]:
                    testval = try_valve(minute+1, v, w, valvesopen)
                    if testval > maxval:
                        maxval = testval

            #print(minute, yourvalve, elephantvalve, pressure_released+maxval)
            #cache[(minute, yourvalve, elephantvalve, str(valvesopen))] = pressure_released+maxval
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

    result = try_valve(1, 'AA', 'AA', [])

    return result

#result = process('d16-p1-data.txt')
result = process('d16-p1-testdata.txt')
print(result)
