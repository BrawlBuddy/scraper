import requests
import time
import pickle

def compare_arrays(team0, team1):
    for i in range(3):
        word0 = team0[i]
        word1 = team1[i]

        if word0 == word1:
            continue
        if word0 > word1:
            return 1,0
        else:
            return 0,1
        
    return -1,-1

def query(url):
    api_key = r"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc3NDY1ODQ1LWM4MzEtNDBmMy04NWYyLTQzYzE1MzljMWM1NyIsImlhdCI6MTY5NzY3OTM3NSwic3ViIjoiZGV2ZWxvcGVyL2ZjNjE3MjUwLWVlNWUtYTBmMy0wYzQ4LWJjZDNmOTAzN2QxOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTI5LjE0Ni40NS4xNzUiXSwidHlwZSI6ImNsaWVudCJ9XX0.BK6-DN_p18WGgUOGdTEJQB4nsLgQvs_bqdRnmg2F9wFB1HjIbuI78ZSY8mUGwrILbAQZzNnvaE5pWi0wV3nkLQ"
    # Set up the headers with your API token
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None


def view_logs(tag):

    good_game_modes = ["brawlBall", "gemGrab", "knockout", "heist", "bounty"]

    
    with open("entries.pickle" , 'rb') as f:
        entries = pickle.load(f)
    
    entries = dict()
    cleaned_tag = tag.replace('#','')

    # URL for the Brawl Stars API
    url = f'https://api.brawlstars.com/v1/players/%23{cleaned_tag}/battlelog'

    data = query(url)
    if data == None:
        return

    for battle in data['items']:
        mode = battle['event'].get('mode')


        if mode == None or mode not in good_game_modes:
            continue
        
        game_map = battle['event']['map']
        time = battle['battleTime']
        star_player = battle['battle']['starPlayer']['tag']
        if battle['battle']['result'] =="victory":
            victory = True #this means that the player whos id im scanning won
        else:
            victory = False
        team_results = list()

        for team in battle['battle']['teams']:
            team_status = not victory #if player is NOT on this team, the teams status is the opposite of the result
            team_comp = list()
            for player in team:
                if player['tag'] == tag:
                    team_status = victory #if player is on this team, the teams status matches the result
                team_comp.append(player['brawler']['name'])
            team_comp = sorted(team_comp) #sort alpha so always same order
            team_results.append((team_status, team_comp))
        teamA, teamB = compare_arrays(team_results[0],team_results[1]) #basically making sure team comps are always in the same order
        if teamA == -1:
            continue #if the two teams are the same ignore

        teamA = tuple(team_results[teamA][1]),
        teamB = tuple(team_results[teamB][1]),
        teamAWin = team_results[0][0]

        

        key = (teamA,teamB)
        unique_string = str(time) + star_player
        
        if entries.get(key) == None:
            new_result = {
                'teamA':teamA,
                'teamB':teamB,
                'teamAWin':teamAWin,
                'mode':mode,
                'gameMap':game_map,
                'starPlayer': star_player,
                'time': time
            }


            first_battle_result = [new_result]
            entries[key] = {
                'uniqueGames': {unique_string},
                'battleResults': first_battle_result
            }
        else:
            if unique_string in entries[key]['uniqueGames']:
                print("skipping already seen battle...")
                continue #skip repeat events
            entries[key]['uniqueGames'].add(unique_string)
            entries[key]['battleResults'].append({'teamA':teamA, 'teamB':teamB, 'teamAWin':teamAWin, 'mode':mode, 'gameMap':game_map, 'starPlayer': star_player, 'time': time})
        


    


    with open("entries.pickle", "wb") as f:
        pickle.dump(entries,f)

    #debug out the response from server
    '''
    with open("response.json", "w") as f:
        json.dump(data,f)
    '''


def get_country_clubs(country):
    data = query(f'https://api.brawlstars.com/v1/rankings/{country}/clubs')
    if data == None:
        return []
    output = list()
    for club in data['items']:
        output.append(club['tag'])   
    return output



def get_club_members(club_tag):
    cleaned_tag = club_tag.replace('#','')

    data = query(f'https://api.brawlstars.com/v1/clubs/%23{cleaned_tag}/members')

    if data == None:
        return []

    output = list()
    for member in data['items']:
        output.append(member['tag'])
    
    return output




player_tag_list = list()

for club in get_country_clubs('CA'):
    player_tag_list.extend(get_club_members(club))
    print("done club")
    time.sleep(1)

for player in player_tag_list:
    try:
        view_logs(player)
    except Exception as e:
        print(e.__class__)
        print("caused when checking " + player)
    print("done player")
    time.sleep(1)
