from classes import *

# initialize game map
gameMap = Map()
gameMap.rooms[(0, 0)] = Room(gameMap, (0, 0))
gameMap.rooms[(1, 0)] = Room(gameMap, (1, 0))
gameMap.rooms[(2, 0)] = Room(gameMap, (2, 0))
gameMap.rooms[(1, 1)] = PuzzleRoom(gameMap, (1, 1))

# spawn key in central room
gameMap.rooms[(1, 0)].items.append(Key('key'))

# create puzzle and solution for puzzle room
gameMap.rooms[(1, 1)].puzzle = 'x divided by 42 plus log base 3 of 17 times pi over the square root of 5\n\
is equal to pi times the square root of 5 times log base 3 of 17\nall over 5,\
 plus 23 over 14. What is x?'
gameMap.rooms[(1, 1)].solution = '69'

# initialize and spawn player
player1 = Player(gameMap.rooms[(0, 0)])
player1.name = 'Default'

# print pre-game help messages
print("Type 'move <direction>' to move.")
print("Type 'get <item>' to retrieve an item from a room.")
print("Type 'use <item>' to use an item in your inventory.")
print("Type 'inv' to list the items in your inventory.")
print("Type 'sch' to list the items in the current room.")
print("Type 'quit' to exit game.")

# begin game
while True:

    currentPlayer = player1
    
    # check if player is in puzzle room
    if isinstance(currentPlayer.room, PuzzleRoom):
        if currentPlayer.attemptPuzzle():
            print('You win!')
        quit()

    print('Current location: ' + str(currentPlayer.room.xy[0]) + ', ' + str(currentPlayer.room.xy[1]))
    cmd = input('>>> ')
    cmd = cmd.split()
    
    # quit
    if cmd[0] == 'quit':
        quit()
        
    # move
    elif cmd[0] == 'move':
        direction = (0, 0)
        try:
            if cmd[1] == 'north':
                direction = (0, 1)
            elif cmd[1] == 'east':
                direction = (1, 0)
            elif cmd[1] == 'south':
                direction = (0, -1)
            elif cmd[1] == 'west':
                direction = (-1, 0)
            currentPlayer.move(direction, 0)
        except:
            pass
        
    # search
    elif cmd[0] == 'sch':
        items = currentPlayer.searchRoom()
        if items:
            print('The following items are here: ')
            for item in items:
                print(item)
        else:
            print('There are no items here.')
            
    # get item    
    elif cmd[0] == 'get':
        try:
            currentPlayer.getItem(cmd[1])
        except:
            pass
        
    # list inventory
    elif cmd[0] == 'inv':
        if currentPlayer.inventory:
            print('Your inventory contains: ')
            for item in currentPlayer.inventory:
                print(item.name)
        else:
            print('Your inventory is empty.')
            
    # use item
    elif cmd[0] == 'use':
        try:
            currentPlayer.useItem(cmd[1])
        except:
            pass
