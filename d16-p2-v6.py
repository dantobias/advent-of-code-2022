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

    def check_score(step, minute, valve, valvesopen):
        #print('Checking', step, minute, valve, valvesopen)
        if step >= 3 or minute >= minutes-1:
            if valve in valvesopen:
                return 0
            else:
                return flow[valve]*(minutes-minute)
        else:
            maxscore = 0
            maxvalve = None
            for v in tunnels[valve]:
                if not v in valvesopen:
                    score = check_score(step+1, minute+1, v, valvesopen)
                    if score > maxscore:
                        maxscore = score
                        maxvalve = v
            if maxvalve != None:
                if valve in valvesopen:
                    return flow[valve]*(minutes-minute) + maxscore
                else:
                    return maxscore
            else:
                if valve in valvesopen:
                    return flow[valve]*(minutes-minute)
                else:
                    return 0

    def try_valve(minute, valve, valvesopen, path, score, elephant):
        nonlocal maxscore
        nonlocal lastvalvesopen
        if score > maxscore:
            maxscore = score
            print(minute, path, score, '*')
        if minute == minutes:
            if not elephant:
                if valvesopen != lastvalvesopen:
                    try_valve(1, 'AA', valvesopen, 'AA', score, True)
                    print(minute, path, score, maxscore)
                    lastvalvesopen = valvesopen
            #else:
            #    print('E', minute, path, score, maxscore)
            return maxscore
        gonefurther = False
        if flow[valve] > 0 and not valve in valvesopen:
            try_valve(minute+1, valve, valvesopen+[valve], path+'#', score+flow[valve]*(minutes-minute), elephant)
            gonefurther = True
        scores = {}
        for t in tunnels[valve]:
            if not_dupe(path, valve, t, minute, valvesopen):
                scores[t] = None
        if len(t) > 1:
            for t in scores:
                scores[t] = check_score(1, minute+1, t, valvesopen)
            scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
        for t in scores:
            try_valve(minute+1, t, valvesopen, path+' -> '+t, score, elephant)
            gonefurther = True
        if not gonefurther and not elephant:
            if lastvalvesopen != valvesopen:
                try_valve(1, 'AA', valvesopen, 'AA', score, True)
                #try_valve(3, 'DD', valvesopen, 'AA -> YY -> DD', score, True)
                print(minute, path, score, maxscore)
                lastvalvesopen = valvesopen
        #elif not gonefurther:
        #    print('E', minute, path, score, maxscore)
        return maxscore

    result = None

    with open(filename) as infile:
        filedata = infile.readlines()

        flow = {}
        tunnels = {}
     
        maxscore = 0

        for line in filedata:
            line = line.rstrip()
            cmatch = lineexpr.match(line)
            if cmatch:
                flow[cmatch.group(1)] = int(cmatch.group(2))
                tunnels[cmatch.group(1)] = cmatch.group(3).split(', ')
    
    result = None

    lastvalvesopen = None
    result = try_valve(1, 'AA', [], 'AA', 0, False)
    #result = try_valve(3, 'IR', [], 'AA -> GC -> IR', 0, False)

    # Best result for first run through
    # AA -> GC -> IR# -> JZ -> LY# -> EF -> WL# -> EJ -> CP# -> ZK -> IV -> UC# -> JD -> IZ -> SS# -> SI -> NJ#

    # Do a second run with those valves already open
    #result = try_valve(1, None, 'AA', ['IR', 'LY', 'WL', 'CP', 'UC', 'SS', 'NJ'], 'AA', 1537)

    return result

result = process('d16-p1-data.txt', 26)
#result = process('d16-p1-testdata.txt', 26)
print(result)
