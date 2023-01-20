## About: 
Tn intelligent agent that solves the N-puzzle game. Rules of the game can be found at mypuzzle.org/sliding. 
## Algorithms: 
The program uses bfs, dfs, and A* algorithms to solve the N-puzzle game. For each path searching algorithm it uses the manhattan distance. 
## Run: 
Type the following line in terminal, and the output is written in the text file: \
$ python3 puzzles.py [algorithm] [board configuration]
## Example output: 
$ python3 puzzle.py ast 1,3,5,7,2,4,6,0,8


path_to_goal: ['Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Up', 'Up', 'Right', 'Down', 'Left', 'Down', 'Right', 'Up', 'Right', 'Up', 'Left', 'Left'] 

cost_of_path: 19 

nodes_expanded: 625 

search_depth: 19 

max_search_depth: 19 

running_time: 0.02875304 

max_ram_usage: 0.00130089 
