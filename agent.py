# The agent class tracks the agent position on the 2D map
class Agent:
    def __init__(self, attrib_dict):
        # map_x and map_y are abstract coordinates to represent the agent position and the target in the 2D map matrix
        # direction: (0 = left, 1 = down, 2 = right, 3 = up)
        valid_attributes = ("map_x", "map_y", "direction")
        for key in valid_attributes:
            self.__dict__[key] = attrib_dict[key]