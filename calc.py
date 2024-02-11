import json
import pandas as pd
from itertools import product

win_rate = dict()
interm_result = dict() 
games_played = dict()
use_rate = dict()
max_rate = 0
timestamps = dict()
win_rates = dict()
map_mode = set()
duo_chem = dict()
trio_chem = dict()

# Define chunk size
chunk_size = 1000

# Create a pandas reader object with chunksize
reader = pd.read_csv('combined.csv', chunksize=chunk_size, skiprows=1)

for chunk in reader:
    for index, row in chunk.iterrows():
        battle_time = row.iloc[0]
        battle_mode = row.iloc[1]
        battle_map = row.iloc[2] 
        team_A_wins = bool(row.iloc[3])
        team_A = row.iloc[4].split('_') 
        team_B = row.iloc[5].split('_')

        if len(team_A) != 3 or len(team_B) != 3:
            continue

        #used for use rate
        games = games_played.get(battle_map)
        if games == None:
            games = 0
        games_played[battle_map] = games+1

        #used for use rate and map
        if interm_result.get(battle_map) == None:
            interm_result[battle_map] = dict()
        for brawler_A in team_A:
            current_result = interm_result[battle_map].get(brawler_A)
            if current_result == None:
                current_result = {
                "wins": set(),
                "games": set()
                }
            if team_A_wins:
                current_result['wins'].add(battle_time)
            current_result['games'].add(battle_time)
            interm_result[battle_map][brawler_A] = current_result
        
        for brawler_B in team_B:
            current_result = interm_result[battle_map].get(brawler_B)
            if current_result == None:
                current_result = {
                "wins": set(),
                "games": set()
                }
            if team_A_wins:
                current_result['wins'].add(battle_time)
            current_result['games'].add(battle_time)
            interm_result[battle_map][brawler_B] = current_result

        #used for 1v1
        combinations = list(product(team_A, team_B))
        for brawler_pair in combinations:
            pair = list(brawler_pair)
            pair.sort()
            pair_record = timestamps.get('_'.join(pair))
            if pair_record == None:
                pair_record = {
                    "wins": set(),
                    "games": set()
                }
            pair_record["games"].add(battle_time)
            if team_A_wins ^ (pair[0] in team_B):
                pair_record["wins"].add(battle_time)
            
            timestamps['_'.join(pair)] = pair_record
        
        #map_mode
        map_mode.add((battle_map,battle_mode))

        #duo_chem
        #team_A
        team_A.sort()
        teamA_combos = [f"{team_A[0]}_{team_A[1]}",f"{team_A[1]}_{team_A[2]}",f"{team_A[0]}_{team_A[2]}"]

        for duoA in teamA_combos:
            current_count = duo_chem.get(duoA)
            if current_count == None:
                wins = 0
                games = 0
            else:
                wins = current_count[0]
                games = current_count[1]
            games += 1
            if team_A_wins:
                wins += 1
            duo_chem[duoA] = (wins,games)
        
        #team_B
        team_B.sort()
        teamB_combos = [f"{team_B[0]}_{team_B[1]}",f"{team_B[1]}_{team_B[2]}",f"{team_B[0]}_{team_B[2]}"]
        for duoB in teamB_combos:
            current_count = duo_chem.get(duoB)
            if current_count == None:
                wins = 0
                games = 0
            else:
                wins = current_count[0]
                games = current_count[1]
            games += 1
            if not team_A_wins:
                wins += 1
            duo_chem[duoB] = (wins,games)
        
        #trio_chem
        #team_A
        teamA = '_'.join(team_A)
        current_count = trio_chem.get(teamA)
        if current_count == None:
            wins = 0
            games = 0
        else:
            wins = current_count[0]
            games = current_count[1]
        games += 1
        if team_A_wins:
            wins += 1
        trio_chem[teamA] = (wins,games)
        
        #team_B

        teamB = '_'.join(team_B)
        current_count = trio_chem.get(teamB)
        if current_count == None:
            wins = 0
            games = 0
        else:
            wins = current_count[0]
            games = current_count[1]
        games += 1
        if not team_A_wins:
            wins += 1
        trio_chem[teamB] = (wins,games)



 
    
# 2 and 3 score
with open("results/2scores.json", "w") as f:
    json.dump(duo_chem, f)
        
with open("results/3scores.json", "w") as f:
    json.dump(trio_chem, f)        

#map_mode
with open("results/maps_modes.json","w") as f:
    json.dump(list(map_mode),f)

#1v1
for brawler in list(timestamps.keys()):
    win_rates[brawler] = len(timestamps[brawler]['wins'])/len(timestamps[brawler]['games'])

with open("results/1v1.json", "w") as f:
    json.dump(win_rates, f)



#map and user_rate
for battle_map in interm_result.keys():
    win_rate[battle_map] = dict()
    use_rate[battle_map] = dict()
    for brawler in interm_result[battle_map].keys():
        val = interm_result[battle_map][brawler]
        win_rate[battle_map][brawler] = len(val['wins'])/len(val['games'])
        use_rate[battle_map][brawler] = len(val['wins'])/games_played[battle_map]

with open("results/map.json", "w") as f:
    json.dump(win_rate,f)

with open("results/use_rate.json", "w") as f:
    json.dump(use_rate, f)

