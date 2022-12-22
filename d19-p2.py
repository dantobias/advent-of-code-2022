import re

def process(filename, minutes):

    cache = {}
    highest_geode = -1

    def try_robots(minute, ore, clay, obsidian, geode, orerobot, clayrobot, obsidianrobot, geoderobot):

        def estimate_count(minute, ore, clay, obsidian, geode, orerobot, clayrobot, obsidianrobot, geoderobot):
            newminute = minute
            newore = ore
            newclay = clay
            newobsidian = obsidian
            newgeode = geode
            neworerobot = orerobot
            newclayrobot = clayrobot
            newobsidianrobot = obsidianrobot
            newgeoderobot = geoderobot

            #print(minute, 'Material', ore, clay, obsidian, geode, 'Robot', orerobot, clayrobot, obsidianrobot, geoderobot)

            while newminute < minutes:
                newminute += 1

                tempore = newore
                tempclay = newclay
                tempobsidian = newobsidian
                tempgeode = newgeode

                minutesleft = minutes - newminute
                endingore = (minutesleft - 1)*neworerobot + newore
                endingclay = (minutesleft - 3)*newclayrobot + newclay
                endingobsidian = (minutesleft - 2)*newobsidianrobot + newobsidian

                newore += neworerobot
                newclay += newclayrobot
                newobsidian += newobsidianrobot
                newgeode += newgeoderobot

                if tempobsidian >= geoderobotobsidian and tempore >= geoderobotore:
                    newgeoderobot += 1
                    newobsidian -= geoderobotobsidian
                    newore -= geoderobotore

                elif tempclay >= obsidianrobotclay and tempore >= obsidianrobotore and endingobsidian < geoderobotobsidian * (minutesleft-4):
                    newobsidianrobot += 1
                    newclay -= obsidianrobotclay
                    newore -= obsidianrobotore

                elif clayrobotore >= orerobotore and tempore >= clayrobotore and endingclay < obsidianrobotclay * (minutesleft-8):
                    newclayrobot += 1
                    newore -= clayrobotore

                elif tempore >= orerobotore and endingore <= geoderobotore * (minutesleft - 1):
                    neworerobot += 1
                    newore -= orerobotore

                elif orerobotore < clayrobotore and tempore >= clayrobotore and endingclay < obsidianrobotclay * (minutesleft-8):
                    newclayrobot += 1
                    newore -= clayrobotore

                #print('  ', newminute, 'Material', newore, newclay, newobsidian, newgeode, 'Robot', neworerobot, newclayrobot, newobsidianrobot, newgeoderobot)

            return newgeode

        #print(blueprintno, minute, "Robots:", orerobot, clayrobot, obsidianrobot, geoderobot, "Supplies:", ore, clay, obsidian, geode)

        if (minute, ore, clay, obsidian, geode, orerobot, clayrobot, obsidianrobot, geoderobot) in cache:
            #print('Cache!', minute, geode)
            return cache[(minute, ore, clay, obsidian, geode, orerobot, clayrobot, obsidianrobot, geoderobot)]

        statstr = "Minute "+str(minute)+": "+str(orerobot)+" ore robots, "+str(clayrobot)+" clay robots, "+str(obsidianrobot)+" obsidian robots, "+str(geoderobot)+" geode robots\n"
        statstr += "  "+str(ore)+" ore, "+str(clay)+" clay, "+str(obsidian)+" obsidian, "+str(geode)+" geode\n"

        if minute>=minutes:
            #print('\n'+statstr)
            #print('Endpoint', minute, geode)
            nonlocal highest_geode
            if geode > highest_geode:
                highest_geode = geode
                print('New max:', highest_geode)
            return (geode, statstr)

        possibilities = []

        if obsidian >= geoderobotobsidian and ore >= geoderobotore:
            possibilities.append((0, 0, 0, 1))

        if clay >= obsidianrobotclay and ore >= obsidianrobotore:
            possibilities.append((0, 0, 1, 0))

        if ore >= clayrobotore:
            possibilities.append((0, 1, 0, 0))

        if ore >= orerobotore:
            possibilities.append((1, 0, 0, 0))

        possibilities.append((0, 0, 0, 0))

        #print(maxp)

        output = None

        if minute < 99:
            maxtest = -1
            for p in possibilities:
                newore = ore + orerobot - orerobotore*p[0] - clayrobotore*p[1] - obsidianrobotore*p[2] - geoderobotore*p[3]
                newclay = clay + clayrobot - obsidianrobotclay*p[2]
                newobsidian = obsidian + obsidianrobot - geoderobotobsidian*p[3]
                newgeode = geode + geoderobot
                testoutput = try_robots(minute+1, newore, newclay, newobsidian, newgeode, orerobot+p[0], clayrobot+p[1], obsidianrobot+p[2], geoderobot+p[3])
                if testoutput[0] > maxtest:
                    output = testoutput
                    maxtest = testoutput[0]
        else:
            maxgeode = -1
            maxp = None
            for p in possibilities:
                newore = ore + orerobot - orerobotore*p[0] - clayrobotore*p[1] - obsidianrobotore*p[2] - geoderobotore*p[3]
                newclay = clay + clayrobot - obsidianrobotclay*p[2]
                newobsidian = obsidian + obsidianrobot - geoderobotobsidian*p[3]
                newgeode = geode + geoderobot
                testgeode = estimate_count(minute+1, newore, newclay, newobsidian, newgeode, orerobot+p[0], clayrobot+p[1], obsidianrobot+p[2], geoderobot+p[3])
                if testgeode > maxgeode:
                    maxgeode = testgeode
                    maxp = p

            p = maxp
            newore = ore + orerobot - orerobotore*p[0] - clayrobotore*p[1] - obsidianrobotore*p[2] - geoderobotore*p[3]
            newclay = clay + clayrobot - obsidianrobotclay*p[2]
            newobsidian = obsidian + obsidianrobot - geoderobotobsidian*p[3]
            newgeode = geode + geoderobot
            output = try_robots(minute+1, newore, newclay, newobsidian, newgeode, orerobot+p[0], clayrobot+p[1], obsidianrobot+p[2], geoderobot+p[3])

        #if maxgeode >= 11:
        #    print('\n'+statstr+outstatus)

        #cache[(minute, ore, clay, obsidian, geode, orerobot, clayrobot, obsidianrobot, geoderobot)] = (output[0], statstr+output[1])

        return (output[0], statstr+output[1])


    lineexpr = re.compile(r'Blueprint ([0-9]+)\: Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore\. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay\. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian\.')

    result = 1

    with open(filename) as infile:
        filedata = infile.readlines()

        for line in filedata:
            line = line.rstrip()
            cmatch = lineexpr.match(line)
            if cmatch:
                blueprintno = int(cmatch.group(1))
                orerobotore = int(cmatch.group(2))
                clayrobotore = int(cmatch.group(3))
                obsidianrobotore = int(cmatch.group(4))
                obsidianrobotclay = int(cmatch.group(5))
                geoderobotore = int(cmatch.group(6))
                geoderobotobsidian = int(cmatch.group(7))

                #if blueprintno in saveddata:
                #    testresult = (saveddata[blueprintno], 'From Saved Data')
                #else:

                testresult = try_robots(0, 0, 0, 0, 0, 1, 0, 0, 0)
                print(blueprintno, testresult[0])

                result *= testresult[0]
                print(testresult[1])
                        
    return result

result = process('d19-p2-data.txt', 32)
#result = process('d19-p1-testdata.txt', 32)

print(result)
