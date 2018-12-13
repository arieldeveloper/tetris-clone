#########################################
# Programmer: Mrs.G
# Date: 21/11/2015
# File Name: tetris_classes5.py
# Description: These classes are templates for writing a Tetris game.
#########################################
import pygame

BLACK     = (0, 0, 0)
RED       = (255, 0, 0)
GREEN     = (0, 255, 0)
BLUE      = (0, 0, 255)
ORANGE    = (255, 127, 0)
CYAN      = (0, 183, 235)
MAGENTA   = (255, 0, 255)
YELLOW    = (255, 255, 0)
WHITE     = (255, 255, 255)

COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
figures   = [None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None]

#Shape Ima
class Block(object):                    
    """ A square - basic building block used in all the other classes
        data:               behaviour:
            col - column        draw
            row - row
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
        pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1)

    def shadowDraw(self, surface, gridsize=20):
        x = self.col * gridsize
        y = self.row * gridsize
        pygame.draw.rect(surface, WHITE, (x, y, gridsize, gridsize), 1)
    
    def move_left(self):
        self.col = self.col - 1
        
    def move_right(self):
        self.col = self.col + 1
    
    def move_down(self):
        self.row = self.row + 1
    
    def move_up(self):
        self.row = self.row - 1

class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      

        #Vertical offsets
        self._colOffsets = [0]*blocksNo  #@@
        #horizontal offsets
        self._rowOffsets = [0]*blocksNo  #@@

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] #@@
            blockROW = self.row+self._rowOffsets[i] #@@
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    
    def append(self, other): 
        """ Append all blocks from another cluster to this one.
        """
        for i in other.blocks:
            self.blocks.append(i)

    def clear(self):
        """
        Clears the blocks list, removes all the obstacles
        """
        self.blocks.clear()

class Obstacles(Cluster):
    """ Combination of all the previous shapes that fell down.
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print(block)

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        
        #Fill the number of rows with # of blocks
        for block in self.blocks:                       
            rows.append(block.row)
        
        #Starting from the top row, count down, if as many blocks in row as columns, its full so return a list with the full rows numbers
        for row in range(top, bottom):
            if rows.count(row) == columns:
                fullRows.append(row)
        return fullRows

    def removeFullRows(self, fullRows):
        """
            Remove the rows that are full, move down the rows that are not.
            """
        #for each full row starting from the top down to the bottom, check all obstacle blocks in order that way it doesn't go out of range
        for row in fullRows:
            for i in reversed(range(len(self.blocks))):
                #Remove each block that is on that full row
                if self.blocks[i].row == row:
                    self.blocks.pop(i)
                #Move down each block that isn't on the row that is full
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()

class Shape(Cluster):                     
    """ A bunch of shapes: Z,S,J,L,I,T,O; Each consists of 4 x Block() objects.
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] #@@
        self._rowOffsets = [-1,-1, 0, 0] #@@
        self._rotate() #@@
        
    def __str__(self):                  
        return figures[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #
        elif self.clr == 2:
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
                             
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #
        
        elif self.clr == 4:
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [1, 1, 0, -1], [1, 0, 0,0], [-1, -1, 0,1]]
            _rowOffsets = [[-1,-1, 0, 1], [-1,0, 0, 0], [1,1, 0,-1], [1,0, 0, 0]]
        
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
                
        self._colOffsets = _colOffsets[self._rot] #@@
        self._rowOffsets = _rowOffsets[self._rot] #@@
        self._update() #@@

    def move_left(self):                
        self.col = self.col - 1                   
        self._update() #@@
        
    def move_right(self):               
        self.col = self.col + 1                   
        self._update() #@@
        
    def move_down(self):                
        self.row = self.row + 1                   
        self._update() #@@
        
    def move_up(self):                  
        self.row = self.row - 1                   
        self._update() #@@

    def rotateClkwise(self):
        self._rot = (self._rot + 1) % 4
        self._rotate()

    def rotateCntclkwise(self):
        self._rot = (self._rot - 1) % 4
        self._rotate()

class Shadow(Shape):
    def moveToBottom(self, floor, obstacles):
        while self.collides(floor) == False and self.collides(obstacles) == False:
            self.move_down()
        self.move_up()
        self._update()

    def update(self, other):
        self._rot = other._rot
        self.col = other.col
        self.clr = other.clr
        self._rotate()

    def draw(self, surface, gridsize = 20):
        for block in self.blocks:
            block.shadowDraw(surface, gridsize)

class Floor(Cluster):
    """ Horizontal line of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i  #@@
        self._update() #@@

class Wall(Cluster):
    """ Vertical line of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i #@@
        self._update() #@@
