import re

cmd = re.compile(r'\$ (.+)')

def process(filename):
    result = None
    currdir = '/'
    dirsize = {}
    dirs = ['/']
    with open(filename) as infile:
        filedata = infile.readlines()

        for line in filedata:
            line = line.rstrip()
            cmatch = cmd.match(line)
            if cmatch:
                command = cmatch.group(1).split()
                if command[0] == 'cd':
                    if command[1] == '..':
                        dirs.pop()
                        currdir = dirs[-1]
                    elif command[1] == '/':
                        currdir = '/'
                        dirs = ['/']
                    else:
                        currdir += command[1] + '/'
                        dirs.append(currdir)
            else:
                value = line.split()
                if value[0] != 'dir':
                    for d in dirs:
                        if d in dirsize:
                            dirsize[d] += int(value[0])
                        else:
                            dirsize[d] = int(value[0])

    freespace = 70000000 - dirsize['/']
    spaceneeded = 30000000 - freespace
    for d in dirsize:
        if dirsize[d] >= spaceneeded and (not result or dirsize[d] < result):
            result = dirsize[d]
    return result

result = process('d07-p1-data.txt')
print(result)
