from bot import Bot
from licytacja import Licytacja

def earnings(gracze):
    for player in gracze:
        for tile in player.ownedTiles:
            player.coins+=tile.value
