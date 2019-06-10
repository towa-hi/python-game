from Item import Item
import random

class Room:
    unsafe_hash = True

    def __init__(self, position, roomtype):
        self.linkedDoor = None
        self.description = "A featureless hallway..."
        self.position = position
        self.walkable = True
        self.ROOMTYPE = roomtype
        self.playerInRoom = False
        self.enemyInRoom = False
        self.isHidden = True
        self.alphaDoorInserted = []
        self.inventory = []
        if self.ROOMTYPE == "SOLID":
            self.walkable = False
        if self.ROOMTYPE == "ALPHADOOR":
            self.setAlphaDoor()
        #edges
        self.edges = []
        self.skullkeys = ["R","G","B","Y","W","P"]
        self.answer = None
        self.clue = ["?","?","?","?","?","?"]
        self.switches = ["\u2580","\u2580","\u2580","\u2580","\u2580"]
        self.chestAnswer = ["\u2584","\u2580","\u2584","\u2584","\u2580"]
        if self.ROOMTYPE == "MASTERMIND":
            self.setMastermind()


    def setEdges(self, edges):
        self.edges = edges

    def printEdges(self):
        print(self.edges)

    def __hash__(self):
        return hash(self.position)

    def __eq__(self, other):
        return self.position == other.position

    def getRoomChar(self):

        if self.playerInRoom == True:
            return "@"
        if self.isHidden == True:
            return "\u2591"
        if self.enemyInRoom == True:
            return "&"
        if self.ROOMTYPE == "DOOR":
            return "D"
        if self.ROOMTYPE == "SOLID":
            return "\u2588"
        if self.ROOMTYPE == "ALPHADOORCLUE":
            return "a"
        if self.ROOMTYPE == "ALPHADOOR":
            return "A"
        if self.ROOMTYPE == "CIPHERDOORCLUE":
            return "b"
        if self.ROOMTYPE == "CIPHERDOOR":
            return "B"
        if self.ROOMTYPE == "PUZZLECHEST":
            return "n"
        if self.ROOMTYPE == "MASTERMIND":
            return "c"
        if self.ROOMTYPE == "MASTERMINDDOOR":
            return "C"
        if self.ROOMTYPE == "CLUE":
            return "?"
        if self.ROOMTYPE == "EXIT":
            return "X"
        if len(self.inventory) != 0:
            return "*"
        return " "

    def getInventoryString(self):
        inventoryString = ""
        for x in range(len(self.inventory)):
            inventoryString += " " + str(x) + ":" + self.inventory[x].getNameString()
        if inventoryString == "":
            inventoryString += " nothing"
        return inventoryString

    def addToInventory(self, item):
        self.inventory.append(item)
        if self.ROOMTYPE == "ALPHADOORCLUE":
            if item.value != None:
                if self.checkAlphaDoorAnswer():
                    self.activateDoor()

    def getItem(self, itemIndex):
        item = None
        if 0 <= itemIndex < len(self.inventory):
            item = self.inventory.pop(itemIndex)
        return item

    def setAlphaDoor(self):
        self.ROOMTYPE = "ALPHADOOR"
        self.walkable = False

    def setCipherDoor(self):
        self.ROOMTYPE = "CIPHERDOOR"
        self.walkable = False

    def hasItem(self, itemName):
        for x in range(len(self.inventory)):
            if self.inventory[x].NAME == itemName:
                return True
        return False

    def getDescription(self):
        if self.ROOMTYPE == "ALPHADOORCLUE":
            NINETYSEVENSTRING = "★ "
            FORTYONESTRING = "★ "
            ONEHUNDREDANDSEVENSTRING = " ★ "
            SEVENSTRING = "★"
            FIFTYSEVENSTRING = "★ "
            ONEHUNDREDANDONESTRING = " ★ "
            ONEHUNDREDANDTHREESTRING = " ★ "
            starStrings = [NINETYSEVENSTRING, FORTYONESTRING, ONEHUNDREDANDSEVENSTRING, SEVENSTRING, FIFTYSEVENSTRING, ONEHUNDREDANDONESTRING, ONEHUNDREDANDTHREESTRING]
            count = 0
            for item in self.inventory:
                if item.value != None:
                    starStrings[count] = str(item.value)
                    count += 1
            description = "You see a diagram carved onto the door\n"
            description += "    {}\n".format(starStrings[0])
            description += "   /  \\\n"
            description += "  {}   {}\n".format(starStrings[1], starStrings[4])
            description += " / \\   /\n"
            description += "{} {}{}\n".format(starStrings[2], starStrings[3], starStrings[5])
            description += "       \\\n"
            description += "       {} \n".format(starStrings[6])
            self.description = description
        if self.ROOMTYPE == "PUZZLECHEST":
            description = "In the middle of the room is a locked chest. It can only be [open]ed by manipulating the eight switches on top to make the 'value of the architect's name'.\n"
            description += str(self.switches)
            self.description = description
        if self.ROOMTYPE == "RANDOMDOORCLUE":
            description = "This door has a mechanism built into it. Pulling a lever will do something."
        if self.ROOMTYPE == "CIPHERDOORCLUE":
            description = "This door is locked with a combination lock with four digits. Carved onto the door is the word '[ISOPSEPHY]'."
            self.description = description
            #Μῑνώταυρος
            #M = 40
            #ῑ = 10
            #ν = 50
            #ώ = 800
            #τ = 300
            #α = 1
            #υ = 400
            #ρ = 100
            #ο - 70
            #ς = 200
            #answer = 1971
        if self.ROOMTYPE == "MASTERMIND":
            self.description = "This door will not open until a six letter word has been entered. All you can do is [guess]\n"
            self.description += str(self.clue)
        if self.hasItem("OFFERINGS"):
            self.description = "Do not linger here."
        return self.description

    def setPuzzleChest(self):
        self.ROOMTYPE = "PUZZLECHEST"


    def setRandomDoorClue(self, linkedDoor):
        self.linkedDoor = linkedDoor
        self.ROOMTYPE = "RANDOMDOORCLUE"
    def setCipherDoorClue(self, linkedDoor):
        self.linkedDoor = linkedDoor
        self.ROOMTYPE = "CIPHERDOORCLUE"

    def setAlphaDoorClue(self, linkedDoor):
        self.linkedDoor = linkedDoor
        self.ROOMTYPE = "ALPHADOORCLUE"
        self.addToInventory(Item("NINETYSEVEN"))
        #     97
        #    /  \
        #   41   107
        #  / \   /
        # 7  53 101
        #        \
        #        103

    def checkAlphaDoorAnswer(self):
        answerKey = [97,41,7,53,107,101,103]
        answerKeyAlt = [97,41,7,53,103,101,107]
        answerList = []
        for item in self.inventory:
            if item.value != None:
                answerList.append(item.value)
        if answerKey == answerList or answerKeyAlt == answerList:
            return True
        else:
            return False

    def checkCipherDoorAnswer(self, sum):
        if sum == 9971:
            self.activateDoor()

    def activateDoor(self):
        self.linkedDoor.openDoor()
        if self.ROOMTYPE == "ALPHADOORCLUE":
            self.ROOMTYPE = "EMPTY"
            newInventory = []
            for item in self.inventory:
                if item.value == None:
                    newInventory.append(item)
            self.inventory = newInventory
            self.description = "There was a diagram here. It's gone now..."
        print("The door has opened...")

    def setAlphaDoor(self):
        self.ROOMTYPE = "ALPHADOOR"
        self.walkable = False

    def setExit(self):
        self.ROOMTYPE = "EXIT"
        self.walkable = True

    def setRandomDoor(self):
        self.ROOMTYPE = "RANDOMDOOR"
        self.walkable = False

    def openDoor(self):
        self.walkable = True
        self.ROOMTYPE = "EMPTY"
        self.description = "There was a door here. It's gone now..."

    def isopsephy(self):
        combo = [None,None,None,None]
        invalidInputString = "Not a valid number between [0] and [9]"
        nums = ["0","1","2","3","4","5","6","7","8","9"]
        while combo[0] == None:
            playerInput = input("Enter the first digit (between [0] and [9]):")
            if playerInput in nums:
                combo[0] = int(playerInput)
            else:
                print(invalidInputString)
        while combo[1] == None:
            playerInput = input("Enter the second digit (between [0] and [9]):")
            if playerInput in nums:
                combo[1] = int(playerInput)
            else:
                print(invalidInputString)
        while combo[2] == None:
            playerInput = input("Enter the third digit (between [0] and [9]):")
            if playerInput in nums:
                combo[2] = int(playerInput)
            else:
                print(invalidInputString)
        while combo[3] == None:
            playerInput = input("Enter the fourth digit (between [0] and [9]):")
            if playerInput in nums:
                combo[3] = int(playerInput)
            else:
                print(invalidInputString)
        self.checkIsopsephy(combo)

    def checkIsopsephy(self, combo):
        if combo == [1,9,7,1]:
            print("The door has opened...")
            self.linkedDoor.openDoor()
            self.ROOMTYPE = "EMPTY"
            self.description = "There was a lock here. It's gone now..."
        else:
            print("Nothing seems to have happened...")

    def setMastermind(self, linkedDoor):
        self.linkedDoor = linkedDoor
        self.ROOMTYPE = "MASTERMIND"
        self.answer = "ICARUS"
        self.description = self.clue

    def mastermindGuess(self):
        validInput = False
        while validInput == False:
            playerInput = input("Enter a six lettered word:").upper()
            if len(playerInput) != len(self.answer):
                print("Only a six lettered word will open this door...")
                validInput = False
            else:
                validInput = True
        solvedNum = 0
        for index in range(6):
            if playerInput[index] == self.answer[index]:
                self.clue[index] = playerInput[index]
                solvedNum += 1
            elif playerInput[index] in self.answer:
                self.clue[index] = "!"
            else:
                self.clue[index] = "?"
        if solvedNum == 6:
            self.linkedDoor.openDoor()
            self.ROOMTYPE = "EMPTY"
            self.description = "There was a lock here. It's gone now..."
            print("The door opens...")

    def setMastermindDoor(self):
        self.ROOMTYPE = "MASTERMINDDOOR"
        self.walkable = False

    def chestGuess(self):
        validInput = False
        activatedSwitch = None
        while validInput == False:
            playerInput = input("Enter the index of the switch you wish to activate [0] - [4]:")
            if playerInput not in ["0","1","2","3","4"]:
                print("Invalid input. Not a number between [0] and [4]")
            else:
                validInput = True
                activatedSwitch = int(playerInput)
        if activatedSwitch != None:
            if self.switches[activatedSwitch] == "\u2584":
                self.switches[activatedSwitch] = "\u2580"
            else:
                self.switches[activatedSwitch] = "\u2584"
        if self.switches == self.chestAnswer:
            print("The chest opened. Inside was a BIG TORCH.")
            self.ROOMTYPE = "EMPTY"
            self.description = "There was a chest here. It's gone now"
            self.addToInventory(Item("BIG TORCH"))
#idea: cursed key. holding this will have a 33% chance to negate a movement
#idea:
    def hasItem(self, itemName):
        itemIndex = None
        for index in range(len(self.inventory)):
            if self.inventory[index].NAME == itemName:
                itemIndex = index
        return itemIndex

    def setGenericClue(self, string = None):
        self.ROOMTYPE = "CLUE"
        if self.hasItem("OFFERINGS"):
            self.description = "Do not linger here."
        if string != None:
            self.description = string
