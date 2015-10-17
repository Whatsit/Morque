# directions
NORTH = (0, 1)
EAST = (1, 0)
SOUTH = (0, -1)
WEST = (-1, 0)

class Map (object):
    def __init__(self):
        ''' 
            Dictionary contains a tuple with x, y coordinates as a key, e.g. (3,2).
            Room object is accessed with this key.
        '''
        self.rooms = {}
    
class Room (object):
    def __init__(self, map, xy):
        self.map = map
        self.players = []
        self.items = []
        self.xy = xy
        
class PuzzleRoom (Room):
    def __init__(self, map, xy):
        super().__init__(map, xy)
        self.puzzle = ''
        self.solution = ''
        
    def verifySolution(self, attempt):
        if attempt == self.solution:
            return True
        return False

class Item:
    # Abstract class, cannot be initiated.
    def __init__(self):
        raise NotImplementedError
        
class Key (Item):
    def __init__(self):
        self.name = 'key'
        
    def __init__(self, name):
        self.name = name
     
class Player (object):
    def __init__(self, room):
        self.room = room
        self.room.players.append(self)
        self.name = ''
        self.inventory = []
        
    def move(self, direction, priority):
        try:
            nextRoom = self.room.map.rooms[(self.room.xy[0] + direction[0], self.room.xy[1] + direction[1])]
        except:
            print('You hit a wall.')
            return
        if isinstance(nextRoom, PuzzleRoom) and priority is 0:
            print('Room is locked. Use a key.')
        else:
            self.room.players.remove(self)
            self.room = nextRoom
            self.room.players.append(self)
        
    def useItem(self, itemName):
        ''' 
            Takes the name of the item as a string and
            accesses the object from the player's inventory.
        '''
        itemFound = False
        item = None
        for i in self.inventory:
            if i.name.lower() == itemName.lower():
                itemFound = True
                item = i
                break
        if itemFound is False:
            print('No such item in inventory.')
            return
            
        if isinstance(item, Key):
            self.__unlock(item)
            
    def __unlock(self, key):
        for direction in [NORTH, EAST, SOUTH, WEST]:
            try:
                newRoom = self.room.map.rooms[(self.room.xy[0] + direction[0], self.room.xy[1] + direction[1])]
            except:
                continue
            
            if isinstance(newRoom, PuzzleRoom):
                # self.inventory.remove(key)
                print('Puzzle room unlocked. Moving there now.')
                self.move(direction, 1)
                return
                
        print('No door to use key on.')
        
    def attemptPuzzle(self):
        # Returns True if player solved puzzle, False if not.
        if isinstance(self.room, PuzzleRoom):
            triesLeft = 3
            while triesLeft > 0:
                print('You have ' + str(triesLeft) + ' tries left.')
                print('The puzzle description reads as follows:')
                print()
                print(self.room.puzzle)
                print()
                if self.room.verifySolution(input()):
                    print('That is correct!\n')
                    return True
                else:
                    print('\nSorry, that is incorrect.')
                    triesLeft -= 1
            
            print('Your ded')
            return False
    
    def getItem(self, itemName):
        itemFound = False
        item = None
        for i in self.room.items:
            if i.name.lower() == itemName.lower():
                itemFound = True
                item = i
                print('You have picked up: ' + itemName)
                break
        if itemFound is False:
            print('No such item in room.')
            return
            
        self.room.items.remove(item)
        self.inventory.append(item)
        
    def searchRoom(self):
        # Returns a list of the names of items in the current room.
        itemList = []
        for item in self.room.items:
            itemList.append(item.name)
        return itemList
