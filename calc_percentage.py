import json
import itertools

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



with open("brawlers.json", 'r') as f:
    brawlers = json.load(f)

with open("entries copy.json", 'r') as f:
    entries = json.load(f)

brawler_names = list()

for brawler in brawlers['items']:
    brawler_names.append(brawler['name'])

combinations = list(itertools.combinations(brawler_names,3))

sorted_combinations = list()

for team in combinations:
    sorted_combinations.append(sorted(team))


result = dict()

for teamA in sorted_combinations:
    #for teamB in sorted_combinations:
    teamB = ["BELLE","OTIS","SHELLY"]

    if not is_correct_order(teamA, teamB): #if out of order or same teams skip
        continue
    matches = 0
    wins = 0
    for entry in entries:
        if entry['teamA'] == teamA and entry['teamB'] == teamB:
                matches += 1
                if entry['teamAWin'] == True:
                    wins += 1
    if matches == 0:
        win_rate = None
    else:
        win_rate = wins / matches
        print((teamA,teamB, win_rate, matches))
    result[(tuple(teamA), tuple(teamB))] = (win_rate, matches)

#print(result)
        
