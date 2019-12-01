# **Fight**

## SETUP
* Copy the code in template.py to a file that you make in the players folder.
* The filename should be John.py or Mario.py etc.
* Read all of the comments in the file you have just made.
* Your only task is to implement the get_move function.
* You can use helper functions and class fields if you want.

## RULES
* Fight is played turn by turn automatically.
* There's a random sized square board with sizes ranging from 15-35.
* 1 player spawns in the lower right corner, the other spawns in the upper left corner.
* Your goal is to kill the other player by moving and then attacking.


## INFO
* While it is your turn to move and attack, the other player will not move.
* There are several class fields that will be inherited from the player class. You should look at that class to see what is available to you.
* Some of the things that may be helpful:
1) enemy_stats and my_stats are dictionaries containing both players x,y,health,mana and role.
2) me and enemy are the symbols on the board. me is your symbol, enemy is the enemies symbol
3) Your location is given to you every turn as well as the board
* get_move needs to return 3 values as a tuple.
They are: Which way do you want to go, which way you want to attack, and how far should you move.
You can use the global UP, DOWN, LEFT and RIGHT to move and attack. Remember, you will ALWAYS move then attack. The Mage and Monk can also use a spell. The Monk heals themself and the Mage teleports away to a corner. The argument movesize is the maximum  amount of space you can move. You use your SPELL by returning SPELL as the attack direction.
* If you try to move farther than the game told you was possible. You die.
* If you try to move onto a player or off the board, you will stay still, but still attack.
* your move direction and chosen move size will still make you move if you use a spell.
