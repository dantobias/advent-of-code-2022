itemtypes = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def rucksacks(filename):
    with open(filename) as infile:
        filedata = infile.readlines()
        sum = 0
        num = 0
        for line in filedata:
            line = line.rstrip()
            if len(line)>0:
                num_in_group = num % 3
                    
                if num_in_group == 0:
                    typefound = ({}, {}, {})

                for i in range(0, len(line)):
                    typefound[num_in_group][line[i]] = True

                if num_in_group == 2:
                    matchtype = None
                    for itemtype in typefound[0]:
                        if itemtype in typefound[1] and itemtype in typefound[2]:
                            matchtype = itemtype
                    priority = itemtypes.rfind(matchtype)+1
                    sum += priority

                num += 1
    return sum

sum = rucksacks('d03-p1-data.txt')
print(sum)
