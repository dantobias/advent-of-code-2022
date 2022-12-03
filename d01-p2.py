def find_max_calories(filename, num_elves):
    with open(filename) as infile:
        filedata = infile.readlines()
        filedata.append('')
        maxcal = [0 for n in range(0,num_elves)]
        currcal = 0
        for line in filedata:
            line = line.rstrip()                       
            if line=='':
                for i in range(0,num_elves):
                    if currcal > maxcal[i]:
                        for j in range(num_elves-1, i-1, -1):
                            maxcal[j] = maxcal[j-1]
                        maxcal[i] = currcal
                        break
                currcal = 0
            else:
                currcal += int(line)
    return maxcal

max_array = find_max_calories('d01-p1-data.txt', 3)
print(max_array)
print(sum(max_array))
