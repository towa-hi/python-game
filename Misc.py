#In this file are things I coded but couldn't find a place to put in my game.
class Node:
    left = None;
    right = None;
    data = None;
    def __init__(self, data):
        self.data = data

class Tree:
    def __init__(self, data):
        root = Node(data)
        self.root = root

    def insert(self, data):
        newNode = Node(data)
        if self.root == None:
            self.root = newNode
        else:
            self.insertRec(self.root, newNode)

    def insertRec(self, root, newNode):
        if newNode.data < root.data:
            if root.left == None:
                root.left = newNode
            else:
                self.insertRec(root.left, newNode)
        elif newNode.data > root.data:
            if root.right == None:
                root.right = newNode
            else:
                self.insertRec(root.right, newNode)
        else:
            print("tree already has value", newNode.data)

    def getPreorder(self):
        outputList = []
        if self.root == None:
            return None
        else:
            self.preorderRec(self.root, outputList)
        return outputList

    def preorderRec(self, root, outputList):
        if root != None:
            outputList.append(root.data)
            self.preorderRec(root.left, outputList)
            self.preorderRec(root.right, outputList)

    def getInorder(self):
        outputList = []
        if self.root == None:
            return None
        else:
            self.inorderRec(self.root, outputList)
        return outputList

    def inorderRec(self, root, outputList):
        if root != None:
            self.inorderRec(root.left, outputList)
            outputList.append(root.data)
            self.inorderRec(root.right, outputList)

    def getHeight(self, root):
        if root == None:
            return 0
        height = max(self.getHeight(root.left), self.getHeight(root.right)) + 1
        return height

    def isBalanced(self):
        return self.isBalancedRec(self.root)

    def isBalancedRec(self, root):
        if root == None:
            return True
        if abs(self.getHeight(root.left) - self.getHeight(root.right)) <= 1:
            if self.isBalancedRec(root.left) == True and self.isBalancedRec(root.right) == True:
                return True
        return False

    def searchBST(self, data):
        if self.root == None:
            return False
        if self.searchBSTRec(self.root, data) != None:
            return True
        else:
            return False

    def searchBSTRec(self, root, data):
        if root == None:
            return root
        if root.data == data:
            return root
        if data < root.data:
            return self.searchBSTRec(root.left, data)
        if data > root.data:
            return self.searchBSTRec(root.right, data)

    def getSmallestNode(self, root):
        currentNode = root
        while (currentNode.left != None):
            currentNode = currentNode.left
        #print("SMALLEST VAL:" + str(currentNode.data))
        return currentNode

    def remove(self, data):
        self.deleteNodeRec(self.root, data)

    def deleteNodeRec(self, root, data):
        if root == None:
            return root
        if data < root.data:
            root.left = self.deleteNodeRec(root.left, data)
        elif data > root.data:
            root.right = self.deleteNodeRec(root.right, data)
        else:
            #print("NODE HAS 1 CHILD")
            if root.left == None:
                temp = root.right
                root = None
                return temp
            elif root.right == None:
                temp = root.left
                root = None
                return temp
            #print("NODE HAS 2 CHILDREN")
            temp = self.getSmallestNode(root.right)
            #print("GETTING SMALLEST NODE")
            root.data = temp.data
            root.right = self.deleteNodeRec(root.right, temp.data)
        return root
print("creating tree with initial value of 5")
tree = Tree(5)
print("inserting 4, 8 , 6 , 9 , 2, 3, 1")
tree.insert(4)
tree.insert(8)
tree.insert(6)
tree.insert(9)
tree.insert(2)
tree.insert(3)
tree.insert(1)
print(tree.getInorder())
print("removing 4")
tree.remove(4)
print("removing 8")
tree.remove(8)
print("removing 5")
tree.remove(5)
print(tree.getInorder())

teachersSet = {"bob", "eric", "small eric"}
classesSet = {"webdev", "android", "discrete"}
print("teachers:")
print(teachersSet)
print("classes:")
print(classesSet)
print("all possible combos of teachers and classes")
import itertools
allPossibleClasses = itertools.product(teachersSet, classesSet)
print(list(allPossibleClasses))
iceCreamSet = {"vanilla", "chocolate", "strawberry"}
print("flavors of ice cream:")
print(iceCreamSet)
shakeSet = {"vanilla", "strawberry", "oreo"}
print("flavors of shakes:")
print(shakeSet)
allFlavors = iceCreamSet | shakeSet
print("all possible flavors:")
print(allFlavors)
sharedFlavors = iceCreamSet & shakeSet
print("shared flavors")
print(sharedFlavors)
iceCreamUnique = iceCreamSet - shakeSet
print("flavors unique to ice cream:")
print(iceCreamUnique)
