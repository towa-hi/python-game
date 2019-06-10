To access the cheat menu, input 'i am a weenie'

Solutions:
1. The star tree door can only be opened if the room's inventory contains the right items in the right sequence. There are two possible answers for this:
[97,41,7,53,107,101,103] and [97,41,7,53,103,101,107] will both give the correct answer.

2. The cipher door requires a cipher in the form of adding the sum of the values obtained using this table with the word Μῑνώταυρος: https://en.wikipedia.org/wiki/Isopsephy. The answer is [1][9][7][1]

3. The binary chest can be opened by again using the https://en.wikipedia.org/wiki/Numerology#Pythagorean_system to obtain the name of the creator of the Labyrinth, Daedalus and converting to binary to get 101100, which is the sequence of switches activated.

4. The permutation door can be opened either with guessing or by knowing who the son of Daedalus is. ! represents a correct letter but incorrect placement. This is basically a set guessing problem identical to the game Mastermind.

Requirements:

1. Number conversion from decimal to binary is the key element of the binary chest

2. Ciphers are used twice, once to hash the name Daedalus into a integer for the binary chest, and again to hash the word Μῑνώταυρος to unlock the cipher door.

3. Sets are used in the function makeWalkableRoomsSet() and in the dijkstra() function. Sets are used here because order doesn't matter but we need a way to guarentee that no duplicate rooms can exist. Examples of unions, intersections and set difference can be found in the Misc.py file.

4. All the puzzles require some kind of permutation or ordering of the correct answers. The mastermind game has the player make a narrowing set of permutations to come to the correct answer.

5. The cursed SHACKLES item will negate your movement randomly with the odds of 0.33 every time you attempt to move.

6. Dijkstra's algorithm is used for both the pathfinding for the enemy and as a simulation for line of slight. Dijkstra's algorithm is greedy. A depth first search is used to interpret the graph created by the dijkstra() function

7. Recursion is used to do a depth first search in the function dfs() within the shortestPath() function. Recursion is also used to add and delete nodes in the tree.

8. The tree star door requires the player to insert elements by their preorder traversal. A tree is also included in the Misc.py file with insertion and deletion.

9. All the Room objects inside of my MAP contain references to adjacent Room objects. This is a graph. I do depth first graph traversal using the dfs() function in my pathfinding algorithm.

10. The only stat attached to the player entity itself is a stat for line of sight, which increases and decreases depending on whether or not you are holding a torch.

11. There are four puzzles.

12. There are at least a hundred rooms all in various dynamic states.
