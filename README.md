# q-learning-labyrinth-solver

A visual representation of a q-learning algorithm solving a labyrinth. The project is being developed with Python and pygame modules. 

Q-learning is a model-free reinforcement learning algorithm. Q-learning is also an unsupervised training algorithm and therefore it does not use examples or previously known references.

As of reinforcement learning, q-learning involves an agent, a set of states and set of actions. In my application: 
• The agent is an entity that wants to reach a 
• A state would be the current position of the agent
• A action would be the agent movement to an adjacent position.

Q-learning also involves a reward matrix (the R matrix) and a memory/knowledge matrix with all (state, action) possible.

My application builds a map from a map file, currently in "example_map.txt".
• *: Indicates a wall or blocking object
• 0: An empty square
• 1: Indicates a path between two squares
• 2: Indicates goal position

![](pictures/q-learning_map.PNG)

Before training, all values in the Q value matrix are 0's:

![](pictures/q-learning_untrained.PNG)

After training, the agent has a memory/knowledge (filled Q matrix) of the path to the target/goal position:

![](pictures/q-learning_trained.PNG)
