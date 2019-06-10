from Player import Player
from Enemy import Enemy
from Room import Room
from Point import Point
from Item import Item

import operator
import random
Point.x = property(operator.itemgetter(0))
Point.y = property(operator.itemgetter(1))

class Game:
    SCREEN = None
    MAP = {}
    MAPDIMENSIONS = Point(25, 23)
    PLAYERSTARTPOSITION = Point(11, 11) #should be 11 11
    ENEMYSTARTPOSITION = Point(10, 7) #should b e 10 7
    VIEWPORTDIMENSIONS = Point(8,8)
    PLAYER = None
    ENEMY = None
    turn = 0
    gameRunning = True
    gameState = "INGAME"
    offeringPosition = None
    offeringCountdown = 6
    debugMessage = ""
    controlString = "Movement: [w][a][s][d] [p]ick up [i]nspect dr[o]p"
    def __init__(self):
        intro = "You have been selected to become one of the seven boys and seven girls to be sacrificed as tribute to the great King Minos. Your parents and community have told you that it is a great honor to be selected, but it does not make the red hot iron brand shaped like an M any less painful. You scratch the sizzling wound on your chest as you are led down a dark hallway by the kings men. You see a rope mechanism leading down into a large circular pit. You know the guards are there to make sure the sacrifices do not jump into the pit. To lose a sacrifice before it is ready will anger the gods. The kings men put you into a barrel and slowly lower you into the pit. You cannot see out of the barrel but you know you are going down. After hours of waiting, the rope holding the barrel snaps, and you and your barrel are sent hurtling down into the abyss.\n\nYou come to in a dark featureless room made entirely out of smooth black stone. There is no light, but somehow you are able to see your own hands. There is no ceiling, but the walls are far too tall and smooth to climb. In the distance, you can hear the echos of hooves on stone. You are not the only one here."
        print(intro)
        playerInput = input("Enter any input to continue:")
        self.MAP = self.initMap()
        self.initEdges()
        self.MAP[Point(9,7)].addToInventory(Item("TORCH"))
        self.MAP[Point(1,1)].addToInventory(Item("SEVEN"))
        self.MAP[Point(4,5)].addToInventory(Item("FIFTYTHREE"))
        self.MAP[Point(9,17)].addToInventory(Item("ONEHUNDREDANDTHREE"))
        self.MAP[Point(1,21)].addToInventory(Item("FORTYONE"))
        self.MAP[Point(11,1)].addToInventory(Item("ONEHUNDREDANDONE"))
        self.MAP[Point(11,13)].addToInventory(Item("ONEHUNDREDANDSEVEN"))
        self.MAP[Point(23,1)].addToInventory(Item("OFFERINGS"))
        self.MAP[Point(23,17)].addToInventory(Item("SHACKLES"))
        self.MAP[Point(23,7)].setGenericClue("You can make out the word 'Μῑνώταυρος' etched onto the floor.")
        self.MAP[Point(16,7)].setGenericClue("I dedicate this LABYRINTH to my beloved son.")
        self.MAP[Point(15,17)].setMastermindDoor()
        self.MAP[Point(16,17)].setMastermind(self.MAP[Point(15,17)])
        self.MAP[Point(12,5)].setAlphaDoor()
        self.MAP[Point(11,5)].setAlphaDoorClue(self.MAP[Point(12,5)])
        self.MAP[Point(23,11)].setCipherDoor()
        self.MAP[Point(23,10)].setCipherDoorClue(self.MAP[Point(23,11)])
        self.MAP[Point(11,21)].setExit()
        self.MAP[Point(14,15)].setPuzzleChest()
        self.initializePlayer()
        self.initializeEnemy()
        self.gameLoop()

    def gameLoop(self):
        self.debugMessage = "Starting game..."
        while self.gameRunning == True:
            print(self.PLAYER.position)
            print(self.debugMessage)
            print(self.generateViewport())
            print(self.MAP[self.PLAYER.position].getDescription())
            playerInput = input("Movement: [w][a][s][d] [p]ick up [i]nspect dr[o]p: ")
            self.handleInput(playerInput)
            self.initEdges()
            if self.ENEMY != None:
                self.doEnemyTurn()
                self.checkIfDead()
            if self.MAP[self.PLAYER.position].ROOMTYPE == "EXIT":
                self.win()

    def doEnemyTurn(self):
        short = None
        if self.offeringPosition != None:
            short = self.shortestPath(self.MAP[self.ENEMY.position], self.MAP[self.offeringPosition])
        else:
            short = self.shortestPath(self.MAP[self.ENEMY.position],self.MAP[self.PLAYER.position])
        if self.ENEMY.position != self.PLAYER.position:
            if len(short) > 1:
                self.moveEnemy(short[1])
        if self.offeringPosition != None and self.offeringCountdown > 0:
            if self.ENEMY.position == self.offeringPosition:
                self.offeringCountdown -= 1
        if self.offeringPosition != None and self.offeringCountdown == 0:
            self.offeringCountdown = 5
            offeringIndex = self.MAP[self.offeringPosition].hasItem("OFFERINGS")
            self.MAP[self.offeringPosition].inventory.pop(offeringIndex)
            self.offeringPosition = None

    def moveEnemy(self, newRoom):
        if self.turn % 2 == 0:
            self.MAP[self.ENEMY.position].enemyInRoom = False
            self.ENEMY.position = newRoom.position
            newRoom.enemyInRoom = True
            print("ENEMY moved to" + str(newRoom.position))

    def checkIfDead(self):
        if self.ENEMY.position == self.PLAYER.position:
            print("GAME OVER")
            self.gameRunning = False

    def handleInput(self, playerInput):
        playerInput = playerInput.lower()
        if playerInput == "quit":
            self.debugMessage = "Quitting the game..."
            self.gameRunning = False
            return
        if self.gameState == "INGAME":
            newPosition = self.PLAYER.position
            if playerInput == "a":
                newPosition += Point(0, -1)
                if self.movePlayer(newPosition):
                    self.endTurn()
            elif playerInput == "d":
                newPosition += Point(0, 1)
                if self.movePlayer(newPosition):
                    self.endTurn()
            elif playerInput == "w":
                newPosition += Point(-1, 0)
                if self.movePlayer(newPosition):
                    self.endTurn()
            elif playerInput == "s":
                newPosition += Point(1, 0)
                if self.movePlayer(newPosition):
                    self.endTurn()
            elif playerInput == "p":
                if self.pickUpItem():
                    self.endTurn()
            elif playerInput == "i":
                self.inspectItem()
            elif playerInput == "o":
                if self.dropItem():
                    self.endTurn()
            elif playerInput == "isopsephy" and self.MAP[self.PLAYER.position].ROOMTYPE == "CIPHERDOORCLUE":
                self.MAP[self.PLAYER.position].isopsephy()
                self.endTurn()
            elif playerInput == "guess" and self.MAP[self.PLAYER.position].ROOMTYPE == "MASTERMIND":
                self.MAP[self.PLAYER.position].mastermindGuess()
                self.endTurn()
            elif playerInput == "open" and self.MAP[self.PLAYER.position].ROOMTYPE == "PUZZLECHEST":
                self.MAP[self.PLAYER.position].chestGuess()
                self.endTurn()
            elif playerInput == "i am a weenie":
                self.weenie()
                self.endTurn()
            else:
                return


    def endTurn(self):
        self.turn += 1
        print("----------Turn End----------")

    def weenie(self):
        print("input [0] to move to tree puzzle")
        print ("input [1] to move to cipher puzzle")
        print("input [2] to move to binary puzzle")
        print("input [3] to move to permutation puzzle")
        print("input [4] to remove danger")
        validInput = False
        selectedChoice = None
        while validInput == False:
            playerInput = input("input:")
            if playerInput in ["0","1","2","3","4"]:
                validInput = True
                selectedChoice = playerInput
        if selectedChoice == "0":
            self.weenieTeleport(Point(11,5))
            self.PLAYER.addToInventory(Item("FORTYONE"))
            self.PLAYER.addToInventory(Item("SEVEN"))
            self.PLAYER.addToInventory(Item("FIFTYTHREE"))
            self.PLAYER.addToInventory(Item("ONEHUNDREDANDSEVEN"))
            self.PLAYER.addToInventory(Item("ONEHUNDREDANDONE"))
            self.PLAYER.addToInventory(Item("ONEHUNDREDANDTHREE"))
        if selectedChoice == "1":
            self.weenieTeleport(Point(23,10))
        if selectedChoice == "2":
            self.weenieTeleport(Point(14,15))
        if selectedChoice == "3":
            self.weenieTeleport(Point(16,17))
        if selectedChoice == "4":
            self.MAP[self.ENEMY.position].enemyInRoom = False
            self.ENEMY = None

    def weenieTeleport(self, newPosition):
        self.MAP[self.PLAYER.position].playerInRoom = False
        self.PLAYER.position = newPosition
        self.MAP[self.PLAYER.position].playerInRoom = True
        self.debugMessage = "You teleported to " + str(newPosition)

    def movePlayer(self, newPosition):
        if self.PLAYER.hasItem("SHACKLES"):
            rand = random.randint(0,3)
            if rand == 1:
                print("The cursed SHACKLES slow you down.")
                return False
        if self.PLAYER.position == newPosition:
            self.debugMessage = "You didn't move"
            return False
        if newPosition in self.MAP:
            if self.MAP[newPosition].walkable == True:
                self.MAP[self.PLAYER.position].playerInRoom = False
                self.PLAYER.position = newPosition
                self.MAP[self.PLAYER.position].playerInRoom = True
                self.debugMessage = "You moved to" + str(newPosition)
                return True
            else:
                if self.MAP[newPosition].ROOMTYPE == "SOLID":
                    self.debugMessage = "You bumped into a wall..."
                elif self.MAP[newPosition].ROOMTYPE in ["ALPHADOOR", "CIPHERDOOR", "MASTERMINDDOOR"]:
                    self.debugMessage = "You bumped into a door..."
                return False
        else:
            self.debugMessage = "DEBUG: ATTEMPTED TO MOVE OUT OF BOUNDS!"
            return False

    def initializePlayer(self):
        self.PLAYER = Player(self.PLAYERSTARTPOSITION)
        self.MAP[self.PLAYERSTARTPOSITION].playerInRoom = True

    def initializeEnemy(self):
        self.ENEMY = Enemy(self.ENEMYSTARTPOSITION)
        self.MAP[self.ENEMYSTARTPOSITION].enemyInRoom = True

    def generateViewport(self):
        upperLeftBound = self.PLAYER.position + Point(-3, -3)
        lowerRightBound = self.PLAYER.position + Point(4, 4)
        mapString = self.printMap(upperLeftBound, lowerRightBound)
        return mapString

    def pickUpItem(self):
        if len(self.MAP[self.PLAYER.position].inventory) == 0:
            print("Nothing to pick up...")
            return False
        if len(self.MAP[self.PLAYER.position].inventory) == 1:
            item = self.MAP[self.PLAYER.position].getItem(0)
            self.PLAYER.addToInventory(item)
            print("You picked up a " + item.NAME)
            return True
        validInput = False
        while validInput == False:
            playerInput = input("Enter the index of the item you wish to pick up: ")
            if playerInput.isnumeric() == True:
                if 0 <= int(playerInput) < len(self.MAP[self.PLAYER.position].inventory):
                    validInput = True
                else:
                    print("Not a valid index. Item not found")
                    return False
            else:
                print("Not a valid number.")
                return False
        itemIndex = int(playerInput)
        item = self.MAP[self.PLAYER.position].getItem(itemIndex)
        self.PLAYER.addToInventory(item)
        print("You picked up a " + item.NAME)
        return True

    def dropItem(self):
        if len(self.PLAYER.inventory) == 0:
            print("Nothing to drop...")
            return False
        validInput = False
        while validInput == False:
            playerInput = input("Enter the index of the item in your inventory you wish to drop: ")
            if playerInput.isnumeric() == True:
                if 0 <= int(playerInput) < len(self.PLAYER.inventory):
                    validInput = True
                else:
                    print("Not a valid index. Item not found")
                    return False
            else:
                print("Not a valid number.")
                return False
        itemIndex = int(playerInput)
        item = self.PLAYER.getItem(itemIndex)
        if item.value != None:
            print("You inserted " + item.NAME + " into the door...")
            self.MAP[self.PLAYER.position].addToInventory(item)
            return True
        elif item.NAME == "OFFERINGS":
            if self.offeringPosition == None:
                print("You have placed the OFFERINGS on the floor. RUN.")
                self.offeringPosition = self.PLAYER.position
                self.MAP[self.PLAYER.position].addToInventory(item)
                return True
            else:
                print("You have already placed OFFERINGS.")
                return False
        elif item.NAME == "SHACKLES":
            print("You can't drop these SHACKLES. They appear to be cursed.")
            return False
        else:
            print("You have dropped " + item.NAME + " on the floor...")
            self.MAP[self.PLAYER.position].addToInventory(item)
            return True

    def inspectItem(self):
        if len(self.PLAYER.inventory) == 0:
            print("Nothing to inspect...")
            return
        validInput = False
        while validInput == False:
            playerInput = input("Enter the index of the item in your inventory you wish to inspect: ")
            if playerInput.isnumeric() == True:
                if 0 <= int(playerInput) < len(self.PLAYER.inventory):
                    validInput = True
                else:
                    print("Not a valid index. Item not found")
                    return
            else:
                print("Not a valid number.")
                return
        itemIndex = int(playerInput)
        item = self.PLAYER.inventory[itemIndex]
        print("Description: " + item.description)

    def printMap(self, upperLeftBound, lowerRightBound):
        mapString = ""
        row = 0
        dist = self.dijkstra(self.MAP[self.PLAYER.position], self.makeWalkableRoomsSet())
        for room in self.MAP.values():
            room.isHidden = True
        for x in range(upperLeftBound.x, lowerRightBound.x):
            for y in range(upperLeftBound.y, lowerRightBound.y):
                if Point(x,y) in self.MAP:
                    if self.MAP[Point(x,y)] in dist:
                        vision = dist[self.MAP[Point(x,y)]]
                        if vision <= self.PLAYER.getVisionRadius():
                            self.MAP[Point(x,y)].isHidden = False
                            adjacents = [(0,1),(0,-1),(1,0),(-1,0), (1,1), (-1,-1), (1, -1), (-1,1)]
                            for adjacent in adjacents:
                                newPosition = Point(x,y) + adjacent
                                if newPosition in self.MAP:
                                    if self.MAP[newPosition].walkable == False:
                                        self.MAP[newPosition].isHidden = False
        for x in range(upperLeftBound.x,lowerRightBound.x):
            lineString = ""
            for y in range(upperLeftBound.y,lowerRightBound.y):
                if Point(x,y) in self.MAP:
                    distance = self.PLAYER.position - Point(x,y)

                    #print(Point(x,y))
                    visionRadius = self.PLAYER.getVisionRadius()
                    # if distance.x <= visionRadius and distance.x >= visionRadius * -1:
                    #     if distance.y <= visionRadius and distance.y >= visionRadius * -1:
                    #         self.MAP[Point(x,y)].isHidden = False
                    lineString += self.MAP[Point(x,y)].getRoomChar()
                else:
                    lineString += "\u2591"
            if row == 0:
                lineString += " Turn: " + str(self.turn)
            if row == 2:
                lineString += " Items in room:" + self.MAP[self.PLAYER.position].getInventoryString()
            if row == 3:
                lineString += " Inventory:" + self.PLAYER.getInventoryString()
            lineString += "\n"
            mapString += lineString
            row += 1
        return mapString

    @staticmethod
    def initMap():
        intMap = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0],
            [0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0],
            [0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0],
            [0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0],
            [0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0],
            [0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0],
            [0,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0],
            [0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0],
            [0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0],
            [0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0],
            [0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0],
            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],]
        newDict = {}
        for x in range(len(intMap)):
            for y in range(len(intMap[x])):
                if intMap[x][y] == 0:
                    newDict[(x,y)] = Room(Point(x,y), "SOLID")
                if intMap[x][y] == 1:
                    newDict[(x,y)] = Room(Point(x,y), "EMPTY")
        return newDict

    def initEdges(self):
        for room in self.MAP.values():
            self.setEdges(room)

    def setEdges(self, currentRoom):
        adjacents = [(0,1),(1,0),(-1,0),(0,-1)]
        edges = []
        for adjacent in adjacents:
            newPosition = currentRoom.position + adjacent
            if (newPosition) in self.MAP:
                if self.MAP[newPosition].walkable == True:
                    edges.append(self.MAP[newPosition])
        currentRoom.edges = edges

    def makeWalkableRoomsSet(self):
        nodes = set()
        for room in self.MAP.values():
            if room.walkable:
                nodes.add(room)
        return nodes

    #adapted from https://gist.github.com/econchick/4666413
    def dijkstra(self, startNode, walkableRooms):
        visited = {startNode: 0}
        path = {}
        rooms = walkableRooms
        while rooms:
            minNode = None
            for node in rooms:
                if node in visited:
                    if minNode is None:
                        minNode = node
                    elif visited[node] < visited[minNode]:
                        minNode = node
            if minNode is None:
                break
            rooms.remove(minNode)
            current_weight = visited[minNode]
            for edge in minNode.edges:
                weight = current_weight + 1
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = minNode
        return visited

    def shortestPath(self, start, end):
        dist = self.dijkstra(start, self.makeWalkableRoomsSet())
        if end not in dist:
            return []
        def dfs(v, path = []):
            if v == start:
                return path
            distv = dist[v]
            for e in v.edges:
                if dist[e] < distv:
                    return dfs(e, path + [e])
        shortest = dfs(end, [end])
        shortest.reverse()
        return shortest

    def win(self):
        wintext = "The door opens and you climb the spiral staircase. You look down and see the walls of the LABYRINTH extending outwards in every direction into darkness. You do not know how tall this staircase is, but the sound of hooves on stone below motivates you to keep climbing. \n\nAfter what feels like many days of climbing the spiral staircase without rest, you feel wind for the first time. You continue to climb higher and higher until you are blinded by light.\n\nYou emerge the cave not far from home. You can smell the salt and hear the sea crashing against the rocks.\n\nTaking on a new identity, you sail far away from Crete. Sometimes, late at night, you wonder if the brand of sacrifice is permanent. Sometimes, just before you fall asleep, you can still hear the sound of hooves on stone.\n\n\nTHE END"
        print(wintext)
        self.gameRunning = False


#run praugram
game = Game()
