# scraper_results

JSON output of our Brawl Stars API scrapper. Sorted by country of club. In the process of developing the 'formatter' which converts the scrapper's output to form usable by the Brawler Manager.

## Picking Process

Randomly selects map and game mode (map implies the game mode). 20 second timer starts with each member getting to pick one brawler to ban. Each player bans one. 3-6 banned. As each player picks, that player is also removed from the pool.

## Weighting of options/results

More information about the weighting will be included in the Brawler Manager repo. However these are are preliminary weights:

- 40% score aginst counter (```1v1.json```)
- 40% score against map (```map.json```)
- 20% score against pool (```1v1.json```)

## TODO

Revolve what's going on with the 1v1 win rates. I got different (more believable) win rates with ```alt_method_1v1_test.py```. Need to figure out why this happened, figure out which results are correct, and write a script to find the 1v1 win rates with a better time efficiency.


Need to figure out what is causing the weird team composition arrays outputted by the scrapper. 40k+ records seem to have this problem, as shown in ```test.py```. Will review:
- what maps/gamemodes aren't 3v3 -> make sure they are excluded from the results
- there are ~1.5k battles were the teams rousters are of uneven lengths -> was this a side effect of sets? (I don't think so, since there are battles that have duplicate brawlers) Maybe this has something to do with disconnects or quits?
- ~39k of these battles have > 3 brawlers per team. What does this mean?

## Current Outputs:

### ```1v1.json```

Maps two brawlers, sorted alphabetically to the first brawlers win rate in the given matchup. For example:
```
{
    "CORDELIUS_HANK": 0.6609989373007439

}
```

This excerpt shows that word CORDELIUS faces HANK, CORDELIUS wins 66.09989373007439% of the time.

### ```map.json```
The first layer of this file maps the game map to a dictionary of results regarding the 

```
{
    "Off the Line": {
        "CORDELIUS": 0.47469357124989575
    }
}
```
This excerpt shows that on the map Off the Line, Cordelius has a 47.469357124989575% win rate.

### ```maps_modes.json```

Contains an array of all maps played in the data set
```
[
    ["Side by Side", "bounty"]
]
```
This excerpt shows that on the map Side by Side, the gamemode is bounty.

### ```2scores.json```

Contains dictionary mapping a pair of brawlers sorted alphabetically to a tuple containing the number of games they have won and played together as a team. For example:
```
{
    "AMBER_CORDELIUS": [
        90621,
        181240
    ]
}
```
This excerpt shows that AMBER and CORDELIUS have played together for 181,240 games and won 90,621 of them.

### ```3scores.json```

Contains dictionary mapping three brawlers sorted alphabetically to a tuple containing the number of games they have won and played together as a team. For example:
```
{
    "AMBER_CORDELIUS_SPIKE": [
        5,
        11
    ]
}
```
This excerpt shows that AMBER, CORDELIUS, and SPIKE have played together for 11 games and won 5 of them.
