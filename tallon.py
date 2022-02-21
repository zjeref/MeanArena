# tallon.py
#
# The code that defines the behaviour of Tallon. This is the place
# (the only place) where you should write code, using access methods
# from world.py, and using makeMove() to generate the next move.
#
# Written by: Simon Parsons
# Last Modified: 12/01/22


from calendar import c
import world
import random
import config
from utils import Directions
from utils import Pose

class Tallon():

    def __init__(self, arena):

        # Make a copy of the world an attribute, so that Tallon can
        # query the state of the world
        self.gameWorld = arena

        # What moves are possible.
        self.moves = [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]
        
    def makeMove(self):
        # This is the function you need to define
        myPosition = self.gameWorld.getTallonLocation()
        nextDirection = self.shortestPath(myPosition)

        print(nextDirection)

        if not nextDirection:
            dice = random.randint(0,3)
            return self.moves[dice]

        if nextDirection[0] > myPosition.x:
            return Directions.EAST
        if nextDirection[0] < myPosition.x:
            return Directions.WEST
        # If not at the same y coordinate, reduce the difference
        if nextDirection[1] < myPosition.y:
            return Directions.NORTH
        if nextDirection[1] > myPosition.y:
            return Directions.SOUTH



        # if there are still bonuses, move towards the next one.


        # if there are no more bonuses, Tallon doesn't move

    def shortestPath(self, myPosition):
        row = config.worldLength
        column = config.worldBreadth

        # This is used to get all positions of the characters in game
        allBonuses = self.gameWorld.getBonusLocation()
        allMeanies = self.gameWorld.getMeanieLocation()
        allPits = self.gameWorld.getPitsLocation()

        # using Breadth First Search to get shortest path of bonus which avoid all the meanies and pits
        start = (myPosition.x, myPosition.y)
        frontier=[start]
        explored=[start]
        directions = [[0,1], [0,-1], [1,0], [-1,0]]
        bfsPath = {}

        while len(frontier)>0:
            coord = frontier.pop()

            for i in range(len(allBonuses)):
                if coord[0] == allBonuses[i].x and coord[1] == allBonuses[i].y:
                    return frontier[1]

            for dir in directions:
                newRow, newColumn = coord[0]+dir[0], coord[1]+dir[1]
                
                childCell = (newRow, newColumn)

                if(newRow < 0 or newRow >= row or newColumn < 0 or newColumn >= column):
                    continue

                if childCell in explored:
                    continue
                p = Pose()
                p.x = newRow
                p.y = newColumn
                if self.gameWorld.isSmelly(p) or self.gameWorld.isWindy(p):
                    continue

                for i in range(len(allMeanies)):
                    if newRow == allMeanies[i].x and newColumn == allMeanies[i].y:
                        continue

                for i in range(len(allPits)):
                    if newRow == allPits[i].x and newColumn == allPits[i].y:
                        continue

                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = coord



