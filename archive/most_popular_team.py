import json


def sort_dict_by_value(input_dict):
    # Use the sorted() function to sort the dictionary items by value
    sorted_items = sorted(input_dict.items(), key=lambda item: item[1])
    return tuple(sorted_items)

with open("entries.json", 'r') as f:
    entries = json.load(f)

teamA_count = dict()
teamB_count = dict()

print(len(entries))
for entry in entries:
    # team A portion:
    teamA = tuple(entry['teamA'])
    if teamA_count.get(teamA) == None:
        teamA_count[teamA] = 1
    else:
        teamA_count[teamA] += 1
    
    # team B portion:
    teamB = tuple(entry['teamB'])
    if teamB_count.get(teamB) == None:
        teamB_count[teamB] = 1
    else:
        teamB_count[teamB] += 1


teamA_result = sort_dict_by_value(teamA_count)
print(teamA_result)

teamB_result = sort_dict_by_value(teamB_count)
#print(teamB_result)



