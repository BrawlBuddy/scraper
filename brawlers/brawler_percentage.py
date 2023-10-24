import collections
import json

with open("brawlers.json", 'r') as f:
    brawlersRaw = json.load(f)

with open("entries.json", 'r') as f:
    entries = json.load(f)

brawler_names = list()

for brawler in brawlersRaw['items']:
    brawler_names.append(brawler['name'])

class Brawler:
    def __init__(self, name, brawlers):
        self.name = name
        self.maps = collections.defaultdict(lambda: [0,0])
        self.gamemodes = collections.defaultdict(lambda: [0,0])
        self.wl = {}
        for b in brawlers:
            self.wl[b] = [0,0] #wins, losses
        
    
    def update_b(self, brawler, win):
        if win:
            self.wl[brawler][0] += 1
        else:
            self.wl[brawler][1] += 1
    
    def update_g(self, gamemode, win):
        if win:
            self.gamemodes[gamemode][0] += 1
        else:
            self.gamemodes[gamemode][1] += 1
    
    def update_m(self, map, win):
        if win:
            self.maps[map][0] += 1
        else:
            self.maps[map][1] += 1
    
    def get_win_percentage_b(self, brawler):
        games = sum(self.wl[brawler])
        if games:
            return self.wl[brawler][0]/games
        else:
            return 0
    
    def get_win_percentage_g(self, gamemode):
        games = sum(self.gamemodes[gamemode])
        if games:
            return self.gamemodes[gamemode][0]/games
        else:
            return 0
    
    def get_win_percentage_m(self, map):
        games = sum(self.maps[map])
        if games:
            return self.maps[map][0]/games
        else:
            return 0

brawlers = {}
for b in brawler_names:
    brawlers[b] = Brawler(b, brawler_names)

def find_all_percentages():
    for entry in entries:
        map = entry["map"]
        gamemode = entry["mode"]
        a_won = entry["teamAWin"] #not sure if this returns the bool properly
        if a_won:
            w_team = entry["teamA"]
            l_team = entry["teamB"]
        else:
            w_team = entry["teamB"]
            l_team = entry["teamA"]
        
        w_team = list(set(w_team)) #get rid of duplicates
        l_team = list(set(l_team))

        for name in w_team:
            winner = brawlers[name]
            winner.update_g(gamemode, True)
            winner.update_m(map, True)
            for name2 in l_team:
                loser = brawlers[name2]
                winner.update_b(name2, True)
                loser.update_b(name, False)
                loser.update_m(map, False)
                loser.update_g(gamemode, False)

def display_win_percentages(brawler_list):
    for name in brawler_list:
        b = brawlers[name]
        print(name)
        for name2 in brawler_list:
            print(name, "win percentage against", name2, ":", b.get_win_percentage_b(name2))
        for mode in b.gamemodes:
            print(name, "win percentage in", mode, ":", b.get_win_percentage_g(mode))

def display_highest_win_percentages():
    for b in brawlers.values():
        max_w = -1
        opp_name = None
        for opp in b.wl:
            win_p = b.get_win_percentage_b(opp)
            if win_p > max_w:
                max_w = win_p
                opp_name = opp
        print(b.name, "highest win percentage is", max_w, "against", opp_name)

find_all_percentages()
#display_win_percentages(["SHELLY", "BUSTER", "LEON", "SURGE", "SPIKE"])
display_highest_win_percentages()



    