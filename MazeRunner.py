import API # This is just used to interface with the simulator software
import sys
from collections import deque # used for the queue in floodFill()
# TODO: Write known path plus visited cells to storage incase we need to restart the device

'''The important stats about where the mouse is and where it is facing'''
currentOrientation = "N" # orientation of the bot
currentX = 0
currentY = 0

'''THe file names used for storing maze information to storage. I use global variables to avoid two different methods accidentally using different file names.'''
cellDistancesFile = "SavedCellDistances.txt"
wallInformationFile = "WallInformation.txt"
visitedCellsFile = "VisitedCells.txt"

''' Each entry in the matrix corresponds to that cell in the maze.
    Each value is that cell's distance from the center (notice the 0 distances in the middle
'''
cellDistances =[[14,13,12,11,10,9 ,8 ,7 ,7 ,8 ,9 ,10,11,12,13,14],
                [13,12,11,10,9 ,8 ,7 ,6 ,6 ,7 ,8 ,9 ,10,11,12,13],
                [12,11,10,9 ,8 ,7 ,6 ,5 ,5 ,6 ,7 ,8 ,9 ,10,11,12],
                [11,10,9 ,8 ,7 ,6 ,5 ,4 ,4 ,5 ,6 ,7 ,8 ,9 ,10,11],
                [10,9 ,8 ,7 ,6 ,5 ,4 ,3 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10],
                [9 ,8 ,7 ,6 ,5 ,4 ,3 ,2 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ],
                [8 ,7 ,6 ,5 ,4 ,3 ,2 ,1 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ],
                [7 ,6 ,5 ,4 ,3 ,2 ,1 ,0 ,0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ],
                [7 ,6 ,5 ,4 ,3 ,2 ,1 ,0 ,0 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ],
                [8 ,7 ,6 ,5 ,4 ,3 ,2 ,1 ,1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ],
                [9 ,8 ,7 ,6 ,5 ,4 ,3 ,2 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ],
                [10,9 ,8 ,7 ,6 ,5 ,4 ,3 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10],
                [11,10,9 ,8 ,7 ,6 ,5 ,4 ,4 ,5 ,6 ,7 ,8 ,9 ,10,11],
                [12,11,10,9 ,8 ,7 ,6 ,5 ,5 ,6 ,7 ,8 ,9 ,10,11,12],
                [13,12,11,10,9 ,8 ,7 ,6 ,6 ,7 ,8 ,9 ,10,11,12,13],
                [14,13,12,11,10,9 ,8 ,7 ,7 ,8 ,9 ,10,11,12,13,14]]

''' The following lists tell you which wall configurations would exclude you from going to your neighbor to your specified direction.
    For example, wallsThatExcludeNorth tells you which wall configuration the cell above you would have the would prevent you from moving in to it.'''
