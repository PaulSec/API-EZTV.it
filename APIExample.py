from eztvAPI import *

test_api = eztvAPI().TV_Show('Game Of Thrones')

# get all the seasons from Game Of Thrones
print test_api.seasons()

# specific season
print test_api.season(3)

# specific episode
print test_api.episode(3, 10)