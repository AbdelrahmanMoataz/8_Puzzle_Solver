

"""
Convert index of a tile in state to coordinates
"""

"""
Convert index of a tile in state to coordinates
"""
def find_coordinates(position: list, tile=0):
    match position.index(tile):
        case 0:
            return 1, 1
        case 1:
            return 1, 2
        case 2:
            return 1, 3
        case 3:
            return 2, 1
        case 4:
            return 2, 2
        case 5:
            return 2, 3
        case 6:
            return 3, 1
        case 7:
            return 3, 2
        case 8:
            return 3, 3

"""
Manhattan distance is the sum of horizontal and vertical moves required to reach goal state from current state
"""
def manhattan_heuristic(current_state: list, goal: list):
    heuristic = 0
    for i in range(0, 9):
        current_x, current_y = find_coordinates(current_state, i)
        goal_x, goal_y = find_coordinates(goal, i)
        heuristic += abs(current_x - goal_x) + abs(current_y - goal_y)
    return heuristic

"""
Euclidean distance is the distance of the straight line connecting the current state tiles to goal state tiles
"""
def euclidean_heuristic(current_state: list, goal: list):
    heuristic = 0
    for i in range(0, 9):
        current_x, current_y = find_coordinates(current_state, i)
        goal_x, goal_y = find_coordinates(goal, i)
        heuristic = ((current_x - goal_x) ** 2 + abs(current_y - goal_y) ** 2) ** 0.5
    return heuristic

