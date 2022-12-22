import re

lineexpr = re.compile(r'([a-z]+) ([\+\-\*\/]) ([a-z]+)')

def process(filename):

    def evaluate_monkey(monkey):
        nonlocal monkeyval

        print("evaluate_monkey:", monkey, monkeyval[monkey])

        if not monkey in monkeyval:
            return None

        if monkeyval[monkey] == None:
            if monkeyop[monkey][1] == '+':
                monkeyval[monkey] = evaluate_monkey(monkeyop[monkey][0]) + evaluate_monkey(monkeyop[monkey][2])
            elif monkeyop[monkey][1] == '-':
                monkeyval[monkey] = evaluate_monkey(monkeyop[monkey][0]) - evaluate_monkey(monkeyop[monkey][2])
            elif monkeyop[monkey][1] == '*':
                monkeyval[monkey] = evaluate_monkey(monkeyop[monkey][0]) * evaluate_monkey(monkeyop[monkey][2])
            elif monkeyop[monkey][1] == '/':
                monkeyval[monkey] = int(evaluate_monkey(monkeyop[monkey][0]) / evaluate_monkey(monkeyop[monkey][2]))

        return monkeyval[monkey]

    monkeyval = {}
    monkeyop = {}

    result = None

    with open(filename) as infile:
        filedata = infile.readlines()

        for line in filedata:
            line = line.rstrip()
            vals = line.split(': ')
            monkeyname = vals[0]
            monkeynum = vals[1]
            mathmatch = lineexpr.match(monkeynum)
            if mathmatch:
                monkey1 = mathmatch.group(1)
                mathop = mathmatch.group(2)
                monkey2 = mathmatch.group(3)
                monkeynum = None
                monkeyop[monkeyname] = (monkey1, mathop, monkey2)
            else:
                monkeynum = int(monkeynum)

            monkeyval[monkeyname] = monkeynum

    result = evaluate_monkey('root')        

    return result

result = process('d21-p1-data.txt')
#result = process('d21-p1-testdata.txt')

print(result)
