import pygame
import constant
from q_learning import QLearning
from labyrinth import Labyrinth
from agent import Agent

# Main function, the first function called in the program
def main():

    # Create q-learning and other necessary objects for the window
    agent = create_agent()
    labyrinth = create_labyrinth(agent)
    q_learning_solver = create_q_learning_solver(labyrinth)
    screen = create_game_window()
    monospace_font, fps_clock, game_step_timed_event = create_window_objects()

    # Randomize agent initial position
    q_learning_solver.randomize_agent_position()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False      
            # Update the game for each game step (currently each constant.GAME_STEP_DELAY)
            if event.type == game_step_timed_event:

                q_learning_solver.decide_next_move()
                screen.fill(constant.COLOR_DICT['white'])
                draw_text_on_screen(monospace_font, screen, (agent, labyrinth, q_learning_solver))
                labyrinth.draw(screen)

        # true if agent in is target/goal position
        if(q_learning_solver.is_agent_on_goal()):
            q_learning_solver.randomize_agent_position()
                
        # Update game cycle based on a fps target
        fps_clock.tick(constant.FPS_TARGET)
        # Update and possibly repaint window
        pygame.display.update()

def create_window_objects():
    # Font creation
    monospace_font = pygame.font.SysFont(constant.FONT_NAME, constant.FONT_SIZE)

    # Timed event
    game_step_timed_event = constant.GAME_STEP_EVENT_ID
    pygame.time.set_timer(game_step_timed_event, constant.GAME_STEP_DELAY)

    # Defined FPS and FPS clock creation
    fps_clock = pygame.time.Clock()

    return monospace_font, fps_clock, game_step_timed_event

def create_game_window():

    # Initializing pygame and font
    pygame.init()
    pygame.font.init()

    # Set game window title
    pygame.display.set_caption(constant.WINDOW_TITLE)

    # Screen dimensions
    screen_dimensions = constant.WIDTH, constant.HEIGHT

    # Screen creation
    screen = pygame.display.set_mode(screen_dimensions)

    return screen

def create_q_learning_solver(labyrinth):
    # Setting up the q-learning R and Q matrixes
    q_learning_config_dict = {
    'labyrinth': labyrinth,
    'learning_rate': constant.STD_LEARNING_RATE,
    'exploration_chance': constant.STD_EXPLORATION_CHANCE
    }
    q_learning_solver = QLearning(q_learning_config_dict)
    return q_learning_solver

def create_labyrinth(agent):
     # Labyrinth map creation
    file_address = "maps/example_map.txt"
    map_file = open(file_address, "r")
    labyrinth = Labyrinth(map_file, agent)
    return labyrinth

def create_agent():
    # Agent configuration and creation
    agent_config_dict = {
    'map_x': constant.AGENT_MAP_X,
    'map_y': constant.AGENT_MAP_Y,
    'direction': constant.AGENT_DEFAULT_DIRECTION
    }
    agent = Agent(agent_config_dict)
    return agent

# Draw Q matrix on screen
def draw_matrix_text(font, screen, object_references):
    # object_references[0]: agent
    # object_references[1]: labyrinth
    # object_references[2]: q_learning_solver
    list_of_lines, state_text, action_text = create_matrix_texts(font, screen, object_references)
    below_map_y = object_references[1].map_squares[len(object_references[1].map_squares)-1][0].y+(2.5 * constant.FONT_SIZE)

    screen.blit(state_text, (50, below_map_y+(7*constant.FONT_SIZE)+((len(list_of_lines)/2)*0.8*constant.FONT_SIZE)))
    screen.blit(action_text, (200, below_map_y+(5.8*constant.FONT_SIZE)))
    for i in range(len(list_of_lines)):
        screen.blit(list_of_lines[i], (120, below_map_y+(7*constant.FONT_SIZE)+(i*0.9*constant.FONT_SIZE)))

# Draw the labyrinth map square ids at the top-left corner of a map square
def draw_labyrinth_map_square_id_text(font, screen, object_references):
    for i in range(len(object_references[1].map_squares)):
        for j in range(len(object_references[1].map_squares[i])):
            test_text = font.render(str(object_references[1].map_squares[i][j].id), constant.SMOOTH_EDGES,
                constant.COLOR_DICT['black'])
            screen.blit(test_text, (object_references[1].map_squares[i][j].x, object_references[1].map_squares[i][j].y))

# Draw texts for agent's current position, current epoch, total amount of steps and current exploration_chance from q-learning_solver
def draw_text_on_screen(font, screen, object_references):
    # object_references[0]: agent
    # object_references[1]: labyrinth
    # object_references[2]: q_learning_solver
    
    # Get list of texts to draw on screen
    list_of_texts = create_texts(font, screen, object_references)

    below_map_y = object_references[1].map_squares[len(object_references[1].map_squares)-1][0].y+(2.5 * constant.FONT_SIZE)

    # Drawing texts on screens
    for i in range(len(list_of_texts)):
        screen.blit(list_of_texts[i], (70, below_map_y+(1.5 * i * constant.FONT_SIZE)))

    # Draw Q matrix
    draw_matrix_text(font, screen, object_references)
    # Draw the labyrinth map square ids
    draw_labyrinth_map_square_id_text(font, screen, object_references)

# Create texts for agent's current position, current epoch, total amount of steps and current exploration_chance from q-learning_solver
def create_texts(font, screen, object_references):

    list_of_texts = []
    agent_position_text = font.render("Agent position: ("+str(object_references[1].agent.map_x)+
        ", "+str(object_references[1].agent.map_y)+")", constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    epoch_text = font.render("Epoch: "+str(object_references[2].epoch), constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    num_steps_text = font.render("Total steps: "+str(object_references[2].num_steps), constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    exploration_chance_text = font.render("exploration_chance: {:.2f}".format(object_references[2].exploration_chance),
     constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])

    list_of_texts.append(agent_position_text)
    list_of_texts.append(epoch_text)
    list_of_texts.append(num_steps_text)
    list_of_texts.append(exploration_chance_text)

    return list_of_texts

# Create matrix texts
def create_matrix_texts(font, screen, object_references):
    list_of_lines = []
    line = ""
    for i in range(len(object_references[1].map_squares) * len(object_references[1].map_squares[0])):
        line = ""
        for j in range(len(object_references[1].map_squares) * len(object_references[1].map_squares[0])):
            if(object_references[2].q_matrix[(i, j)] >= 100):
                line += str(object_references[2].q_matrix[(i, j)])+" "
            elif(object_references[2].q_matrix[(i, j)] >= 10 and object_references[2].q_matrix[(i, j)] < 100):
                line += str(object_references[2].q_matrix[(i, j)])+"  "
            elif(object_references[2].q_matrix[(i, j)] < 10):
                line += str(object_references[2].q_matrix[(i, j)])+"   "
        line_text = font.render(line, constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
        list_of_lines.append(line_text)

    state_text = font.render("state", constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    action_text = font.render("action", constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    return list_of_lines, state_text, action_text

if __name__ == "__main__": main()