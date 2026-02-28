from collections import deque
from game import Game
from game import State
import heapq


"""
Breadth First Search function. Takes a game object as input and returns frontier, visited, max depth and goal state.
"""
def bfs(game: Game):
    # Initialise root state
    initial_state = State(game.start)
    # deque is faster with queues
    frontier = deque([initial_state])
    # Create dictionary containing all states in both visited and frontier
    frontier_dict = {initial_state: True}
    # Count number of nodes visited
    nodes_expanded = 0
    # Initialise the max_depth variable
    max_depth = 0
    # Initialise a flag that checks if goal state was found or not
    found = False
    # Only exit loop if frontier is empty
    while frontier:
        # Since BFS uses queues, we pop leftmost element (which entered first)
        state = frontier.popleft()
        # A state popped from frontier is considered visited and will be marked as False (no longer in frontier)
        frontier_dict[state] = False
        # Compare max_depth variable to current state depth. Will return maximum depth of search (of explored nodes)
        max_depth = max(max_depth, state.depth)
        # Update the game state by the state popped from frontier (required to find children of this state)
        game.current = state.position # Update the current position being explored for the game
        # Marks state as explored
        nodes_expanded += 1
        # Goal check, terminates the search if the goal is found
        if state.position == game.end:
            found = True
            return frontier, nodes_expanded, max_depth, found, state
        # If goal not found, need to update the frontier for next loop
        # Find the children of the current state
        action_list = ['up', 'down', 'left', 'right']
        # Loop through all possible actions to find children
        for action in action_list:
            # Initialise a new state whose position will be the parent state after an action is performed on it
            new_state = State(game.move(action))
            # An invalid action will return the parent position with no change. This checks make sure the parent state
            # will not become a child of itself.
            if new_state.position != game.current:
                # Assign the attributes of the valid child state
                new_state.move = action
                new_state.parent = state
                new_state.depth = state.depth + 1
                # Add new state to list of children of parent state
                state.children.append(new_state)
        # Add the applicable children to the frontier
        for child in state.children:
            # Check if child is in either frontier or visited through dictionary (O(1))
            if child not in frontier_dict:
                frontier_dict[child] = True
                frontier.append(child)
    # Only when the frontier is empty will the search end with failure (no goal state found)
    return frontier, nodes_expanded, max_depth, found, 0


"""
Depth First Search with depth limit functionality. Give limit = -1 for unlimited depth.
"""
def dfs(game: Game, limit = -1):
    # Most of DFS code will be similar to BFS
    initial_state = State(game.start)
    frontier = deque([initial_state])
    # Instead of marking if the state is in frontier or not, mark it with its depth
    frontier_dict = {initial_state: initial_state.depth}
    nodes_expanded = 0
    max_depth = 0
    found = False
    while frontier:
        # Since DFS uses stack, we pop rightmost element (which entered last)
        state = frontier.pop()
        max_depth = max(max_depth, state.depth)
        game.current = state.position
        nodes_expanded += 1
        # Goal Check
        if state.position == game.end:
            found = True
            return frontier, nodes_expanded, max_depth, found, state
        # If limit exists, only execute code to add children if current state depth is lower than limit
        # This condition is ignored if limit is -1
        if state.depth < limit or limit == -1:
            action_list = ['up', 'down', 'left', 'right']
            for action in action_list:
                new_state = State(game.move(action))
                if new_state.position != game.current:
                    new_state.move = action
                    new_state.parent = state
                    new_state.depth = state.depth + 1
                    state.children.append(new_state)
            for child in state.children:
                # If a limit exists, a second condition is added that will allow adding of states to frontier
                # that were already explored / in frontier only if their depth is lower than those in visited/frontier.
                # If limit is -1, this condition is ignored and only use the BFS check to avoid infinite loops.
                if child not in frontier_dict or (child.depth < frontier_dict.get(child, 0) and limit != -1):
                    frontier_dict[child] = child.depth
                    frontier.append(child)
    return frontier, nodes_expanded, max_depth, found, 0

"""
Iterative Deepening DFS. Can give maximum number of iterations of DFS before stopping
"""
def iddfs(game: Game, iter = float('inf')):
    # Iterating depth for DLS
    i = 0
    # Need to count the number of nodes expanded each loop
    nodes_expanded = 0
    # Loop for the number of iterations given. Not <= because loop starts from i = 0
    while i < iter:
        frontier, explored, max_depth, found , state = dfs(game, i)
        nodes_expanded += explored
        i += 1
        if found:
            return frontier, nodes_expanded, max_depth, found , state
    # If search failed to find goal within maximum iterations, only return nodes expanded, max depth which will be
    # no. of iterations - 1, and the found flag as False
    return 0, nodes_expanded, iter - 1, False, 0

"""
A* search. 
"""
def a_star(game: Game, heuristic):
    initial_state = State(game.start, 'A*')
    # This heuristic will be used as the priority for our priority queue
    initial_state.h = heuristic(game.start, game.end)
    frontier = []
    entry_count = 1
    # Elements of frontier are composed of tuples. The State object is coded to compare cost function automatically
    # as priority. Entry count acts as a tiebreak if duplicate priorities exist
    heapq.heappush(frontier, (initial_state, entry_count))
    # The dictionary this time will contain a list whose first element is the cost function of state and second element
    # is a check if the state
    #frontier_dict = {initial_state: [initial_state.cost(), True]}
    frontier_dict = {initial_state: initial_state.cost()}
    # Although dictionary already contains both frontier and visited, a future check requires visited states only
    # so this time we will create a set for visited states instead of counting nodes expanded
    visited = set()
    max_depth = 0
    found = False
    while frontier:
        state = heapq.heappop(frontier)[0]  # First element of tuple is the state object
        # If a state that was already visited is popped from frontier again, ignore the loop
        # This acts as decrease key functionality of the priority queue
        if state in visited:
            continue
        max_depth = max(max_depth, state.depth)
        game.current = state.position
        visited.add(state)
        # Goal Check
        if state.position == game.end:
            found = True
            return frontier, len(visited), max_depth, found, state
        # Add children
        action_list = ['up', 'down', 'left', 'right']
        for action in action_list:
            new_state = State(game.move(action), 'A*')
            if new_state.position != game.current:
                new_state.move = action
                new_state.parent = state
                new_state.depth = state.depth + 1
                # For A*, need to assign the state cost and heuristic
                new_state.g = state.g + 1   # Edge cost is always 1 for the 8 puzzle (added to parent cost)
                new_state.h = heuristic(new_state.position, game.end)
                state.children.append(new_state)
        for child in state.children:
            # Only add child if it was never visited
            if child not in visited:
                # Only add child if was also not in frontier OR if it has lower cost than one that exists in frontier
                if child not in frontier_dict or child.cost() < frontier_dict.get(child, 0):
                    entry_count += 1
                    heapq.heappush(frontier, (child, entry_count))
                    frontier_dict[child] = child.cost()

    return frontier, len(visited), max_depth, found, 0  # Only when the frontier is empty will the search end with failure (no goal state found)