wallsThatExcludeNorth = [2,5,8,10,12,13,14]
wallsThatExcludeSouth = [4,6,7,10,11,12,14]
wallsThatExcludeEast = [1,5,6,9,11,13,14]
wallsThatExcludeWest = [3,7,8,9,11,12,13]
'''Each position corresponds to that cell's position in the maze. Each value encodes the currently known wall data for each cell.'''
wallInformation=[   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
"""
0  - no walls
1  - left
2  - bottom
3  - right
4  - top
5  - left, bottom
6  - left, top
7  - top, right
8  - bottom, right
9  - left, right
10 - top, bottom
11 - left, top, right
12 - top, right, bottom
13 - left, bottom, right
14 - top, left, bottom
"""

'''Each position corresponds to that cell's position in the maze. Each value signifies if the bot has been in this cell before.'''
visitedCells=  [[False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False],
                [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]]

'''To interface with the simulator, I use the API library. This will need to be swapped out when we build the physical mouse.'''
def wallFront():
    return API.wallFront()

def wallLeft():
    return API.wallLeft()

def wallRight():
    return API.wallRight()

# If a wall has been discovered on the left side of a cell, update it accordingly
def updateWallOnLeftOfCell(currentX, currentY):
    ''' This function and its sister functions must first look at what the currently saved wall information is for a cell,
        then update it accordingly with the newly discovered wall information.
        
        You will notice that not every possible wall value is checked in the switch-statement. This is because it some wall values would already include the newly discovered
        wall, or a cell would have walls on all sides, which is impossible (otherwise how did the mouse get in there???)
    '''

    global wallInformation
    currentCellWallInfo = wallInformation[currentX][currentY]

    match currentCellWallInfo:
            case 0:
                wallInformation[currentX][currentY] = 1
            case 2:
                wallInformation[currentX][currentY] = 5
            case 3:
                wallInformation[currentX][currentY] = 9
            case 4:
                wallInformation[currentX][currentY] = 6
            case 7:
                wallInformation[currentX][currentY] = 11
            case 8:
                wallInformation[currentX][currentY] = 13
            case 10:
                wallInformation[currentX][currentY] = 14

def updateWallOnRightOfCell(currentX, currentY):
    '''See documentation for updateWallOnLeftOfCell()'''
    global wallInformation
    currentCellWallInfo = wallInformation[currentX][currentY]

    match currentCellWallInfo:
        case 0:
            wallInformation[currentX][currentY] = 3
        case 1:
            wallInformation[currentX][currentY] = 9
        case 2:
            wallInformation[currentX][currentY] = 8
        case 4:
            wallInformation[currentX][currentY] = 7
        case 5:
            wallInformation[currentX][currentY] = 13
        case 6:
            wallInformation[currentX][currentY] = 11
        case 10:
            wallInformation[currentX][currentY] = 12

def updateWallOnTopOfCell(currentX, currentY):
    '''See documentation for updateWallOnLeftOfCell()'''
    global wallInformation
    currentCellWallInfo = wallInformation[currentX][currentY]

    match currentCellWallInfo:
        case 0:
            wallInformation[currentX][currentY] = 4
        case 1:
            wallInformation[currentX][currentY] = 6
        case 2:
            wallInformation[currentX][currentY] = 10
        case 3:
            wallInformation[currentX][currentY] = 7
        case 5:
            wallInformation[currentX][currentY] = 14
        case 8:
            wallInformation[currentX][currentY] = 12
        case 9:
            wallInformation[currentX][currentY] = 11

def updateWallOnBottomOfCell(currentX, currentY):
    '''See documentation for updateWallOnLeftOfCell()'''
    global wallInformation
    currentCellWallInfo = wallInformation[currentX][currentY]

    match currentCellWallInfo:
        case 0:
            wallInformation[currentX][currentY] = 2
        case 1:
            wallInformation[currentX][currentY] = 5
        case 3:
            wallInformation[currentX][currentY] = 8
        case 4:
            wallInformation[currentX][currentY] = 10
        case 6:
            wallInformation[currentX][currentY] = 14
        case 7:
            wallInformation[currentX][currentY] = 12
        case 9:
            wallInformation[currentX][currentY] = 13

def discoverWalls(currentX, currentY):
    ''' Checks for a wall to left, front, and right, then updates wallInformation list to reflect this information.
    
        The following three if statements follow this format:
        FIRST check if sensors pick up on a wall
            THEN find the bot's orientation
                FINALLY update the wall information corresponding to which sensor picked up a wall AND bot current orientation
                Two walls must be updated because walls are shared by two cells 
        
        updateWallOn____OfCell() are helper functions that handle the logic of updating wall info.
        This is because what value to update the cell info to depends on what cell info is already stored.
    '''

    if wallLeft():
        if currentOrientation == "N":
            updateWallOnLeftOfCell(currentX, currentY)
            if currentX > 0: # If we are against the leftmost wall,then there is no corresponding cell in [] to be updated
                updateWallOnRightOfCell(currentX-1, currentY)
        elif currentOrientation == "W":
            updateWallOnBottomOfCell(currentX, currentY)
            if currentY > 0: # If we are at bottomost wall, then there is no corresponding cell in [] to be updated 
                updateWallOnTopOfCell(currentX, currentY-1)
        elif currentOrientation == "S":
            updateWallOnRightOfCell(currentX, currentY)
            if currentX < 15:
                updateWallOnLeftOfCell(currentX+1, currentY)
        elif currentOrientation == "E":
            updateWallOnTopOfCell(currentX, currentY)
            if currentY < 15:
                updateWallOnBottomOfCell(currentX, currentY+1)
    
    if wallRight():
        if currentOrientation == "N":
            updateWallOnRightOfCell(currentX, currentY)
            if currentX < 15: # If we are on rightmost wall, then there is no corresponding cell in [] to be updated 
                updateWallOnLeftOfCell(currentX+1, currentY)
        elif currentOrientation == "W":
            updateWallOnTopOfCell(currentX, currentY)
            if currentY < 15: # If we are at topmost wall, then there is no corresponding cell in [] to be updated
                updateWallOnBottomOfCell(currentX, currentY+1)
        elif currentOrientation == "S":
            updateWallOnLeftOfCell(currentX, currentY)
            if currentX > 0:
                updateWallOnRightOfCell(currentX-1, currentY)
        elif currentOrientation == "E":
            updateWallOnBottomOfCell(currentX, currentY)
            if currentY > 0:
                updateWallOnTopOfCell(currentX, currentY-1)

    if wallFront():
        if currentOrientation == "N":
            updateWallOnTopOfCell(currentX, currentY)
            if currentY < 15:
                updateWallOnBottomOfCell(currentX, currentY+1)
        elif currentOrientation == "W":
            updateWallOnLeftOfCell(currentX, currentY)
            if currentX > 0: # If we are against the leftmost wall,then there is no corresponding cell in [] to be updated
                updateWallOnRightOfCell(currentX-1, currentY)
        elif currentOrientation == "S":
            updateWallOnBottomOfCell(currentX, currentY)
            if currentY > 0:
                updateWallOnTopOfCell(currentX, currentY-1)
        elif currentOrientation == "E":
            updateWallOnRightOfCell(currentX,currentY)
            if currentX < 15:
                updateWallOnLeftOfCell(currentX+1, currentY)

def turnMouse(direction):
    ''' Turns mouse either 90 degrees to the left or right ONCE.
        Currently uses the API library to interface with the simulator... this will be changed when we build the physical bot.'''
    if direction == "R":
        API.turnRight()
    elif direction == "L":
        API.turnLeft()
    else:
        print("ERROR: invalid direction")
        pass

def driveForward():
    '''Moves mouse forward by one cell.'''
    API.moveForward()

def moveMouse(directionToMove):
    ''' Handles the logic for how to get from one cell to its cardinal neighbor.
        Will update the orientation and position information about the mouse accordingly.

        The number of 90 degree turns that must be made before the bot can proceed in the directionToMove depends on the bot's current direction.
        Therefore the following if statement has a block for each of the possible directions for the bot to be facing.
        Then inside of each if statement is a switch-statement that decides how many 90 degree turns are necessary before moving forward.
    '''
    global currentOrientation
    global currentX
    global currentY

    if currentOrientation == "N":
        match directionToMove:
            case "N":
                driveForward()
                currentY += 1
            case "S":
                turnMouse("R")
                turnMouse("R")
                driveForward()
                currentY -= 1
            case "E":
                turnMouse("R")
                driveForward()
                currentX += 1
            case "W":
                turnMouse("L")
                driveForward()
                currentX -= 1
    elif currentOrientation == "S":
        match directionToMove:
            case "N":
                turnMouse("R")
                turnMouse("R")
                driveForward()
                currentY += 1
            case "S":
                driveForward()
                currentY -= 1
            case "E":
                turnMouse("L")
                driveForward()
                currentX += 1
            case "W":
                turnMouse("R")
                driveForward()
                currentX -= 1
    elif currentOrientation == "E":
        match directionToMove:
            case "N":
                turnMouse("L")
                driveForward()
                currentY += 1
            case "S":
                turnMouse("R")
                driveForward()
                currentY -= 1
            case "E":
                driveForward()
                currentX += 1
            case "W":
                turnMouse("R")
                turnMouse("R")
                driveForward()
                currentX -= 1
    elif currentOrientation == "W":
        match directionToMove:
            case "N":
                turnMouse("R")
                driveForward()
                currentY += 1
            case "S":
                turnMouse("L")
                driveForward()
                currentY -= 1
            case "E":
                turnMouse("R")
                turnMouse("R")
                driveForward()
                currentX += 1
            case "W":
                driveForward()
                currentX -= 1

    currentOrientation = directionToMove

def cellLessThanOther(currentCell, neighborCell):
    ''' Tells you if neighborCell has a lower distance value than currentCell.
        Helps keep the if statements in main() that decide which neighbor of the current cell has the lowest distance value from getting too ugly.
    '''
    if cellDistances[neighborCell[0]][neighborCell[1]] < cellDistances[currentCell[0]][currentCell[1]]:
        return True
    else:
        # neighborCell has a larger distance value than currentCell
        return False

def resetCellDistances():
    ''' A helper function for floodFill. Every time floodFill is run, it must first reset the target cell distances to 0 and all others to "no distance value".
        -1 represents 'no distance value'. 
    '''
    global cellDistances

    cellDistances= [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,0 ,0 ,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,0 ,0 ,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]

def getAccessibleNeighbors(cellCoords):
    '''Finds and returns all cells that not blocked by a wall AND are adjacent to the cell described by cellCoords.'''
    adjacentNeighbors = []
    tmpX = cellCoords[0]
    tmpY = cellCoords[1]

    # Check if this cell has a north neighbor
    if tmpY < 15: # Can't have a north neighbor if you are at the top of the maze
        northNeighborWallInfo = wallInformation[tmpX][tmpY+1]
        if northNeighborWallInfo not in wallsThatExcludeNorth:
            adjacentNeighbors.append((tmpX, tmpY+1))
    
    # Check for south neighbor
    if tmpY > 0: # Can't have south neighbor if you are at bottom of maze
        southNeighborWallInfo = wallInformation[tmpX][tmpY-1]
        if southNeighborWallInfo not in wallsThatExcludeSouth:
            adjacentNeighbors.append((tmpX, tmpY-1))
    
    # Check for west neighbor
    if tmpX > 0: # Can't have west neighbor if you are at left side of maze
        westNeighborWallInfo = wallInformation[tmpX-1][tmpY]
        if westNeighborWallInfo not in wallsThatExcludeWest:
            adjacentNeighbors.append((tmpX-1, tmpY))
    
    # Check for east neighbor
    if tmpX < 15: # Can't have east neighbor if you are at right side of maze
        eastNeighborWallInfo = wallInformation[tmpX+1][tmpY]
        if eastNeighborWallInfo not in wallsThatExcludeEast:
            adjacentNeighbors.append((tmpX+1, tmpY))
    
    return adjacentNeighbors

def floodFill():
    ''' The floodFill algorithm is responsible for calculating the manhattan distances of all cells to the target cells (the cells at the center of the maze).
        It uses the wall information that is currently known, assuming there are no walls in cells that haven't been visited.
    '''
    cellsQueue = deque()
    global cellDistances
    resetCellDistances()

    # Start by adding goal cells to queue
    # Recall that goal cells have distance of 0... because they are the goals
    cellsQueue.append((7,7))
    cellsQueue.append((7,8))
    cellsQueue.append((8,7))
    cellsQueue.append((8,8))

    ''' From Micromouse Lecture 6 Slide 17 detailing flood fill:

        While queue is not empty:
            Take front cell in queue out of line for consideration
            Set all blank and accessible neighbors to front cell's value + 1
            Add cells we just processed to the queue
            Else, continue!
    '''
    while cellsQueue:
        tmpCell = cellsQueue.popleft()
        tmpCellDistance = cellDistances[tmpCell[0]][tmpCell[1]]
        
        tmpCellNeighbors = getAccessibleNeighbors(tmpCell)
        for neighbor in tmpCellNeighbors:
            # -1 means that cell is 'blank', aka it has no value yet (because the values were reset)
            if cellDistances[neighbor[0]][neighbor[1]] == -1:              
                cellDistances[neighbor[0]][neighbor[1]] = tmpCellDistance + 1
                cellsQueue.append(neighbor)

def writeMazeInfoToStorage():
    ''' Saves the cell distances, wall information, and visited cells information to storage
        so that it can be loaded. Will be run by main() when the end is reached, so that any subsequent runs 
        should be able to go straight to the destination cells.
    '''

    # First, save the cell distances information to storage
    # with statement will automatically handle closing files, even if exceptions occur
    with open(cellDistancesFile, 'w') as file:
        for row in cellDistances:
            # Convert each value to string and join with commas
            line = ','.join(map(str, row))
            file.write(line + '\n')
    
    # Second, save the wall information to storage
    with open(wallInformationFile, 'w') as file:
        for row in wallInformation:
            # Convert each value to string and join with commas
            line = ','.join(map(str, row))
            file.write(line + '\n')
    
    ''' Third, save visited cells information to storage.
        Note that because visitedCells uses booleans, if we were to save 'True' or 'False' to a txt file, 
        there would be no good way to convert these strings back to booleans. So, save them as either 1 or 0 instead in the txt file,
        then when they are loaded back in loadMazeInfoFromStorage, each 1 or 0 will be converted back to their respective boolean.
    '''
    with open(visitedCellsFile, 'w') as file:
        for row in visitedCells:
            # Convert booleans to '1' and '0' for clearer reading
            # and join with commas
            line = ','.join('1' if cell else '0' for cell in row)
            file.write(line + '\n')

def loadMazeInfoFromStorage():
    ''' Loads information regarding cell distances, wall information, and visited cells that had 
        been saved when the mouse had reached the destination cells. 
        Loading these values from storage should be all that is needed for the mouse to go straight to the destination.
    '''

    # Reset the lists to be updated:
    global cellDistances
    global wallInformation
    global visitedCells
    cellDistances = []
    wallInformation = []
    visitedCells = []

    # First, load the cell distances information from storage:
    try:
        with open(cellDistancesFile, 'r') as file:
            for line in file:
                # Split the line by commas and convert each value to int
                row = [int(val) for val in line.strip().split(',')]
                cellDistances.append(row)
    except FileNotFoundError:
        print(f"Error: {cellDistancesFile} not found")
    
    # Second, load the wall information from storage:
    try:
        with open(wallInformationFile, 'r') as file:
            for line in file:
                # Split the line by commas and convert each value to int
                row = [int(val) for val in line.strip().split(',')]
                wallInformation.append(row)
    except FileNotFoundError:
        print(f"Error: {wallInformationFile} not found")
    
    # Third, load the visited cells information from storage.
    # Note that because Python can't convert strings to booleans, when this list was stored as a txt file
    # it had to convert each boolean to either 1 or 0... so, convert these 1s and 0s back to booleans in this step:
    try:
        with open(visitedCellsFile, 'r') as file:
            for line in file:
                # Convert '1' to True and '0' to False
                row = [val == '1' for val in line.strip().split(',')]
                visitedCells.append(row)
    except FileNotFoundError:
        print(f"Error: {visitedCellsFile} not found")

def main():
    ''' Coordinates:
        - checking for new walls
        - deciding which cell to move to next
        - performing flood fill if there is no where to move to next

        The way the floodFill algorithm works is like this:
            Get accessible neighbors of the current cell
            Move to the neighbor with the lowest distance value
            IF there are no accessible neighbors with distance values LOWER THAN the current cell's distance value THEN
                perform floodFill() to recalculate all distance values
    '''
    
    loadInformation = False
    if loadInformation:
            loadMazeInfoFromStorage()


    while(True): # Runs until the end is reached
        global visitedCells

        # If we have reached the center of the maze, stop running
        # The cell distances of the target cells will always be 0
        if cellDistances[currentX][currentY] == 0:
            print("The destination has been reached!")
            print("Writing the maze information to storage...")
            
            if not loadInformation: # If we've loaded the information from storage, why would we need to write it again?
                writeMazeInfoToStorage()
            break

        # No need to check for walls in a cell we've already been to
        if not visitedCells[currentX][currentY]:
            discoverWalls(currentX, currentY)
            visitedCells[currentX][currentY] = True
        
        # An 'open neighbor' is a neighboring cell without a wall blocking your path to it
        openNeighbors = []

        # If the bot has a (direction) neighbor, and if that isn't blocked by a wall, then add that neighbor to the list of possible neighbors to travel to
        if currentX > 0: # if there is a cell west of the bot
            westNeighborWall = wallInformation[currentX-1][currentY]
            # a neighbor is only eligible to be moved into if its value is less than the current cell's value, hence the 'and' statement
            if (westNeighborWall not in wallsThatExcludeWest) and cellLessThanOther((currentX, currentY), (currentX-1, currentY) ):
                openNeighbors.append( ("W", cellDistances[currentX-1][currentY]) )
        
        if currentX < 15: # if there is a cell east of the bot
            eastNeighborWall = wallInformation[currentX+1][currentY]
            if (eastNeighborWall not in wallsThatExcludeEast) and cellLessThanOther((currentX, currentY), (currentX+1, currentY) ):
                openNeighbors.append( ("E", cellDistances[currentX+1][currentY]) )

        if currentY > 0: # if there is a cell south of the bot
            southNeighborWall = wallInformation[currentX][currentY-1]
            if (southNeighborWall not in wallsThatExcludeSouth) and cellLessThanOther((currentX, currentY), (currentX, currentY-1) ):
                openNeighbors.append( ("S", cellDistances[currentX][currentY-1]) )
        
        if currentY < 15: # if there is a cell north of the bot
            northNeighborWall = wallInformation[currentX][currentY+1]
            if (northNeighborWall not in wallsThatExcludeNorth) and cellLessThanOther((currentX, currentY), (currentX, currentY+1) ):
                openNeighbors.append( ("N", cellDistances[currentX][currentY+1]) )

        # Go to the neighbor with the lowest "distance from center" value
        if openNeighbors:
            shortestDistanceNeighbor = min(openNeighbors, key=lambda x: x[1])
            moveMouse(shortestDistanceNeighbor[0])
        else:
            # If this is executing, it means that there are no accessible neighbors who have distance values lower than the current cell's distance value
            # This means it is time to reupdate the distance values for all cells... hence, run floodFill()
            floodFill()

main()