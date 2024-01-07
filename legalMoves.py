def getMetropolis(board, who):
    metro = 0
    for tile in who.ownedTiles:
        if board.pola[tile[0]][tile[1]].typ == 'capital' and board.pola[tile[0]][tile[1]].isMetropolis == True:
            metro += 1
    return metro

def getIslands(board, who):
    island = 0
    for tile in who.ownedTiles:
        if board.pola[tile[0]][tile[1]].typ == 'capital':
            island += 1
    return island

def getLegalMoves(board, who, god, at, ze, po, ar, ap):
    legalMoves = []
    if board.isFight:
        if board.mayReatreat != who:
            return legalMoves
        legalMoves.append(f"0")
        if board.pola[board.whereFight[0]][board.whereFight[1]].typ == 'water':
            for x in range(13):
                for y in range(13):
                    if board.pola[x][y].typ == 'water' and board.isNeightbour(board.whereFight[0], board.whereFight[1], x, y) and (board.pola[x][y].owner == board.pusty or board.pola[x][y].owner == who):
                        legalMoves.append(f"1 {x} {y}")
        else:
            for x in range(13):
                for y in range(13):
                    if board.pola[x][y].typ == 'capital' and board.isBridge(board.whereFight[0], board.whereFight[1], who, x, y) and (board.pola[x][y].owner == board.pusty or board.pola[x][y].owner == who):
                        legalMoves.append(f"1 {x} {y}")
    if board.turn != who: #checking if it's this players turn
        return legalMoves
    if who.isBuildingMetropolis:
        if who.philosophers == 4: #building Metropolis using philosophers
            for tile in who.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ == 'capital' and board.pola[tile[0]][tile[1]].isMetropolis == False:
                    legalMoves.append(f"{tile[0]} {tile[1]}")
        else: #building Metropolis using buildings
            validIsalnds = []
            validBuildings = []
            for i in range(5):
                validBuildings.append([])
            for tile in who.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ == 'capital':
                    if board.pola[tile[0]][tile[1]].isMetropolis == False:
                        validIsalnds.append(tile)
                    for i in range(0, len(board.pola[tile[0]][tile[1]].buildings)):
                        validBuildings[board.pola[tile[0]][tile[1]].buildings[i]].append((tile[0], tile[1], i))
            for targetIsland in validIsalnds:
                for b1 in validBuildings[1]:
                    for b2 in validBuildings[2]:
                        for b3 in validBuildings[3]:
                            for b4 in validBuildings[4]:
                                legalMoves.append(f"{b1[0]} {b1[1]} {b1[2]} {b2[0]} {b2[1]} {b2[2]} {b3[0]} {b3[1]} {b3[2]} {b4[0]} {b4[1]} {b4[2]} {targetIsland[0]} {targetIsland[1]}")

    #specific gods
    legalMoves.append(f"p")
    if god == "at":
        #build
        if who.coins >= 2:
            for tile in who.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ == 'capital':
                    for i in range(0, len(board.pola[tile[0]][tile[1]].buildings)):
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
                if board.pola[tile[0]][tile[1]].typ == 'capital':
                    for i in range(0, len(board.pola[tile[0]][tile[1]].buildings)):
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
                    if (board.pola[x][y].typ == 'capital' or board.pola[x][y].typ == 'water') and board.pola[x][y].strength > 0:
                        legalMoves.append(f"m {x} {y}")
    if god == 'po':
        #build
        if who.coins >= 2:
            for tile in who.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ == 'capital':
                    for i in range(0, len(board.pola[tile[0]][tile[1]].buildings)):
                        legalMoves.append(f"b {tile[0]} {tile[1]} {i}")
        #recruit
        koszt = 0
        if po.ktora > 0:
            koszt += po.ktora
        if po.ktora < 4 and who.coins >= koszt:
            for x in range(13):
                for y in range(13):
                    if board.pola[x][y].typ == 'water' and (board.pola[x][y].owner == who or board.pola[x][y].owner == board.pusty):
                        test = False
                        for tile in who.ownedTiles:
                            if board.pola[tile[0]][tile[1]].typ=='capital' and board.isNeightbour(tile[0], tile[1], x, y):
                                test = True
                        if test:
                            legalMoves.append(f"r {x} {y}")
        #move
        for tile in who.ownedTiles:
            if board.pola[tile[0]][tile[1]].typ == 'water':
                koszt = 1
                if po.lastMovex == tile[0] and po.lastMovey == tile[1] and po.ileRuch<3:
                    koszt = 0
                if who.coins + who.actionDiscount >= koszt:
                    for x in range(13):
                        for y in range(13):
                            if board.pola[x][y].typ == 'water' and board.isNeightbour(tile[0], tile[1], x, y):
                                for i in range(1, board.pola[tile[0]][tile[1]].strength+1):
                                    legalMoves.append(f"m {tile[0]} {tile[1]} {i} {x} {y}")
    if god == 'ar':
        #build
        if who.coins >= 2:
            for tile in who.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ == 'capital':
                    for i in range(0, len(board.pola[tile[0]][tile[1]].buildings)):
                        legalMoves.append(f"b {tile[0]} {tile[1]} {i}")
        #recruit
        koszt = 0
        if ar.ktora > 0:
            koszt += ar.ktora + 1
        if po.ktora < 4 and who.coins >= koszt:
            for tile in who.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ == 'capital':
                    legalMoves.append(f"r {tile[0]} {tile[1]}")
        #move
        metro = getMetropolis(board, who)
        if who.coins + who.actionDiscount > 0:
            for tile in who.ownedTiles:
                if board.pola[tile[0]][tile[1]].typ == 'capital':
                    for x in range(13):
                        for y in range(13):
                            if board.pola[x][y].typ == 'capital' and (x, y) != tile and board.isBridge(tile[0], tile[1], who, x, y):
                                enemy = board.pola[x][y].owner
                                enemyIsalnds = getIslands(board, enemy)
                                if enemy == who or metro > 1 or enemyIsalnds > 1:
                                    for i in range(1, board.pola[tile[0]][tile[1]].strength + 1):
                                        legalMoves.append(f"m {tile[0]} {tile[1]} {i} {x} {y}")
    if god == 'ap':
        if who not in ap.wykonane:
            if ap.ktora == 0:
                for tile in who.ownedTiles:
                    if board.pola[tile[0]][tile[1]].typ == 'capital':
                        legalMoves.append(f"x {tile[0]} {tile[1]}")
            else:
                legalMoves.append(f"x")
    return legalMoves