from search_algorithms import bfs
from search_algorithms import dfs
from search_algorithms import iddfs
from search_algorithms import a_star
from heuristic import manhattan_heuristic
from heuristic import euclidean_heuristic
from game import Game
from time import time

def computer_play(initialState: list, gameType: bool, searchFunc, *args):
    # Create offline instance of the 8 puzzle for planning
    game = Game(initialState, gameType)
    start_time = time()
    frontier, nodes_expanded, max_depth, found, goal_state = searchFunc(game, *args)
    end_time = time()
    if found:
        # Find path to goal by looping through parents starting from goal and ending at root
        state = goal_state
        action_list = []
        while state.position != initialState:
            action_list.append(state.move)
            state = state.parent
        # Reverse actions to get final path
        action_list.reverse()
        print("Path to goal: " + ' -> '.join(action_list))
        # Cost for any action is 1 and therefore it will
        print("Cost of path: %d"%(len(action_list)))
    else:
        print("Failed to find solution :(")
    print("Nodes expanded: %d" % nodes_expanded)
    print("Search depth: %d" % max_depth)
    print("Searching time: %f" % (end_time - start_time))


initial_state = [6, 4, 3, 8, 1, 2, 5, 7, 0]
#initial_state = [1, 0, 2, 3, 4, 5, 6, 7, 8]
#initial_state = [1, 2, 5, 3, 4, 0, 6, 7, 8]
#initial_state = [int(x) for x in list('753816240')]
#initial_state = [int(x) for x in list('210354678')]
print("A* Manhattan:")
computer_play(initial_state, True, a_star, manhattan_heuristic)
print("\nA* Euclidean:")
computer_play(initial_state, True, a_star, euclidean_heuristic)
print("\nBFS:")
computer_play(initial_state, True, bfs)
print("\nDFS:")
computer_play(initial_state, True, dfs)
print("\nIterative Deepening:")
computer_play(initial_state, True, iddfs)
