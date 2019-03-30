from labyrinth import Labyrinth
import random

class QLearning:
    def __init__(self, attrib_dict):
        # learning_rate(0.0 to 1.0): Gamma (Q-learning learning rate)
        # exploration_chance(0.0 to 1.0): Probability for the agent to randomly pick a course of action
        valid_attributes = ("labyrinth", "learning_rate", "exploration_chance")
        for key in valid_attributes:
            self.__dict__[key] = attrib_dict[key]
        # Reward matrix
        self.r_matrix = self.create_r_matrix()
        # Q matrix represents the agent's brain/memory
        self.q_matrix = self.create_q_matrix()
        # Incremented when agent reaches goal/target during training
        self.epoch = 0
        # Total number of steps by the agent
        self.num_steps = 0

    # Create and return reward matrix
    def create_r_matrix(self):
        r_matrix = {}
        
        for i in range(len(self.labyrinth.map_squares)):
            for j in range(len(self.labyrinth.map_squares[i])):
                for k in range(len(self.labyrinth.map_squares)):
                    for l in range(len(self.labyrinth.map_squares[i])):
                        r_matrix[(self.labyrinth.map_squares[i][j].id, self.labyrinth.map_squares[k][l].id)] = -1
                # Check if it is possible to reach adjacent map squares (no walls in between) from self.labyrinth.map_squares[i][j]
                r_matrix = self.check_and_create_connections((i, j), r_matrix, 0)
                if(self.labyrinth.map_squares[i][j].is_blocked_dict["my_type"] == '2'):
                    r_matrix = self.check_and_create_connections((i, j), r_matrix, 100)
        return r_matrix

    # Function that checks and creates all (state, action) -> score pairs
    def check_and_create_connections(self, coordinates, r_matrix, score):
        current_square = self.labyrinth.map_squares[coordinates[0]][coordinates[1]]
        if(coordinates[0] != 0 and current_square.is_blocked_dict["top"] == '1'):
            top_square = self.labyrinth.map_squares[coordinates[0]-1][coordinates[1]]
            r_matrix = self.determine_r_matrix_state_action((current_square.id, top_square.id), r_matrix, score)
        if(coordinates[0] != len(self.labyrinth.map_squares)-1 and current_square.is_blocked_dict["bottom"] == '1'):
            bottom_square = self.labyrinth.map_squares[coordinates[0]+1][coordinates[1]]
            r_matrix = self.determine_r_matrix_state_action((current_square.id, bottom_square.id), r_matrix, score)
        if(coordinates[1] != len(self.labyrinth.map_squares[coordinates[0]])-1 and current_square.is_blocked_dict["right"] == '1'):
            right_square = self.labyrinth.map_squares[coordinates[0]][coordinates[1]+1]
            r_matrix = self.determine_r_matrix_state_action((current_square.id, right_square.id), r_matrix, score)
        if(coordinates[1] != 0 and current_square.is_blocked_dict["left"] == '1'):
            left_square = self.labyrinth.map_squares[coordinates[0]][coordinates[1]-1]
            r_matrix = self.determine_r_matrix_state_action((current_square.id, left_square.id), r_matrix, score)
        return r_matrix

    def determine_r_matrix_state_action(self, state_action_pair, r_matrix, score):
        if(score == 0):
            r_matrix[(state_action_pair[0], state_action_pair[1])] = score
        elif(score == 100):
            r_matrix[(state_action_pair[1], state_action_pair[0])] = score
        return r_matrix

    # Create and return the Q matrix for the labyrinth
    def create_q_matrix(self):
        q_matrix = {}
        for i in range(len(self.labyrinth.map_squares)):
            for j in range(len(self.labyrinth.map_squares[i])):
                for k in range(len(self.labyrinth.map_squares)):
                    for l in range(len(self.labyrinth.map_squares[i])):
                        q_matrix[(self.labyrinth.map_squares[i][j].id, self.labyrinth.map_squares[k][l].id)] = 0
        
        return q_matrix

    # Randomize agent position
    def randomize_agent_position(self):
        self.labyrinth.agent.map_y = random.randint(0, len(self.labyrinth.map_squares)-1)
        self.labyrinth.agent.map_x = random.randint(0, len(self.labyrinth.map_squares[self.labyrinth.agent.map_y])-1)
        # Check if the agent new randomized position is equal to the target/goal position
        # If true, randomize again
        while(self.labyrinth.agent.map_x == self.labyrinth.target_x and self.labyrinth.agent.map_y == self.labyrinth.target_y):
            self.labyrinth.agent.map_y = random.randint(0, len(self.labyrinth.map_squares)-1)
            self.labyrinth.agent.map_x = random.randint(0, len(self.labyrinth.map_squares[self.labyrinth.agent.map_y])-1)
    
    
    # Check if agent is on goal position
    def is_agent_on_goal(self):
        if(self.labyrinth.agent.map_x == self.labyrinth.target_x and self.labyrinth.agent.map_y == self.labyrinth.target_y):
            self.epoch += 1
            self.exploration_chance -= 0.02
            if(self.exploration_chance < 0.0):
                self.exploration_chance = 0.0
            return True
        return False

    def decide_next_move(self):
        # key: directions ("left", "bottom", "right", "top")
        # value: tuples with (next_move_position.id and q_matrix[(current_position.id ,next_move_position.id)])
        q_value_direction_dict = self.create_q_value_direction_dict(self.labyrinth.agent.map_x, self.labyrinth.agent.map_y)
        max_q_value, max_direction, available_directions = self.calculate_next_move_data(q_value_direction_dict)
        if(max_q_value == 0):
            self.decide_when_no_max_value(available_directions, q_value_direction_dict)
        else:  
            # Decide next move based on Q table
            if(random.random() > self.exploration_chance):
                self.decide_when_max_value(available_directions, max_direction, q_value_direction_dict)
            # The agent decided to explore the map randomly
            else:
                self.decide_when_no_max_value(available_directions, q_value_direction_dict)
        self.num_steps += 1

    # Function that determines the max Q value for all current possible (state, action), the direction in which the Q value is maxed and the
    # available directions in case the action is decided at random (all Q values are 0 or the agent decides to explore)
    def calculate_next_move_data(self, q_value_direction_dict):
        max_q_value = 0
        max_direction = ""
        available_directions = []
        for key in q_value_direction_dict:
            # The agent must not stay in the same place, it must not choose "my_type" as next move
            if(key != 'my_type'):
                available_directions.append(key)
            if(q_value_direction_dict[key][1] > max_q_value):
                max_q_value = q_value_direction_dict[key][1]
                max_direction = key
        return max_q_value, max_direction, available_directions

    # Update the Q(state, action)
    def adjust_q_table(self, direction_to_go, q_value_direction_dict):
        # R(state, action)
        reward = self.r_matrix[(q_value_direction_dict["my_type"][0], q_value_direction_dict[direction_to_go][0])]
        dif_x, dif_y = self.calculate_current_position_offset(direction_to_go)
        q_value_next_move_data_dict = self.create_q_value_direction_dict(self.labyrinth.agent.map_x+dif_x, self.labyrinth.agent.map_y+dif_y)
        max_q_value_next_move = self.calculate_next_move_data(q_value_next_move_data_dict)[0]
        # Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]
        self.q_matrix[(q_value_direction_dict["my_type"][0],q_value_direction_dict[direction_to_go][0])] = int(reward + (self.learning_rate * max_q_value_next_move))

    # Function that calculates the position offset to the adjacent square
    def calculate_current_position_offset(self, direction_to_go):
        dif_x = 0
        dif_y = 0
        if(direction_to_go == "left"):
            dif_x -= 1
        if(direction_to_go == "right"):
            dif_x += 1
        if(direction_to_go == "bottom"):
            dif_y += 1
        if(direction_to_go == "top"):
            dif_y -= 1
        return dif_x, dif_y

    # The next move will be the greatest (state, action) in Q table
    def decide_when_max_value(self, available_directions, direction_to_go, q_value_direction_dict):
        self.adjust_q_table(direction_to_go, q_value_direction_dict)

        if(direction_to_go == "left"):
            self.labyrinth.agent.map_x -= 1
        if(direction_to_go == "right"):
            self.labyrinth.agent.map_x += 1
        if(direction_to_go == "bottom"):
            self.labyrinth.agent.map_y += 1
        if(direction_to_go == "top"):
            self.labyrinth.agent.map_y -= 1

    # All (state, action) in Q table have value 0
    def decide_when_no_max_value(self, available_directions, q_value_direction_dict):

        random_index = random.randint(0, len(available_directions)-1)
        random_direction = available_directions[random_index]
        self.adjust_q_table(random_direction, q_value_direction_dict)

        if(random_direction == "left"):
            self.labyrinth.agent.map_x -= 1
        if(random_direction == "right"):
            self.labyrinth.agent.map_x += 1
        if(random_direction == "bottom"):
            self.labyrinth.agent.map_y += 1
        if(random_direction == "top"):
            self.labyrinth.agent.map_y -= 1

    # Create a dictionary with:
    # key: directions ("left", "bottom", "right", "top")
    # value: tuples with (next_move_position.id and q_matrix[(current_position.id ,next_move_position.id)])
    def create_q_value_direction_dict(self, x, y):
        q_value_direction_dict = {}
        current_position_x = x
        current_position_y = y

        current_position = self.labyrinth.map_squares[current_position_y][current_position_x]
        directions = ["left", "bottom", "right", "top", "my_type"]
        for dir in directions:
            if(current_position.is_blocked_dict[dir] == '1' or current_position.is_blocked_dict[dir] == '0'):
                target_position = (self.get_map_square_with_direction(current_position_x, current_position_y, dir))
                q_value_direction_dict[dir] = (target_position.id, self.q_matrix[(current_position.id, target_position.id)])
        
        return q_value_direction_dict

    # Function that determines and returns the correct adjacent map square to the current agent's map position depending on the direction parameter
    def get_map_square_with_direction(self, x, y, direction):
        if(direction == "left"):
            return self.labyrinth.map_squares[y][x-1]
        if(direction == "right"):
            return self.labyrinth.map_squares[y][x+1]
        if(direction == "bottom"):
            return self.labyrinth.map_squares[y+1][x]
        if(direction == "top"):
            return self.labyrinth.map_squares[y-1][x]
        if(direction == "my_type"):
            return self.labyrinth.map_squares[y][x]