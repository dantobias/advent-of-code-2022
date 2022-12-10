def process(filename):
    with open(filename) as infile:
        filedata = infile.readlines()

        x=1
        cycle = 1
        pixel = 0
        lineno = 0
        image = ['', '', '', '', '', '']

        for line in filedata:
            line = line.rstrip()
            cmd = line.split()
            if cmd[0] == 'noop':
                if pixel >= x-1 and pixel <= x+1:
                    image[lineno] += '#'
                else:
                    image[lineno] += ' '
                pixel += 1
                if pixel >= 40:
                    pixel -= 40
                    lineno += 1
                cycle += 1
            elif cmd[0] == 'addx':
                for i in range(2):
                    if pixel >= x-1 and pixel <= x+1:
                        image[lineno] += '#'
                    else:
                        image[lineno] += ' '
                    pixel += 1
                    if pixel >= 40:
                        pixel -= 40
                        lineno += 1
                    cycle += 1
                x += int(cmd[1])

    return image

result = process('d10-p1-data.txt')
for i in range(6):
    print(result[i])
