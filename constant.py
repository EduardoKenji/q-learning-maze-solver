# Game properties
WINDOW_TITLE = 'Q-learning labyrinth solver'
WIDTH = 720
HEIGHT = 720
FONT_SIZE = 20
FONT_NAME = 'monospace'
SMOOTH_EDGES = 1
GAME_STEP_DELAY = 70
GAME_STEP_EVENT_ID = 25
FPS_TARGET = 63
# Color dictionary with some colors and their respective RGB values ranging from 0 to 255
COLOR_DICT = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'pink': (255, 105, 180),
    'yellow': (250, 218, 94)
}
# Labyrinth properties
LABYRINTH_X = 70
LABYRINTH_Y = 70
# Map square properties
SQUARE_SIZE = 35
SQUARE_FILLED = 0
SQUARE_EMPTY = 1
WALL_WIDTH = 2
# Agent default properties
AGENT_MAP_X = 0
AGENT_MAP_Y = 3
AGENT_DEFAULT_DIRECTION = 0
# Q-learning default configuration and properties
STD_LEARNING_RATE = 0.8
STD_EXPLORATION_CHANCE = 0.75