import pygame
import constant
from q_learning import QLearning
from labyrinth import Labyrinth
from agent import Agent

def main():

    # Agent configuration and creation
    agent_config_dict = {
    'map_x': constant.AGENT_MAP_X,
    'map_y': constant.AGENT_MAP_Y,
    'direction': constant.AGENT_DEFAULT_DIRECTION
    }
    agent = Agent(agent_config_dict)

    # Labyrinth map creation
    file_address = "example_map.txt"
    map_file = open(file_address, "r")
    labyrinth = Labyrinth(map_file, agent)

    # Setting up the q-learning R and Q matrixes
    q_learning_config_dict = {
    'labyrinth': labyrinth,
    'learning_rate': constant.STD_LEARNING_RATE,
    'exploration_chance': constant.STD_EXPLORATION_CHANCE
    }
    q_learning_solver = QLearning(q_learning_config_dict)

    # Screen dimensions
    screen_dimensions = constant.WIDTH, constant.HEIGHT

    # Initializing pygame and font
    pygame.init()
    pygame.font.init()

    # Set game window title
    pygame.display.set_caption('Q-learning labyrinth solver')

    # Screen creation
    screen = pygame.display.set_mode(screen_dimensions)

    # Font creation
    monospace_font = pygame.font.SysFont("monospace", constant.FONT_SIZE)

    # Timed event
    game_step_timed_event = constant.GAME_STEP_EVENT_ID
    pygame.time.set_timer(game_step_timed_event, constant.GAME_STEP_DELAY)

    # Defined FPS and FPS clock creation
    fps_clock = pygame.time.Clock()

    # Randomize agent position
    q_learning_solver.randomize_agent_position()

    #q_learning_solver.decide_next_move()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False      
            # Update the game for each game step (currently 130 milliseconds)
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

def draw_matrix(font, screen, object_references):

    below_map_y = object_references[1].map_squares[len(object_references[1].map_squares)-1][0].y+(2.5 * constant.FONT_SIZE)

    list_of_lines = []
    line = ""
    for i in range(12):
        line = ""
        for j in range(12):
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
    screen.blit(state_text, (50, below_map_y+(7*constant.FONT_SIZE)+((len(list_of_lines)/2)*0.8*constant.FONT_SIZE)))
    screen.blit(action_text, (200, below_map_y+(5.8*constant.FONT_SIZE)))
    for i in range(len(list_of_lines)):
        screen.blit(list_of_lines[i], (120, below_map_y+(7*constant.FONT_SIZE)+(i*0.9*constant.FONT_SIZE)))


def draw_text_on_screen(font, screen, object_references):
    # object_references[0]: agent
    # object_references[1]: labyrinth
    # object_references[2]: q_learning_solver
    below_map_y = object_references[1].map_squares[len(object_references[1].map_squares)-1][0].y+(2.5 * constant.FONT_SIZE)

    player_position_text = font.render("Agent position: ("+str(object_references[1].agent.map_x)+
        ", "+str(object_references[1].agent.map_y)+")", constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    epoch_text = font.render("Epoch: "+str(object_references[2].epoch), constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    num_steps_text = font.render("Total steps: "+str(object_references[2].num_steps), constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])
    exploration_chance_text = font.render("exploration_chance: {:.2f}".format(object_references[2].exploration_chance),
     constant.SMOOTH_EDGES, constant.COLOR_DICT['black'])

    screen.blit(player_position_text, (70, below_map_y))
    screen.blit(epoch_text, (70, below_map_y+(1.5 * constant.FONT_SIZE)))
    screen.blit(num_steps_text, (70, below_map_y+(3 * constant.FONT_SIZE)))
    screen.blit(exploration_chance_text, (70, below_map_y+(4.5 * constant.FONT_SIZE)))

    for i in range(len(object_references[1].map_squares)):
        for j in range(len(object_references[1].map_squares[i])):
            test_text = font.render(str(object_references[1].map_squares[i][j].id), constant.SMOOTH_EDGES,
                constant.COLOR_DICT['black'])
            screen.blit(test_text, (object_references[1].map_squares[i][j].x, object_references[1].map_squares[i][j].y))

    draw_matrix(font, screen, object_references)

if __name__ == "__main__": main()