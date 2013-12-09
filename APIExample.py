from eztvAPI import *

# get all the seasons from Game Of Thrones
test_api = eztvAPI().TV_Show('Game Of Thrones').seasons()

# specific season
test_api.season(3)

# specific episode
test_api.episode(3, 10)