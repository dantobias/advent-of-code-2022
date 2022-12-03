def rps_outcome(play):
    result = 0
    if play[1] == 'A':
        result += 1
        if play[0] == 'X':
            result += 3
        elif play[0] == 'Z':
            result += 6
    elif play[1] == 'B':
        result += 2
        if play[0] == 'X':
            result += 6
        elif play[0] == 'Y':
            result += 3
    elif play[1] == 'C':
        result += 3
        if play[0] == 'Y':
            result += 6
        elif play[0] == 'Z':
            result += 3
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
