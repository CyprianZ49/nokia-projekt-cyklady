def getLegalMoves(self, board, who, god, at, ze, po, ar, ap):
    legalMoves = []
    if board.isFight: #fighting actions
        pass
    if board.turn != who: #checking if it's this players turn
        return legalMoves
    if who.isBuildingMetropolis:
        if who.philosophers == 4: #building Metropolis using philosophers
            for tile in who.ownedTiles:
                if tile.typ == 'capital' and tile.isMetropolis == False:
                    legalMoves.append(f"{tile[0]} {tile[1]}")
        else: #building Metropolis using buildings
            pass
    #specific gods
    if god == "at":
        #build
        if who.coins >= 2:
            for tile in who.ownedTiles:
                if tile.typ == 'capital':
                    for i in range(0, len(tile.buildings)):
                        legalMoves.append(f"b {tile[0]} {tile[1]} {i}")
        #recruit
        koszt = 0
        if at.ktora > 0:
            koszt = 4
        if at.ktora < 2 and who.coins >= koszt:
            legalMoves.append(f"r")
    if god == 'ze':
        #build
        if who.coins >= 2:
            for tile in who.ownedTiles:
                if tile.typ == 'capital':
                    for i in range(0, len(tile.buildings)):
                        legalMoves.append(f"b {tile[0]} {tile[1]} {i}")
        #recruit
        koszt = 0
        if ze.ktora > 0:
            koszt = 4
        if ze.ktora < 2 and who.coins >= koszt:
            legalMoves.append(f"r")
        #smite
        if who.coins + who.actionDiscount >= 3:
            for x in range(13):
                for y in range(13):
                    if (board[x][y].typ == 'capital' or board[x][y].typ == 'water') and board[x][y].strength > 0:
                        legalMoves.append(f"m {x} {y}")
    if god == 'po':
        #build
        if who.coins >= 2:
            for tile in who.ownedTiles:
                if tile.typ == 'capital':
                    for i in range(0, len(tile.buildings)):
                        legalMoves.append(f"b {tile[0]} {tile[1]} {i}")
        #recruit
        koszt = 0
        if po.ktora > 0:
            koszt += po.ktora
        if po.ktora < 4 and who.coins >= koszt:
            legalMoves.append(f"r")
        #move
        pass
    if god == 'ar':
        #build
        if who.coins >= 2:
            for tile in who.ownedTiles:
                if tile.typ == 'capital':
                    for i in range(0, len(tile.buildings)):
                        legalMoves.append(f"b {tile[0]} {tile[1]} {i}")
        #recruit
        koszt = 0
        if ar.ktora > 0:
            koszt += ar.ktora + 1
        if po.ktora < 4 and who.coins >= koszt:
            legalMoves.append(f"r")
        #move
        if who.coins + who.actionDiscount > 0:
            for tile in who.ownedTiles:
                if tile.typ == 'capital':
                    for x in range(13):
                        for y in range(13):
                            if board[x][y].typ == 'capital' and (x, y) != tile and board.isBridge(tile[0], tile[1], who, x, y):
                                for i in range(1, board[tile[0]][tile[1]].strength + 1):
                                    legalMoves.append(f"m {tile[0]} {tile[1]} {i} {x} {y}")
    if god == 'ap':
        if ap.ktora == 0:
            for tile in who.ownedTiles:
                if tile.typ == 'capital':
                    legalMoves.append(f"x {tile[0]} {tile[1]}")
    return legalMoves