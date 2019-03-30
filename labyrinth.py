import pygame
import constant
from agent import Agent

class MapSquare:
    def __init__(self, attrib_dict):
        # x and y are the true absolute position in the window
        # map_x and map_y are abstract coordinates to represent the agent position and the target in the 2D map matrix
        # the is_blocked_dict represents a source of information (is_blocked_dict) to know where are the walls in a square
        valid_attributes = ("x", "y", "map_x", "map_y", "is_blocked_dict", "id")
        for key in valid_attributes:
            self.__dict__[key] = attrib_dict[key]
    
    # Function used to draw walls in the corners of the map and walls between the map squares
    def draw_walls(self, surface):
        if(self.is_blocked_dict["left"] == '*'):
            pygame.draw.rect(surface, constant.COLOR_DICT['black'], (self.x-1, self.y, constant.WALL_WIDTH, constant.SQUARE_SIZE),
         constant.SQUARE_EMPTY)
        if(self.is_blocked_dict["right"] == '*'):
            pygame.draw.rect(surface, constant.COLOR_DICT['black'], (self.x+constant.SQUARE_SIZE-constant.WALL_WIDTH+1, self.y,
             constant.WALL_WIDTH, constant.SQUARE_SIZE), constant.SQUARE_EMPTY)
        if(self.is_blocked_dict["top"] == '*'):
            pygame.draw.rect(surface, constant.COLOR_DICT['black'], (self.x, self.y-1,
             constant.SQUARE_SIZE, constant.WALL_WIDTH), constant.SQUARE_EMPTY)
        if(self.is_blocked_dict["bottom"] == '*'):
            pygame.draw.rect(surface, constant.COLOR_DICT['black'], (self.x, self.y+constant.SQUARE_SIZE-constant.SQUARE_EMPTY,
             constant.SQUARE_SIZE, constant.WALL_WIDTH), constant.SQUARE_EMPTY)

    # Function used to draw the target map position
    def draw_target(self, surface):
        pygame.draw.rect(surface, constant.COLOR_DICT['pink'], (self.x+1, self.y+1, constant.SQUARE_SIZE-2, constant.SQUARE_SIZE-2),
         constant.SQUARE_FILLED)

    # Function used to draw the agent map position
    def draw_agent(self, surface):
        pygame.draw.rect(surface, constant.COLOR_DICT['yellow'], (self.x+4, self.y+4, constant.SQUARE_SIZE-8, constant.SQUARE_SIZE-8),
         constant.SQUARE_FILLED)
        pygame.draw.rect(surface, constant.COLOR_DICT['black'], (self.x+4, self.y+4, constant.SQUARE_SIZE-8, constant.SQUARE_SIZE-8),
         constant.SQUARE_EMPTY)

class Labyrinth:
    def __init__(self, map_file, agent):
        # The labyrinth contain a reference to the agent
        self.agent = agent
        self.create_labyrinth(map_file)

    def process_file(self, map_file):
        # Processes map file content and define the map width (number of columns)
        map_file_content = map_file.read().split("\n")
        # Closed opened map file
        map_file.close()
        return map_file_content, [int(i) for i in map_file_content[0].split(" ")][0], [int(i) for i in map_file_content[0].split(" ")][1]

    # Create labyrinth
    def create_labyrinth(self, map_file):   
        
        map_file_content, map_height, map_width = self.process_file(map_file)
        # map_squares: The 2D map matrix is represented by the bidimensional list of map squares
        # square_line: An auxiliar one-dimensional list of squares, representing a line, that will be appended to map_squares
        square_line = []
        self.map_squares = []
        # Relative coordinate for the 2D map matrix
        real_x_coord = 0
        real_y_coord = 0
        # Build the 2D map matrix by creating all map squares and appending them to the map_squares list
        for i in range(2, len(map_file_content), 2):
            real_x_coord = 0
            square_line = []
            for j in range(1, len(map_file_content[1])-1, 2):
                # Creating and appending map squares to the 2D map matrix
                if(map_file_content[i][j] == '0' or map_file_content[i][j] == '2'):
                    square_line.append(self.create_map_square(map_file_content, (i, j, real_y_coord, real_x_coord, map_width, map_height)))
                # Setting up the goal position in the map
                if(map_file_content[i][j] == '2'):
                    # target_x and target_y represents the goal position in the map
                    self.target_x = real_x_coord
                    # Modification to assure that the y axis is increasing (bottom -> up)
                    #self.target_y = map_height - (real_y_coord + 1)
                    self.target_y = real_y_coord
                real_x_coord += 1
            self.map_squares.append(square_line)
            real_y_coord += 1

    # Create and return a map square
    def create_map_square(self, map_file_content, coordinates):
        map_square_configuration = {
            'x': constant.LABYRINTH_X+(coordinates[3]*constant.SQUARE_SIZE),
            'y': constant.LABYRINTH_Y+(coordinates[2]*constant.SQUARE_SIZE),
            'map_x': coordinates[3],
            # Modification to assure that the y axis is increasing (bottom -> up)
            #'map_y': (coordinates[5]-(coordinates[2]+1)),
            'map_y': coordinates[2],
            'is_blocked_dict': self.calculate_blocked_dict(map_file_content, coordinates),
            'id': (coordinates[3] + (coordinates[4] * coordinates[2]))
        }
        return MapSquare(map_square_configuration)

    # Create a source of information (is_blocked_dict) to know where are the walls in a square
    # my_type: It corresponds to the map square type (0: normal empty block; 2: target/goal position)
    def calculate_blocked_dict(self, map_file_content, coordinates):
        is_blocked_dict = {
        'top': map_file_content[coordinates[0]-1][coordinates[1]],
        'bottom': map_file_content[coordinates[0]+1][coordinates[1]],
        'left': map_file_content[coordinates[0]][coordinates[1]-1],
        'right': map_file_content[coordinates[0]][coordinates[1]+1],
        'my_type': map_file_content[coordinates[0]][coordinates[1]]
        }
        return is_blocked_dict

    # Draw all 
    def draw(self, surface):
        for i in range(len(self.map_squares)):
            for j in range(len(self.map_squares[i])):
                # Draw normal map square
                self.map_squares[i][j].draw_walls(surface)
                # Draw pink background on target map position
                if(self.map_squares[i][j].map_x == self.target_x and self.map_squares[i][j].map_y == self.target_y):
                    self.map_squares[i][j].draw_target(surface)
                # Draw yellow square indicating the agent position
                if(self.map_squares[i][j].map_x == self.agent.map_x and self.map_squares[i][j].map_y == self.agent.map_y):
                    self.map_squares[i][j].draw_agent(surface)
