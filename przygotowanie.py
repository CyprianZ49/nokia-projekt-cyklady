from plansza import Plansza
#temporary twarde warunki pocz na 5 graczy
def przypiszWarunkiStartowe(board, players, ilosc):
    # board.changeOwnership(7, 6, players[0])
    # board.pola[7][6].strength+=1
    if ilosc > 0:
        board.changeOwnership(1, 1, players[0]) # water
        board.pola[1][1].strength+=1
        board.changeOwnership(3, 3, players[0]) # land
        board.pola[3][3].strength+=1
        board.changeOwnership(9, 9, players[0]) # water
        board.pola[9][9].strength+=1
        board.changeOwnership(9, 10, players[0]) #land
        board.pola[9][10].strength+=1
    if ilosc > 1:
        board.changeOwnership(6, 1, players[1]) # water
        board.pola[6][1].strength+=1
        board.changeOwnership(5, 3, players[1]) # land
        board.pola[5][3].strength+=1
        board.changeOwnership(5, 6, players[1]) # water
        board.pola[5][6].strength+=1
        board.changeOwnership(6, 7, players[1]) # land
        board.pola[6][7].strength+=1
    if ilosc > 2:
        board.changeOwnership(10, 5, players[2])
        board.pola[10][5].strength+=1
        board.changeOwnership(9, 5, players[2])
        board.pola[9][5].strength+=1
        board.changeOwnership(3, 6, players[2])
        board.pola[3][6].strength+=1
        board.changeOwnership(3, 7, players[2])
        board.pola[3][7].strength+=1
    if ilosc > 3:
        board.changeOwnership(10, 7, players[3])
        board.pola[10][7].strength+=1
        board.changeOwnership(10, 8, players[3])
        board.pola[10][8].strength+=1
        board.changeOwnership(2, 4, players[3])
        board.pola[2][4].strength+=1
        board.changeOwnership(1, 6, players[3])
        board.pola[1][6].strength+=1
    if ilosc > 4:
        board.changeOwnership(7, 6, players[4])
        board.pola[7][6].strength+=1
        board.changeOwnership(8, 7, players[4])
        board.pola[8][7].strength+=1
        board.changeOwnership(7, 10, players[4])
        board.pola[7][10].strength+=1
        board.changeOwnership(5, 9, players[4])
        board.pola[5][9].strength+=1