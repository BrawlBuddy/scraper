import os 
import json
import csv

with open("combined.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(['battle_time', 'battle_mode', 'battle_map', 'team_A_wins', 'team_A', 'team_B'])

for file in os.scandir('results/'):
    if file.name.split('.')[1] == "json":
        print(file.name)
        with open(file, "r") as f:
            results = json.load(f)
        with open("combined.csv", "a") as csv_file:
            writer = csv.writer(csv_file)
            for entry in results:
                writer.writerow([entry['battle_time'], entry['battle_mode'], entry['battle_map'], str(entry['team_A_wins']), '_'.join(entry['team_A']), '_'.join(entry['team_B'])])
