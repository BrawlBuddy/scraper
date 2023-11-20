import requests


def custom_hash(input_set):
    hash_value = 0
    for element in input_set:
        hash_value ^= hash(element)  # XOR the hash of each element
    return hash(hash_value)

api_key = r"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImIwZGFiYTY4LWYxZDItNDJhMi1iODYyLWRmMGMzYWE4OTQ1MiIsImlhdCI6MTY5NzU5OTYzNCwic3ViIjoiZGV2ZWxvcGVyL2ZjNjE3MjUwLWVlNWUtYTBmMy0wYzQ4LWJjZDNmOTAzN2QxOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTA4LjYzLjI1MC4xNjciXSwidHlwZSI6ImNsaWVudCJ9XX0.Eks-PhmKytK0RujSYj_u1Td8DqrG83IY3nOHXr--pYrBIG_wWYlAWU8JAR-MlWg3XsZFXky1lA_j8rMq7LPGqQ"


tag = "#VLQPVPY"

cleaned_tag = tag.replace('#','')

# URL for the Brawl Stars API
url = f'https://api.brawlstars.com/v1/players/%23{cleaned_tag}/battlelog'

# Set up the headers with your API token
headers = {
    'Authorization': f'Bearer {api_key}',
}


response = requests.get(url, headers=headers)

entries = list()
# Check the response status code
if response.status_code == 200:
    # Request was successful
    data = response.json()

    for battle in data['items']:

        if battle['battle']['result'] =="victory":
            victory = True
        else:
            victory = False
        team_results = list()
        for team in battle['battle']['teams']:
            team_status = not victory
            team_comp = set()
            for player in team:
                if player['tag'] == tag:
                    team_status = victory
                team_comp.add(player['brawler']['name'])
            if len(team_comp) != 3:
                continue
            team_results.append((team_status, team_comp, custom_hash(team_comp)))
        if team_results[0][2] == team_results[1][2]:
            continue
        if team_results[0][2] > team_results[1][2]:
            entry = {
                'teamA': team_results[0][1],
                'teamB': team_results[1][1],
                'teamAWin': team_results[0][0]
            }
        else:
            entry = {
                'teamA': team_results[1][1],
                'teamB': team_results[0][1],
                'teamAWin': team_results[1][0]
            }
        print(entry)
        entries.append(entry)

    
            
else:
    # Request was not successful, print the status code and any error message
    print(f"Request failed with status code {response.status_code}: {response.text}")

