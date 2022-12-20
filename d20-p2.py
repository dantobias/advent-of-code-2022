def process(filename):
    numbers = []
    newnumbers = []
    numberpos = []

    with open(filename) as infile:
        filedata = infile.readlines()

        i = 0
        for line in filedata:
            line = line.rstrip()
            numbers.append(int(line)*811589153)
            newnumbers.append(int(line))
            numberpos.append(i)
            i += 1

    zeropos = None

    for m in range(10):
        for i in range(len(numbers)):
            if numbers[i] == 0:
                zeropos = i
            else:
                currpos = numberpos[i]
                newpos = (currpos + numbers[i])%(len(numbers)-1)

                if numbers[i] > 0:
                    if newpos > currpos:
                        newnumbers = newnumbers[0:currpos] + newnumbers[currpos+1:newpos+1] + [numbers[i]] + newnumbers[newpos+1:len(numbers)]
                        for j in range(len(numbers)):
                            if numberpos[j] == currpos:
                                numberpos[j] = newpos
                            elif numberpos[j] > currpos and numberpos[j] <= newpos:
                                numberpos[j] -= 1
                    elif newpos < currpos:
                        newnumbers = newnumbers[0:newpos] + [numbers[i]] + newnumbers[newpos:currpos] + newnumbers[currpos+1:len(numbers)]
                        for j in range(len(numbers)):
                            if numberpos[j] == currpos:
                                numberpos[j] = newpos
                            elif numberpos[j] >= newpos and numberpos[j] < currpos:
                                numberpos[j] += 1
                elif numbers[i] < 0:
                    if newpos == 0:
                        newpos = len(numbers)
                    if newpos > currpos:
                        newnumbers = newnumbers[0:currpos] + newnumbers[currpos+1:newpos+1] + [numbers[i]] + newnumbers[newpos+1:len(numbers)]
                        for j in range(len(numbers)):
                            if numberpos[j] == currpos:
                                numberpos[j] = newpos
                            elif numberpos[j] > currpos and numberpos[j] <= newpos:
                                numberpos[j] -= 1
                    elif newpos < currpos:
                        newnumbers = newnumbers[0:newpos] + [numbers[i]] + newnumbers[newpos:currpos] + newnumbers[currpos+1:len(numbers)]
                        for j in range(len(numbers)):
                            if numberpos[j] == currpos:
                                numberpos[j] = newpos
                            elif numberpos[j] >= newpos and numberpos[j] < currpos:
                                numberpos[j] += 1
        #print(newnumbers)

    #print(newnumbers[(1000+numberpos[zeropos])%len(numbers)], newnumbers[(2000+numberpos[zeropos])%len(numbers)], newnumbers[(3000+numberpos[zeropos])%len(numbers)])

    result = newnumbers[(1000+numberpos[zeropos])%len(numbers)] + newnumbers[(2000+numberpos[zeropos])%len(numbers)] + newnumbers[(3000+numberpos[zeropos])%len(numbers)]

    return result

result = process('d20-p1-data.txt')
#result = process('d20-p1-testdata.txt')

print(result)
