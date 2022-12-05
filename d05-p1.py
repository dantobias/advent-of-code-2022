import re

def restack(filename, stacks):
    with open(filename) as infile:
        filedata = infile.readlines()
        movesection = False
        stack = [None]
        for i in range(stacks):
            stack.append([])

        p = re.compile(r'\d+')

        for line in filedata:
            line = line.rstrip()
            if line == '':
                movesection = True
            elif not movesection:
                for i in range(stacks):
                    stackno = i+1
                    index = 1 + 4*i
                    if index < len(line) and line[index] != ' ':
                        stack[stackno].append(line[index])
            else:
                movenums = p.findall(line)
                for i in range(int(movenums[0])):
                    item = stack[int(movenums[1])].pop(0)
                    stack[int(movenums[2])].insert(0, item)
    result = ''
    for i in range(stacks):
        result += stack[i+1][0]
    return result

result = restack('d05-p1-data.txt', 9)
print(result)
