import re

lineexpr = re.compile(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\,\s]+)')

def process(filename, minutes):

    cache = {}
    ecache = {}

    def useless_move(minute, newmove, valvesopen):
        if minute >= minutes:
            return True
        elif minute == minutes - 1 and newmove in valvesopen:
            return True
        elif minute == minutes - 2:
            if newmove in valvesopen:
                for t in tunnels[newmove]:
                    if not t in valvesopen:
                        return False
                return True
        elif minute == minutes - 3:
            if newmove in valvesopen:
                for t in tunnels[newmove]:
                    if t in valvesopen:
                        for u in tunnels[t]:
                            if not u in valvesopen:
                                return False
                return True
        return False

    def not_dupe(path, currplace, newmove, minute, valvesopen):
        result = True
        if useless_move(minute, newmove, valvesopen):
            result = False
        elif path.find(currplace+" -> "+newmove) != -1:
            #print('found')
            result = False
        else:
            dupestr = currplace+'#? -> ([^#]+ )?'+newmove
            #print(dupestr)
            dupeexpr = re.compile(dupestr)
            if dupeexpr.match(path):
                result = False
            else:
                places = path.split(' -> ')
                foundplace = False
                for place in places:
                    if place == newmove or place == newmove+'#':
                        foundplace = True
                    elif place[-1] == '#':
                        foundplace = False
                if foundplace == True:
                    result = False

        #print('not_dupe:', path, currplace, newmove, result)
        return result

    def try_elephant(minute, valve, valvesopen, elephantvalvesopen, path, prevflow):
        #print('E', minute, path)

        valvesopen.sort()
        elephantvalvesopen.sort()
        if (minute, valve, str(valvesopen), str(elephantvalvesopen)) in ecache:
            #print(minute, 'E', valve, valvesopen, elephantvalvesopen, 'C')
            return ecache[(minute, valve, str(valvesopen), str(elephantvalvesopen))]

        #print(minute, 'E', valve, valvesopen, elephantvalvesopen)

        pressure_released = 0
        for v in elephantvalvesopen:
            pressure_released += flow[v]

        valvesleft = 0
        for v in flow:
            if flow[v] > 0 and not v in valvesopen:
                valvesleft += 1

        if valvesleft == 0:
            for v in elephantvalvesopen:
                pressure_released += flow[v] * (26-minute)
            ecache[(minute, valve, str(valvesopen), str(elephantvalvesopen))] = pressure_released
            return pressure_released
        elif minute == minutes:
            ecache[(minute, valve, str(valvesopen), str(elephantvalvesopen))] = pressure_released
            return pressure_released
        else:
            maxval = 0
            for v in elephantvalvesopen:
                maxval += flow[v] * (26-minute)
            if not valve in valvesopen and flow[valve] > 0:
                #print(minute, 'Trying opening', valve, maxval)
                testval = try_elephant(minute+1, valve, valvesopen+[valve], elephantvalvesopen+[valve], path+'#', prevflow+pressure_released)
                if testval > maxval:
                    maxval = testval
            for v in tunnels[valve]:
                if not_dupe(path, valve, v, minute+1, valvesopen):
                    #print(minute, 'Trying tunnel', v, 'from', valve, maxval)
                    testval = try_elephant(minute+1, v, valvesopen, elephantvalvesopen, path+' -> '+v, prevflow+pressure_released)
                    if testval > maxval:
                        maxval = testval
            #print(minute, valve, pressure_released+maxval)
            #ecache[(minute, valve, str(valvesopen), str(elephantvalvesopen))] = pressure_released+maxval
            return pressure_released + maxval

    def try_valve(minute, valve, valvesopen, path, prevflow):
        #print(minute, path)

        valvesopen.sort()
        if (minute, valve, str(valvesopen)) in cache:
            #print(minute, valve, valvesopen, 'C')
            return cache[(minute, valve, str(valvesopen))]

        #print(minute, valve, valvesopen)

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
            #cache[(minute, valve, str(valvesopen))] = pressure_released
            #print('V0:', pressure_released)
            print(prevflow + pressure_released, path)
            return pressure_released
        elif minute == minutes:
            elephant_total = try_elephant(1, 'AA', valvesopen, [], 'AA', prevflow+pressure_released)
            #cache[(minute, valve, str(valvesopen))] = pressure_released + elephant_total
            #print('M:', pressure_released + elephant_total)
            print(prevflow + pressure_released + elephant_total, path)
            return pressure_released + elephant_total
        else:
            maxval = 0
            for v in valvesopen:
                maxval += flow[v] * (26-minute)
            termval = maxval
            if not valve in valvesopen and flow[valve] > 0:
                #print(minute, 'Trying opening', valve, maxval)
                testval = try_valve(minute+1, valve, valvesopen+[valve], path+'#', prevflow+pressure_released)
                if testval > maxval:
                    maxval = testval
            for v in tunnels[valve]:
                if not_dupe(path, valve, v, minute+1, valvesopen):
                    #print(minute, 'Trying tunnel', v, 'from', valve, maxval)
                    testval = try_valve(minute+1, v, valvesopen, path+' -> '+v, prevflow+pressure_released)
                    if testval > maxval:
                        maxval = testval

            if maxval == termval:
                elephant_total = try_elephant(1, 'AA', valvesopen, [], 'AA', prevflow+pressure_released+termval)
                print(prevflow + pressure_released + maxval + elephant_total, path)
            else:
                elephant_total = 0

            #print(minute, valve, pressure_released+maxval)
            #print('T:", pressure_released+maxval+elephant_total)
            #cache[(minute, valve, str(valvesopen))] = pressure_released+maxval+elephant_total
            return pressure_released + maxval + elephant_total

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

    result = try_valve(1, 'AA', [], 'AA', 0)

    return result

result = process('d16-p1-data.txt', 26)
#result = process('d16-p1-testdata.txt', 26)
print(result)
