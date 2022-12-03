def rps_outcome(play):
    result = 0
    if play[0] == 'A':
        if play[1] == 'X':
            result += 3
        elif play[1] == 'Y':
            result += 3
            result += 1
        elif play[1] == 'Z':
            result += 6
            result += 2
    elif play[0] == 'B':
        if play[1] == 'X':
            result += 1
        elif play[1] == 'Y':
            result += 3
            result += 2
        elif play[1] == 'Z':
            result += 6
            result += 3
    elif play[0] == 'C':
        if play[1] == 'X':
            result += 2
        elif play[1] == 'Y':
            result += 3
            result += 3
        elif play[1] == 'Z':
            result += 6
            result += 1
    return result

def rps_score(filename):
    with open(filename) as infile:
        filedata = infile.readlines()
        score = 0
        for line in filedata:
            line = line.rstrip()
            play = line.split()
            score += rps_outcome(play)

    return score

score = rps_score('d02-p1-data.txt')
print(score)
