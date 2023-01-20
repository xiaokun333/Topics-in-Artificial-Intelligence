from __future__ import division
from __future__ import print_function

import sys
import math
import time
import resource
from queue import Queue as Q
import heapq



#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []
        self.tot_cost = calculate_total_cost(self)

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)
        
    def __eq__(self, o):
        for idx in range(self.n * self.n):
            if self.config[idx] != o.config[idx]:
                return False
        return True
    
    def __hash__(self):
        num = 0
        for i in range(9):
            num = num + self.config[i]*pow(10, 8-i)
        return hash(num)
    
    def __lt__(self, o):
        return self.tot_cost < o.tot_cost

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        idx = 0
        #find 0
        for i in range(self.n * self.n):
            if self.config[i] == 0:
                idx = i
                break
             
        if idx < 3:
            return None
        
        else:
            # deep copy the old config
            new_config = list(self.config)
            # move up
            temp = new_config[i - 3] 
            new_config[i - 3] = new_config[i]
            new_config[i] = temp
            new_cost = self.cost + 1
            
            new_state = PuzzleState(new_config, self.n, self, "Up", new_cost)
            return new_state
            
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        idx = 0
        #find 0
        for i in range(self.n * self.n):
            if self.config[i] == 0:
                idx = i
                break
            
        if idx > 5:
            return None
        
        else:
            # deep copy the old config
            new_config = list(self.config)
            # move up
            temp = new_config[i + 3] 
            new_config[i + 3] = new_config[i]
            new_config[i] = temp
            new_cost = self.cost + 1
            
            new_state = PuzzleState(new_config, self.n, self, "Down", new_cost)
            return new_state
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        idx = 0
        #find 0
        for i in range(self.n * self.n):
            if self.config[i] == 0:
                idx = i
                break
            
        if idx % 3 == 0:
            return None
        
        else:
            # deep copy the old config
            new_config = list(self.config)
            # move up
            temp = new_config[i - 1] 
            new_config[i - 1] = new_config[i]
            new_config[i] = temp
            new_cost = self.cost + 1
            
            new_state = PuzzleState(new_config, self.n, self, "Left", new_cost)
            return new_state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        idx = 0
        #find 0
        for i in range(self.n * self.n):
            if self.config[i] == 0:
                idx = i
                break
            
        if (idx - 2) % 3 == 0:
            return None
        
        else:
            # deep copy the old config
            new_config = list(self.config)
            # move up
            temp = new_config[i + 1] 
            new_config[i + 1] = new_config[i]
            new_config[i] = temp
            new_cost = self.cost + 1
            
            new_state = PuzzleState(new_config, self.n, self, "Right", new_cost)
            return new_state

      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children
    
    


# In[12]:


#path_to_goal = []
# Function that Writes to output.txt                     

### Students need to change the method to have the corresponding parameters
def writeOutput(path, cost_of_path, nodes_expanded, search_depth, max_search_depth, run_time, max_ram):
    ### Student Code Goes here
    #actions = list()
    

    file = open("output.txt", "w")
    file.write("path_to_goal: " + str(path) + "\n")
 
    file.write("cost_of_path: " + str(cost_of_path) + "\n")
    file.write("nodes_expanded: " + str(nodes_expanded) + "\n")
    file.write("search_depth: " + str(search_depth) + "\n") 
    file.write("max_search_depth: " + str(max_search_depth) + "\n") 
    file.write("running_time: " )
    file.write('%.8f' % run_time + "\n")
 
    file.write("max_ram_usage: ")
    file.write('%.8f' % max_ram + "\n")
    
    file.close()

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    # goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    start_time = time.time()
    #bfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    visited = set()
    fringe_set = set() # node in the fringe not explored
    queue = Q()
    queue.put(initial_state)
    count = 0 # number of nodes explored
    max_search_depth = 0
    
    while (not queue.empty()):
        cur = queue.get()
        visited.add(cur)
    
        if test_goal(cur) == True:
            
            path = []
            state = cur
            while (state is not None):
                path.append(state.action)
                state = state.parent
                
            path.reverse()
            path = path[1 : ]
            bfs_end_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(10**10))
            #writeOutput()
            end_time = time.time()
            writeOutput(path, len(path), count, cur.cost, max_search_depth, end_time - start_time, bfs_end_ram)
            # print(count)
            # print(max_search_depth)
            # print(cur.cost)
            # print(bfs_end_ram)
            # print("run time: ", end_time - start_time)
            # print(path)
            return
        # print(cur.config)
        cur.expand()
        
        for child in cur.children:
            if child not in visited and child not in fringe_set:
                queue.put(child)
                fringe_set.add(child)
                #visited.add(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
        count += 1

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    #bfs_start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    visited = set()
    fringe_set = set() # node in the fringe not explored
    stack = []
    stack.append(initial_state)
    count = 0 # number of nodes explored
    max_search_depth = 0
    
    while len(stack) != 0:
        cur = stack.pop()
        
        visited.add(cur)
        if test_goal(cur) == True:
            path = []
            state = cur
            while (state is not None):
                path.append(state.action)
                state = state.parent
            path.reverse()
            path = path[1 : ]
            dfs_end_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(10**10))
            #writeOutput()
            end_time = time.time()
            writeOutput(path, len(path), count, cur.cost, max_search_depth, end_time - start_time, dfs_end_ram)
            return
        
        cur.expand()
        for child in reversed(cur.children):
            if child not in visited and child not in fringe_set:
                stack.append(child)
                fringe_set.add(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
        count += 1
            
                
    
    

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    frontier = [initial_state]
    # heapq.heapify(frontier)
    visited = set()
    start_time = time.time()
    fringe_set = set() # node in the fringe not explored
    count = 0 # number of nodes explored
    max_search_depth = 0
    
    while frontier:
        cur = heapq.heappop(frontier)
        visited.add(cur)
        
        if test_goal(cur) == True:
            path = []
            state = cur
            while (state is not None):
                path.append(state.action)
                state = state.parent
            path.reverse()
            path = path[1 : ]
            ast_end_ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(10**10))
            #writeOutput()
            end_time = time.time()
            writeOutput(path, len(path), count, cur.tot_cost, max_search_depth, end_time - start_time, ast_end_ram)
            return
        
        cur.expand()
        for child in cur.children:
            if child not in visited and child not in fringe_set:
                heapq.heappush(frontier, child)
                # frontier.heappush(child)
                fringe_set.add(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
                
        count += 1
    
    
    

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    sum = state.cost
    
    for i in range(state.n * state.n):
        if state.config[i] == 0:
            continue
        sum += calculate_manhattan_dist(i, state.config[i], state.n)
    return sum
def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    x_idx = idx % n
    y_idx = idx // n
    x_val = value % n
    y_val = value // n
    dist = abs(x_idx - x_val) + abs(y_idx - y_val)
    return dist

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    for idx, item in enumerate(puzzle_state.config):
        if idx != item:
            return False
    return True




# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()


# l = [6, 5, 4, 3, 2, 1]
# heapq.heapify(l)
# heapq.heap
# print(type(l))
# In[ ]:



