import random as rnd
import itertools as it
import copy

# stuff

BAMBOO = 0
DOTS = 1
CHARACTER = 2
SUITE = [DOTS, BAMBOO, CHARACTER]

HONOR = 3

EAST = 4
SOUTH = 5
WEST = 6
NORTH = 7
RED = 8
GREEN = 9 
WHITE = 10

PLAYERS = [1,2,3,4]

longnames = {
    BAMBOO: 'BAMBOO',
    DOTS: 'DOTS',
    CHARACTER: 'CHARACTER',

    HONOR: "HONOR",
    EAST: "EAST",
    SOUTH: "SOUTH",
    WEST: "WEST",
    NORTH: "NORTH",
    RED: "RED",
    GREEN: " GREEN ",
    WHITE: "WHITE",
}

shortnames = {
    BAMBOO: 'BA',
    DOTS: 'DT',
    CHARACTER: 'CH',

    HONOR: "HR",
    EAST: "E ",
    SOUTH: "S ",
    WEST: "W ",
    NORTH: "N ",
    RED: "RD",
    GREEN: "GD",
    WHITE: "WD",
}


"""
+-----+ +-----+ +-----+ +-----+
|     | |     | |     | |     |
|  N  | |  E  | |  S  | |  W  |
|     | |     | |     | |     |
+-----+ +-----+ +-----+ +-----+


+-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ 
|  -  | |  O  | |  O  | | O O | | O O | | 8 O | | OOO | |  -  | |  -  | |  -  | 
| |.| | |     | |  O  | |     | |  O  | |     | | OOO | | |.| | | |.| | | |.| | 
|  -  | |  O  | |  O  | | O O | | O O | | 8 8 | | OOO | |  -  | |  -  | |  -  | 
+-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ 


+------------------
|  
| (.) (.)
|  )   (
  (  v  )
   | | |
|
|
|
|
|
|




"""

