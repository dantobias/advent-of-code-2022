import re

lineexpr = re.compile(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\,\s]+)')

def process(filename, minutes):

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
            result = False
        else:
            dupestr = currplace+'#? -> ([^#]+ )?'+newmove
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
        return result

    def try_valve(minute, valve, valvesopen, path, score, elephant):
        nonlocal maxscore
        if score > maxscore:
            maxscore = score
            print(minute, path, score)
        if minute == minutes:
            if score > 1400 and not elephant:
                try_valve(1, None, 'AA', valvesopen, 'AA', score, True)
            return maxscore
        gonefurther = False
        if flow[valve] > 0 and not valve in valvesopen:
            try_valve(minute+1, valve, valvesopen+[valve], path+'#', score+flow[valve]*(minutes-minute), elephant)
            gonefurther = True
        for t in tunnels[valve]:
            if not_dupe(path, valve, t, minute, valvesopen):
                try_valve(minute+1, t, valvesopen, path+' -> '+t, score, elephant)
                gonefurther = True
        if not gonefurther and not elephant:
            #try_valve(1, 'AA', valvesopen, 'AA', score, True)
            try_valve(3, 'DD', valvesopen, 'AA -> YY -> DD', score, True)
        return maxscore

    def find_path(minute, valve, dest, path):
        nonlocal minlength
        nonlocal minpath
        if valve == dest:
            if minute < minlength:
                minlength = minute
                minpath = path
                #print(minlength, path + ' -> ' + valve)
            return minlength
        if minute == minutes or minute > minlength:
            return minlength
        for t in tunnels[valve]:
            if not_dupe(path, valve, t, minute, []):
                find_path(minute+1, t, dest, path+' -> '+t)
        return minlength

    result = None

    with open(filename) as infile:
        filedata = infile.readlines()

        flow = {}
        tunnels = {}
     
        maxscore = 0
        maxlength = None
        maxpath = ''
        maxvalve = None

        for line in filedata:
            line = line.rstrip()
            cmatch = lineexpr.match(line)
            if cmatch:
                flow[cmatch.group(1)] = int(cmatch.group(2))
                tunnels[cmatch.group(1)] = cmatch.group(3).split(', ')

        flow = {k: v for k, v in sorted(flow.items(), key=lambda item: item[1])}
        for v in flow:
            if flow[v] > 16:
                minlength = 9999
                minpath = ''
                find_path(1, 'AA', v, 'AA')
                score = (minutes-minlength)*flow[v]
                print(v, flow[v], minlength, minpath+'#', score)
                if score > maxscore:
                    maxscore = score
                    maxpath = minpath
                    maxlength = minlength
                    maxvalve = v

        for v in flow:
            if flow[v] > 16:
                minlength = 9999
                minpath = ''
                find_path(maxlength+1, maxvalve, v, maxpath)
                score = maxscore + (minutes-minlength)*flow[v]
                print(v, flow[v], minlength, minpath+'#', score)

    result = None

    #result = try_valve(1, 'AA', [], 'AA', 0, False)
    #result = try_valve(3, 'IR', [], 'AA -> GC -> IR', 0, False)

    # Best result for first run through
    # AA -> GC -> IR# -> JZ -> LY# -> EF -> WL# -> EJ -> CP# -> ZK -> IV -> UC# -> JD -> IZ -> SS# -> SI -> NJ#

    # Do a second run with those valves already open
    #result = try_valve(1, None, 'AA', ['IR', 'LY', 'WL', 'CP', 'UC', 'SS', 'NJ'], 'AA', 1537)

    return result

result = process('d16-p1-data.txt', 26)
#result = process('d16-p1-testdata.txt', 26)
print(result)
