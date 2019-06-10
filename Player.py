from Item import Item
#bug double endturn
class Player:
    DEFAULTVISIONRADIUS = 1
    position = None
    inventory = []
    def __init__(self, PLAYERSTARTPOSITION):
        self.position = PLAYERSTARTPOSITION
        self.addToInventory(Item("POCKET LINT"))
        # self.addToInventory(Item("FORTYONE"))
        # self.addToInventory(Item("SEVEN"))
        # self.addToInventory(Item("FIFTYTHREE"))
        # self.addToInventory(Item("ONEHUNDREDANDSEVEN"))
        # self.addToInventory(Item("ONEHUNDREDANDONE"))
        # self.addToInventory(Item("ONEHUNDREDANDTHREE"))
        # self.addToInventory(Item("BIG TORCH"))
    def getVisionRadius(self):
        visionRadius = self.DEFAULTVISIONRADIUS
        for item in self.inventory:
            if item.NAME == "BIG TORCH":
                return visionRadius + 2
            if item.NAME == "TORCH":
                return visionRadius + 1
        return visionRadius

    def getInventoryString(self):
        inventoryString = ""
        for x in range(len(self.inventory)):
            inventoryString += " " + str(x) + ":" + self.inventory[x].getNameString()
        if inventoryString == "":
            inventoryString += " nothing"
        return inventoryString

    def addToInventory(self, item):
        self.inventory.append(item)

    def getItem(self, itemIndex):
        item = None
        if 0 <= itemIndex < len(self.inventory):
            item = self.inventory.pop(itemIndex)
        return item

    def hasItem(self, itemName):
        itemIndex = None
        for index in range(len(self.inventory)):
            if self.inventory[index].NAME == itemName:
                itemIndex = index
        return itemIndex
