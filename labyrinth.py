import pygame
import math
from queue import PriorityQueue

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (237, 233, 5)
PURPLE = (170, 50, 240)

# Information for the rectangles
WIDTH = 22
HEIGHT = 22
MARGIN = 3

# ---
# Initialize your classes etc.here
# --- 

class Rectangle:
     """ Defines a rectangle on the window """
     def __init__(self,row,col,width) -> None:
          self.row = row
          self.column = col
          self.x = row
          self.y = col
          self.width  = width
          self.color = WHITE  
          self.f = 0          # f value (g+h)
          self.g = 0          # g value
          self.parent = 0     # The parent of the rectangle
          self.neighbors = []

     def drawRect(self,screen):
          """Draw the rectangle on the window"""
          pygame.draw.rect(screen,self.color,[(MARGIN + WIDTH) * self.y + MARGIN,
                         (MARGIN + HEIGHT) * self.x + MARGIN,WIDTH,HEIGHT])
          
     def initNeighbors(self,grid):
          """ Initialize the neighbors of the rectangels.
              Don't take a barrier as neighbor.
              total rows - 1 = total columns - 1 = 20 - 1 = 19
          """
          if self.row < 19 and grid[self.row + 1 ][self.column].color != BLACK:      # Bottom neighbor
               self.neighbors.append(grid[self.row +1 ][self.column])
          if self.row > 0 and grid[self.row - 1 ][self.column].color != BLACK:       # Top neighbor
               self.neighbors.append(grid[self.row - 1 ][self.column])
          if self.column < 19 and grid[self.row][self.column + 1].color != BLACK:    # Right neighbor
               self.neighbors.append(grid[self.row][self.column+1])
          if self.column > 0 and grid[self.row][self.column-1].color != BLACK:       # Left neighbor
               self.neighbors.append(grid[self.row][self.column-1])


# Store if the start and end rectangle is defined #
isStartEnabled = False       
isEndEnabled = False  

def reset(rectangle:Rectangle):
     """Reset the rectangle to initial state"""
     global isStartEnabled, isEndEnabled
     if rectangle.color == BLUE:       # If rectangle is the starting point -> Remove the starting point
          isStartEnabled = False
     elif rectangle.color == GREEN:      # If rectangle is the goal -> Remove the goal
          isEndEnabled = False
     
     rectangle.color = WHITE       # Set color to white (initial)
     
          
### Heuristic functions ###
def euclideanDistance(point, other):
      return math.sqrt((point.x-other.x)**2 + (point.y-other.y)**2)

def manhattanDistance(point,other):      
      return abs(point.y-other.y) + abs(point.x-other.x)



def aStar(start:Rectangle,end:Rectangle) -> list:
    """ The A star algotihm"""
    count = 0
    
    open = PriorityQueue()   # Frontier as Priority Queue
    closed = []              # Visited rectangles
    open.put((count,start.g,start))          # enqueue the start point to the queue
    start.color = RED

    while not open.empty():
         rectangle = open.get()[2]         # Dequeue point from Queue (frontier)
         
         if rectangle == end:           # Check if the goal is reached
              closed.append(rectangle)
              rectangle.color = YELLOW
              break
         
         if rectangle in closed:        # Skip the point if it has already been visited
              continue
         
        
         for neighbor in rectangle.neighbors:
               if neighbor not in closed and neighbor not in [tup[2] for tup in open.queue]:
                   neighbor.g = float("inf")
                   open.put((count,neighbor.g,neighbor))

                   
               if rectangle.g + 1 < neighbor.g:        # +1, because the neigbors are "1 step" away
                    tmp = neighbor.g
                    neighbor.g = rectangle.g + 1
                    neighbor.f = neighbor.g + manhattanDistance(neighbor,end)
                    neighbor.parent = rectangle

                    # Update rectangle if it is in frontier
                    if neighbor in [tup[2] for tup in open.queue]:     
                         open.queue.remove((count,tmp,neighbor))
                         open.put((count,neighbor.f,neighbor))
                         neighbor.color = RED
          
               closed.append(rectangle)
               rectangle.color = YELLOW
               count += 1

    path = []       # Stores the final path
    point = closed[-1]      # Begin from goal point -> BACKTRACKING
    while point != 0:       # Backtrack until start point is reached
          point.color = PURPLE
          path.append(point)
          point = point.parent

    return path
         

grid = []
# Start and end point
start = None
end = None     

pygame.init()

size = (500, 500)        # Width and height of the window
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

done = False

clock = pygame.time.Clock()

for x in range(size[0] // WIDTH+MARGIN):
     grid.append([])
     for y in range(size[0] // WIDTH+MARGIN):
          newRectangle = Rectangle(x,y,WIDTH)
          grid[x].append(newRectangle)
          newRectangle.drawRect(screen)



while not done:
     for event in pygame.event.get():
          if event.type == pygame.QUIT:      # If user clicks the exit button...    
               done = True                   # ...quit the game
          
          
          
          if pygame.mouse.get_pressed()[0]:       # On left click
               y,x = pygame.mouse.get_pos()
               if x < 0 or x > size[0] or y < 0 or y > size[1]:
                    # If the mouse is outside the window, don't react
                    continue

               addressedRectangle = grid[(x-MARGIN) // (MARGIN+HEIGHT)][(y-MARGIN)//(MARGIN+WIDTH)]

               # Change rectangle, if the rectangle isn't a start or end point
               if addressedRectangle.color != BLUE and addressedRectangle.color != GREEN:
                    if not isStartEnabled:
                         # Define starting point
                         addressedRectangle.color = BLUE
                         isStartEnabled = True
                         start = addressedRectangle
                    
                    elif not isEndEnabled:
                         # Define the goal
                         addressedRectangle.color = GREEN
                         isEndEnabled = True
                         end = addressedRectangle
                    else:
                         print((y-MARGIN)//(MARGIN+WIDTH))
                         addressedRectangle.color = BLACK

          if pygame.mouse.get_pressed()[2]:       # On right click
               y,x = pygame.mouse.get_pos()
               if x < 0 or x > size[0] or y < 0 or y > size[1]:
                    # If the mouse is outside the window, don't react
                    continue

               addressedRectangle = grid[(x-MARGIN) // (MARGIN+HEIGHT)][(y-MARGIN)//(MARGIN+WIDTH)]
               if addressedRectangle.color != WHITE: 
                    reset(addressedRectangle)

               print(isStartEnabled)

          
          if event.type == pygame.KEYDOWN:
               # Start A* algorithm, if enter key is pressed
               if event.key == pygame.K_RETURN:
                    for row in grid:
                         for rectangle in row:
                              rectangle.initNeighbors(grid)      # Initialize the neighbors
                    
                    path = aStar(start,end)       # Getting the search path from A*
                    #print(len(path))

          screen.fill(BLACK)


     for row in grid:
               for rectangle in row:
                    rectangle.drawRect(screen)       # Draw the rectangles

     pygame.display.update()

pygame.display.flip()

clock.tick(60)

pygame.quit()