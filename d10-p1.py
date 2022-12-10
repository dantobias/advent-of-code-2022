def process(filename):
    result = 0
    with open(filename) as infile:
        filedata = infile.readlines()

        x=1
        cycle = 1
        checkcycle = 20

        for line in filedata:
            line = line.rstrip()
            cmd = line.split()
            if cmd[0] == 'noop':
                if cycle == checkcycle:
                    result += checkcycle * x
                    checkcycle += 40
                cycle += 1
            elif cmd[0] == 'addx':
                if cycle == checkcycle or cycle+1 == checkcycle:
                    result += checkcycle * x
                    checkcycle += 40
                x += int(cmd[1])
                cycle += 2

    return result

result = process('d10-p1-data.txt')
print(result)
