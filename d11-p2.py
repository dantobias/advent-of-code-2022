import re

monkeyline = re.compile(r'Monkey ([0-9]+):')
itemline = re.compile(r'  Starting items: (.*)')
operationline = re.compile(r'  Operation: (.*)')
testline = re.compile(r'  Test: divisible by ([0-9]+)')
trueline = re.compile(r'    If true: throw to monkey ([0-9]+)')
falseline = re.compile(r'    If false: throw to monkey ([0-9]+)')

def process(filename):

    monkeyitems = []
    monkeyops = []
    monkeytests = []
    monkeytrue = []
    monkeyfalse = []
    monkeyinspected = []
    testproduct = 1

    result = None
    with open(filename) as infile:
        filedata = infile.readlines()
        monkey = None

        for line in filedata:
            line = line.rstrip()
            cmatch1 = monkeyline.match(line)
            if cmatch1:
                monkey = int(cmatch1.group(1))
                monkeyinspected.append(0)

            cmatch2 = itemline.match(line)
            if cmatch2:
                items = cmatch2.group(1)
                itemlist = [int(s) for s in items.split(', ')]
                monkeyitems.append(itemlist)

            cmatch3 = operationline.match(line)
            if cmatch3:
                opstr = cmatch3.group(1)
                ops = [s for s in opstr.split(' ')]
                monkeyops.append(ops)

            cmatch4 = testline.match(line)
            if cmatch4:
                test = int(cmatch4.group(1))
                testproduct *= test
                monkeytests.append(test)

            cmatch5 = trueline.match(line)
            if cmatch5:
                trueitem = int(cmatch5.group(1))
                monkeytrue.append(trueitem)

            cmatch6 = falseline.match(line)
            if cmatch6:
                falseitem = int(cmatch6.group(1))
                monkeyfalse.append(falseitem)

    for round in range(10000):
        for monkey in range(len(monkeyops)):
            #print('Round', round, 'Monkey', monkey, 'Items', len(monkeyitems[monkey]))
            for item in range(len(monkeyitems[monkey])):
                monkeyinspected[monkey] += 1
                currlevel = monkeyitems[monkey][item]
                operand = monkeyops[monkey][4]
                if operand == 'old':
                    operand = currlevel
                else:
                    operand = int(operand)
                if monkeyops[monkey][3] == '+':
                    currlevel += operand
                elif monkeyops[monkey][3] == '*':
                    currlevel *= operand
                currlevel %= testproduct
                #print(currlevel, monkeytests[monkey], currlevel % monkeytests[monkey])
                if currlevel % monkeytests[monkey] == 0:
                    monkeyitems[monkeytrue[monkey]].append(currlevel)
                    #print('Moved', currlevel, 'to', monkeytrue[monkey])
                    #print(monkeyitems[monkeytrue[monkey]])
                else:
                    monkeyitems[monkeyfalse[monkey]].append(currlevel)
                    #print('Moved', currlevel, 'to', monkeyfalse[monkey])
                    #print(monkeyitems[monkeyfalse[monkey]])
            monkeyitems[monkey] = []
    #print(monkeyinspected)
    monkeyinspected.sort()
    result = (monkeyinspected[-1] * monkeyinspected[-2])
    return result

result = process('d11-p1-data.txt')
print(result)
