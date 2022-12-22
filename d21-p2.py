import re

lineexpr = re.compile(r'([a-z]+) ([\+\-\*\/\=]) ([a-z]+)')

def process(filename):

    def calc_expr(targetvalue, expr):

        #print('calc_expr', expr, targetvalue, '\n')

        if type(expr) != tuple:
            return targetvalue
        else:
            if type(expr[1]) == int:
                if expr[0] == '=':
                    return calc_expr(expr[1], expr[2])
                elif expr[0] == '+':
                    return calc_expr(targetvalue - expr[1], expr[2])
                elif expr[0] == '-':
                    return calc_expr(expr[1] - targetvalue, expr[2])
                elif expr[0] == '*':
                    return calc_expr(int(targetvalue / expr[1]), expr[2])
                elif expr[0] == '/':
                    return calc_expr(int(expr[1] / targetvalue), expr[2])
            elif type(expr[2]) == int:
                if expr[0] == '=':
                    return calc_expr(expr[2], expr[1])
                elif expr[0] == '+':
                    return calc_expr(targetvalue - expr[2], expr[1])
                elif expr[0] == '-':
                    return calc_expr(targetvalue + expr[2], expr[1])
                elif expr[0] == '*':
                    return calc_expr(int(targetvalue / expr[2]), expr[1])
                elif expr[0] == '/':
                    return calc_expr(targetvalue * expr[2], expr[1])
            else:
                return NotImplemented

    def evaluate_monkey(monkey):
        nonlocal monkeyval

        #print("evaluate_monkey:", monkey, monkeyval[monkey])

        if not monkey in monkeyval:
            return None

        if monkeyval[monkey] == None:

            eval1 = evaluate_monkey(monkeyop[monkey][0])
            eval2 = evaluate_monkey(monkeyop[monkey][2])
            op = monkeyop[monkey][1]

            if type(eval1) != int or type(eval2) != int:
                monkeyval[monkey] = (op, eval1, eval2)
                #print(monkeyval[monkey], '\n')
            else:
                if op == '+':
                    monkeyval[monkey] = eval1 + eval2
                elif op == '-':
                    monkeyval[monkey] = eval1 - eval2
                elif op == '*':
                    monkeyval[monkey] = eval1 * eval2
                elif op == '/':
                    monkeyval[monkey] = int(eval1 / eval2)
                elif op == '=':
                    monkeyval[monkey] = eval1 == eval2

            #print(monkeyop[monkey][0], op, monkeyop[monkey][2], monkeyval[monkey])

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
                if monkeyname == 'root':
                    mathop = '='
                monkey2 = mathmatch.group(3)
                monkeynum = None
                monkeyop[monkeyname] = (monkey1, mathop, monkey2)
            else:
                monkeynum = int(monkeynum)
                if monkeyname == 'humn':
                    monkeynum = 'humn'

            monkeyval[monkeyname] = monkeynum

    result = calc_expr(None, evaluate_monkey('root'))

    return result

result = process('d21-p1-data.txt')
#result = process('d21-p1-testdata.txt')

print(result)
