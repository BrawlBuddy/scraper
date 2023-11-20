import pickle

with open("entries.pickle", "rb") as f:
    entries = pickle.load(f)


for entry in entries.keys():

    print(entry)
    print(f"Match count:\t{len(entries[entry]['battleResults'])}")
    win_count = 0
    for battle in entries[entry]['battleResults']:
        if battle["teamAWin"]:
            win_count += 1
    print(f"Team A Win%:\t{win_count/len(entries[entry]['battleResults'])*100}")
    print("\n")