class Item:
    def __init__ (self, name):
        self.NAME = name
        self.value = None
        self.description = "Generic Object"
        if name == "NINETYSEVEN":
            self.value = 97
            self.description = "A star shaped stone with ϙζ carved onto it."
        if name == "FORTYONE":
            self.value = 41
            self.description = "A star shaped stone with μα carved onto it."
        if name == "ONEHUNDREDANDSEVEN":
            self.value = 107
            self.description = "A star shaped stone with (ρζ) carved onto it."
        if name == "SEVEN":
            self.value = 7
            self.description = "A star shaped stone with (ζ) carved onto it."
        if name == "FIFTYTHREE":
            self.value = 53
            self.description = "A star shaped stone with (νγ) carved onto it."
        if name == "ONEHUNDREDANDONE":
            self.value = 101
            self.description = "A star shaped stone with (ρα) carved onto it."
        if name == "ONEHUNDREDANDTHREE":
            self.value = 103
            self.description = "A star shaped stone with (ργ) carved onto it."
        if name == "TORCH":
            self.description = "A small torch that lets you see farther."
        if name == "BIG TORCH":
            self.description = "A big torch that lets you see farther."
        if name == "POCKET LINT":
            self.description = "It's lint."
        if name == "SKULL":
            self.description = "A dessicated child sized skull."
        if name == "OFFERINGS":
            self.description = "Rotten meat from an unknown source. Not edible."
        if name == "SHACKLES":
            self.description = "These shackles appear cursed. You can't remove them."
    def getNameString(self):
        nameString = "["
        nameString += self.NAME
        nameString += "]"
        return nameString
