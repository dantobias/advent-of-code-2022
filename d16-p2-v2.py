import re

lineexpr = re.compile(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\,\s]+)')

def process(filename, minutes):

    cache = {}

    def useless_move(minute, newmove, valvesopen):
        if minute == minutes - 1 and newmove in valvesopen:
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
                    if not t in valvesopen:
                        for u in tunnels[t]:
                            if not u in valvesopen:
                                return False
                return True
        elif minute == minutes - 4:
            if newmove in valvesopen:
                for t in tunnels[newmove]:
                    if not t in valvesopen:
                        for u in tunnels[t]:
                            if not u in valvesopen:
                                for v in tunnels[u]:
                                    if not v in valvesopen:
                                        return False
                return True
        return False

    def not_dupe(path, otherpath, currplace, newmove, minute, valvesopen):
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

                places = otherpath.split(' -> ')
                foundplace = False
                for place in places:
                    if place == newmove or place == newmove+'#':
                        foundplace = True
                if foundplace == True:
                    result = False

        #print('not_dupe:', path, currplace, newmove, result)
        return result

    def try_valve(minute, yourvalve, elephantvalve, valvesopen, yourpath, elephantpath):

        positions = [yourvalve, elephantvalve]
        positions.sort()

        #print(minute, yourpath, '\n', elephantpath)

        if (minute, str(positions), str(valvesopen)) in cache:
            #print(minute, yourvalve, elephantvalve, valvesopen, cache[(minute, str(positions), str(valvesopen))], 'C')
            return cache[(minute, str(positions), str(valvesopen))]

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
            valvesopen.sort()
            cache[(minute, str(positions), str(valvesopen))] = pressure_released
            return pressure_released

        if minute == minutes:
            #print(minute, yourvalve, elephantvalve, pressure_released)
            valvesopen.sort()
            cache[(minute, str(positions), str(valvesopen))] = pressure_released
            #print(cache)
            return pressure_released
        else:
            maxval = 0
            for v in valvesopen:
                maxval += flow[v] * (26-minute)

            if not yourvalve in valvesopen and flow[yourvalve] > 0:
                if yourvalve != elephantvalve and not elephantvalve in valvesopen and flow[elephantvalve] > 0:
                    testval = try_valve(minute+1, yourvalve, elephantvalve, valvesopen+[yourvalve, elephantvalve], yourpath+'#', elephantpath+'#')
                    if testval > maxval:
                        maxval = testval

                    for v in tunnels[yourvalve]:
                        if not_dupe(yourpath, elephantpath, yourvalve, v, minute, valvesopen):
                            testval = try_valve(minute+1, v, elephantvalve, valvesopen+[elephantvalve], yourpath+' -> '+v, elephantpath+'#')
                            if testval > maxval:
                                maxval = testval

                    for w in tunnels[elephantvalve]:
                        if not_dupe(elephantpath, yourpath, elephantvalve, w, minute, valvesopen):
                            testval = try_valve(minute+1, yourvalve, w, valvesopen+[yourvalve], yourpath+'#', elephantpath+' -> '+w)
                            if testval > maxval:
                                maxval = testval

                else:
                    for w in tunnels[elephantvalve]:
                        if not_dupe(elephantpath, yourpath, elephantvalve, w, minute, valvesopen):
                            testval = try_valve(minute+1, yourvalve, w, valvesopen+[yourvalve], yourpath+'#', elephantpath+' -> '+w)
                            if testval > maxval:
                                maxval = testval
            elif not elephantvalve in valvesopen and flow[elephantvalve] > 0:
                for v in tunnels[yourvalve]:
                    if not_dupe(yourpath, elephantpath, yourvalve, v, minute, valvesopen):
                        testval = try_valve(minute+1, v, elephantvalve, valvesopen+[elephantvalve], yourpath+' -> '+v, elephantpath+'#')
                        if testval > maxval:
                            maxval = testval

            for v in tunnels[yourvalve]:
                if not_dupe(yourpath, elephantpath, yourvalve, v, minute, valvesopen):
                    for w in tunnels[elephantvalve]:
                        if not_dupe(elephantpath, yourpath, elephantvalve, w, minute, valvesopen):
                            testval = try_valve(minute+1, v, w, valvesopen, yourpath+' -> '+v, elephantpath+' -> '+w)
                            if testval > maxval:
                                maxval = testval

            #print(minute, yourvalve, elephantvalve, pressure_released+maxval)
            valvesopen.sort()
            cache[(minute, str(positions), str(valvesopen))] = pressure_released+maxval
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

    result = try_valve(1, 'AA', 'AA', [], 'AA', 'AA')

    return result

result = process('d16-p1-data.txt', 26)
#result = process('d16-p1-testdata.txt', 26)
print(result)
