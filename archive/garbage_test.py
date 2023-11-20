def is_correct_order(team0, team1):
    for i in range(3):
        word0 = team0[i]
        word1 = team1[i]

        if word0 == word1:
            continue
        if word0 > word1:
            return True
        else:
            return False
        
    return False

test = dict()

try:
    print(test['test'])

except Exception as e:
    print(e.__class__)
    print(str(e) + " caused when checking ")

print(is_correct_order(['C','B','C'],['C','B','A']))