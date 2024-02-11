import requests
import json
import time
import config

def get_clubs(country_code):
    time.sleep(0.5)
    url = f"https://api.brawlstars.com/v1/rankings/{country_code}/clubs"
  

    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        # Successful request
        data = response.json()['items']
        club_tags = list()
        for entry in data:
            club_tags.append(entry['tag'].replace('#',''))
        return club_tags
    else:
        # Handle errors
        print(f"Error {response.status_code}: {response.text}")
        return list()

def get_players(tag):
    time.sleep(0.5)
    url = f"https://api.brawlstars.com/v1/clubs/%23{tag}/members"
   
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Successful request
        data = response.json()['items']
        player_tags = list()
        for entry in data:
            player_tags.append(entry['tag'].replace('#',''))
        return player_tags
    else:
        # Handle errors
        print(f"Error {response.status_code}: {response.text}")
        return list()
        

def get_battles(tag):
    #time.sleep(0.5)
    url = f"https://api.brawlstars.com/v1/players/%23{tag}/battlelog"
    tag_with_hashtag = "#" + tag
    

    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        # Successful request
        data = response.json()['items']
        player_battles = list()
        for entry in data:
            battle_time = entry['battleTime']
            battle_map = entry['event'].get('map')
            battle_mode = entry['event'].get('mode')
            if battle_map == None or battle_mode == None:
                continue
            #print((battle_time,battle_map,battle_mode))
            # now trying to find information on match comp and which side won

            result = entry['battle'].get('result')
            if result == None:
                continue
            if result == "victory":
                local_player_wins = True
            else:
                local_player_wins = False

            team_info = entry['battle'].get('teams')
            if team_info == None or len(team_info) != 2:
                print("skipping...")
                continue
            #print(team_info)
            team_A_wins = not local_player_wins
            team_A = team_info[0]
            #print(team_A)
            team_A_comp = list()
            for player in team_A:
                if player['tag'] == tag_with_hashtag:
                    team_A_wins = local_player_wins
                team_A_comp.append(player['brawler']['name'])

            team_B = team_info[1]
            team_B_comp = list()
            for player in team_B:
                team_B_comp.append(player['brawler']['name'])

            if len(team_B_comp) != 3 or len(team_A_comp) != 3:
                continue

            result_struct = {
                'battle_time': battle_time,
                'battle_mode': battle_mode,
                'battle_map': battle_map,
                'team_A_wins': team_A_wins,
                'team_A': team_A_comp,
                'team_B': team_B_comp
            }
            #print(result_struct)
            player_battles.append(result_struct)
            
        return player_battles
    else:
        # Handle errors
        print(f"Error {response.status_code}: {response.text}")
        return list()

# skipped files: already ran on this 
# "AF"


country_codes = ["AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BH","BS","BD","BB","BY","BE","BZ","BJ","BM","BT","BO","BQ","BA","BW","BV","BR","IO","BN","BG","BF","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CC","CO","KM","CG","CD","CK","CR","CI","HR","CU","CW","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","ET","FK", "FO", "FJ", "FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GI","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY","HT","HM","VA","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM","JP","JE","JO","KZ","KE","KI","KP","KR","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","MV","ML","MT","MH","MQ","MR","MU","YT","MX","FM","MD","MC","MN","ME","MS","MA","MZ","MM","NA","NR","NP","NL","NC","NZ","NI","NE","NG","NU","NF","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PN","PL","PT","PR","QA","RE","RO","RU","RW","BL","SH","KN","LC","MF","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB","SO","ZA","SS","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TL","TG","TK","TO","TT","TN","TR","TM","TC","TV","UG","UA","AE","GB","US","UM","UY","UZ","VU","VE","VN","VG","VI","WF","EH","YE","ZM","ZW"]

for country_code in country_codes:
    print(f"{country_code} - Starterd")
    country_buffer = list()
    for club in get_clubs(country_code):
        for player in get_players(club):    
            country_buffer.extend(get_battles(player))
    with open(f"regional_battles/{country_code}.json", "w") as f:
        json.dump(country_buffer, f)





