import re

lineexpr = re.compile(r'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\,\s]+)')

def process(filename, minutes):

    def find_distances(starting_point):
        distance = {}
        queue = []

        distance[starting_point] = 0
        queue.append(starting_point)

        while queue:
            curr = queue.pop(0)
            for t in tunnels[curr]:
                if not t in distance:
                    distance[t] = distance[curr] + 1
                    queue.append(t)
        
        return distance

    def find_values(starting_point, minute, openvalves):
        value = {}
        distance = find_distances(starting_point)
        for v in distance:
            if flow[v] > 0 and not v in openvalves:
                if minutes - (distance[v] + minute) > 0:
                    value[v] = ((minutes - (distance[v] + minute)) * flow[v], distance[v])
        return sorted(value.items(), key=lambda item: -item[1][0])

    def find_total_value(starting_point1, starting_point2, wait1, wait2, minute, openvalves, score):
        nonlocal hiscore
        if score > hiscore:
            hiscore = score
            print(minute, starting_point1, starting_point2, wait1, wait2, score, openvalves)
        maxresult = score
        if minute < minutes:
            if wait1 <= 0:
                values1 = find_values(starting_point1, minute, openvalves)
            else:
                values1 = []
            if wait2 <= 0:
                values2 = find_values(starting_point2, minute, openvalves)
            else:
                values2 = []
            doneany = False
            if not values1:
                wcount = 0
                for w in values2:
                    wcount += 1
                    result = find_total_value(starting_point1, w[0], wait1-1, w[1][1], minute+1, openvalves + [w[0]], score + w[1][0])
                    doneany = True
                    if result > maxresult:
                        maxresult = result
                    if wcount > maxfind and minute > 2 and minute < 20:
                        break
            elif not values2:
                vcount = 0
                for v in values1:
                    vcount += 1
                    result = find_total_value(v[0], starting_point2, v[1][1], wait2-1, minute+1, openvalves + [v[0]], score + v[1][0])
                    doneany = True
                    if result > maxresult:
                        maxresult = result
                    if vcount > maxfind and minute > 2 and minute < 20:
                        break
            else:
                vcount = 0
                for v in values1:
                    vcount += 1
                    wcount = 0
                    for w in values2:
                        if v[0] != w[0]:
                            wcount += 1
                            result = find_total_value(v[0], w[0], v[1][1], w[1][1], minute+1, openvalves + [v[0], w[0]], score + v[1][0] + w[1][0])
                            doneany = True
                            if result > maxresult:
                                maxresult = result
                            if wcount > maxfind and minute > 2 and minute < 20:
                                break
                    if not doneany:
                        result = find_total_value(v[0], starting_point2, v[1][1], wait2-1, minute+1, openvalves + [v[0]], score + v[1][0])
                        doneany = True
                        if result > maxresult:
                            maxresult = result
                    if vcount > maxfind:
                        break
            if not doneany:
                result = find_total_value(starting_point1, starting_point2, wait1-1, wait2-1, minute+1, openvalves, score)
                doneany = True
                if result > maxresult:
                    maxresult = result

        return maxresult

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

    maxfind = 9999
    hiscore = 0
    result = find_total_value('AA', 'AA', 0, 0, 1, [], 0)

    return result

result = process('d16-p1-data.txt', 26)
#result = process('d16-p1-testdata.txt', 26)
print(result)