class Mahjong:

    def __init__(self):
        self.game = {
            'deck': [],
            'graveyard': [],
            'player' : {
                1: [],
                2: [],
                3: [],
                4: [],
            }
        }
        self.activePlayer = 0

    def getDeck(self):
        return self.game['deck']    

    def getGraveyard(self):
        return self.game['graveyard']

    def getPlayerHand(self):
        return self.game['player'][self.activePlayer]

    def getActivePlayer(self):
        return self.activePlayer

    def fullDeck(self):
        deck = []
        for (i,s, _) in it.product(range(1,10), SUITE, range(0,4)):
            deck.append((i, s))
        for (i, _) in it.product(range(EAST, WHITE+1), range(0,4)):
            deck.append((i, HONOR))
        return deck

    def printGameCheat(self):
        print("deck:" + str(len(self.game['deck'])))
        self.printTiles(self.game['deck'])
        for p in PLAYERS:
            print("player: " + str(p) + "  - " + str(len(self.game['player'][p])))
            self.printTiles(sorted(self.game['player'][p], key=lambda x: (x[1], x[0])))
        self.printGame()
        
    def printGame(self):
        print("graveyard:" + str(len(self.game['graveyard'])))
        self.printTiles(self.game['graveyard'])
        print("current hand:")
        hand = sorted(self.game['player'][self.activePlayer], key=lambda x: (x[1], x[0]))
        self.printHand(hand)

    def printHand(self, hand):
        for (i, t) in zip(range(1,len(hand)+1), hand):
            print(str(i) + ":"),
            self.printTile(t)
            print


    def printTiles(self, tiles):
        for tile in tiles:
            self.printTile(tile, short = True)
        print

    def printTile(self, tile, short = True):
        if short:
            names = shortnames
        else:
            names = longnames

        (num, suite) = tile
        if suite == HONOR:
            print("[" + names[num] + "|" + names[HONOR] + "]"),
        else:
            print("[" + str(num) + " |" + names[suite] + "]"),

    # def pictureTile(self, tile):
    #     return pic

    def rollDice(self):
        return rnd.randint((1,6))

    def setActivePlayer(self, p):
        self.activePlayer = p
        print('player set: ' + str(p))

    def startGame(self):
        self.game['deck'] = self.fullDeck()
        rnd.shuffle(self.game['deck'])

        for p in PLAYERS:
            self.game['player'][p] = self.game['deck'][0:13]
            self.game['deck'] = self.game['deck'][13:]


        print("game start") 

    def drawTile(self):
        tile = self.game['deck'].pop(0)
        self.game['player'][self.activePlayer].append(tile)
        return tile

    def stealTile(self, p):
        print('pong move made')    

    def isGameOver(self):
        return (len(self.game['deck']) <= 0)

    def throwTile(self, tile):
        index = self.game['player'][self.activePlayer].index(tile)
        t = self.game['player'][self.activePlayer].pop(index)
        self.game['graveyard'].append(t)

        print("you threw tile:"),
        self.printTile(t)
        print("away")

        self.activePlayer = self.activePlayer % 4 + 1

    def isWining(self):
        hand = self.game['player'][self.activePlayer]
        sols = self.findeyes(hand)
        return (sols != [])
    


    def findeyes(self, hand):
        # eyes = [ ]
        solutions = []
        # hand = self.game['player'][self,activePlayer]
        # look for all pair
        # self.printTiles(hand)
        for tile in hand: 
            eyes_index = [i for i,t in enumerate(hand) if t == tile]
            # print (eyes_index)
            if len(eyes_index) >= 2: 
                h_temp = copy.copy(hand)
                for i in xrange(0,2):
                    h_temp.remove(tile)   

                tps = self.findtriples(h_temp)
                if tps != []:
                    solutions = solutions + [l + [tile, tile] for l in tps]

        return solutions

    def findtriples(self, hand):
        # if triples_needed <= 0:
        #     return []
        solutions = []
        for tile in hand:
            triple_index = [ i for i,t in enumerate(hand) if t == tile]
            if len(triple_index) >= 3:
                triple = [tile,tile,tile]
                h_temp = copy.copy(hand)
                for i in range(0,3):
                    h_temp.remove(tile)
                    
                tps = self.findtriples(h_temp)

                if len(hand) == 3: # kongs will be different here
                    solutions = [triple]
                elif tps != []:
                    # print(">>")
                    # print tps
                    # print triple
                    solutions = solutions + [l + triple for l in tps]          
        
        # if foundTriples == False:
        # find increasing
        for tile in hand:
            (num, suite) = tile
            if suite != HONOR:
                below_index = [i for i,(n,s) in enumerate(hand) if (s == suite and n == num - 1)] 
                above_index = [i for i,(n,s) in enumerate(hand) if (s == suite and n == num + 1)]
                if (len(below_index) >= 1 & len(above_index) >= 1):
                    tile_below = hand[below_index[0]]
                    tile_above = hand[above_index[0]]

                    increasing = [tile_below, tile, tile_above]
                    h_temp = copy.copy(hand)

                    h_temp.remove(tile_below)
                    h_temp.remove(tile)
                    h_temp.remove(tile_above)
                    
                    tps = self.findtriples(h_temp)

                    if len(hand) == 3: # kongs will be different here
                        solutions = [increasing]
                    elif tps != []:
                        solutions = solutions + [l + increasing for l in tps]    

        return solutions
        



if __name__ == "__main__":

    game = Mahjong()
    game.startGame()
    game.setActivePlayer(1)

    while(not game.isGameOver()):
        tile = game.drawTile()
        game.printGame()
        # # game.printGameCheat()

        ap = game.getActivePlayer()
        # print("you are player: " + str(ap))

        hand = game.getPlayerHand()
        # n = len(hand)
        print("is winning?")
        print(game.isWining())
        # tilenum = 0
        # while (tilenum <= 0 or tilenum > n):
        #     print("Enter a number between 1 and " + str(n))
        #     # game.printHand(hand)
        #     tilenum = input()
        
        tilenum = 1
        tile = hand[tilenum - 1]
        game.throwTile(tile)
        

    print("testing:")

    hand = [
        (1, BAMBOO),
        (2, BAMBOO),
        (3, BAMBOO),

        (3, BAMBOO),
        (2, BAMBOO),
        (4, BAMBOO),

        (4, BAMBOO),
        (4, BAMBOO),
        (4, BAMBOO),

        (6, BAMBOO),
        (5, BAMBOO),
        (7, BAMBOO),

        (8, BAMBOO),
        (8, BAMBOO),
        ]

    s = game.findeyes(hand)
    print(s)
        # break


    


    


    

