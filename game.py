class Game:
    def __init__(self, start: list, ascending: bool):
        # Initial game state
        self.start = [x for x in start]  # Create a copy of the start list instead of passing the list itself
        # Choose if goal is with empty pace at start or end
        if ascending:
            self.end = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            self.end = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        # Define an attribute for the current game state, it will start at initial state
        self.current = [x for x in start] # Create a copy of the start list instead of passing the list itself


    def move(self, action: str) -> list:
        current = [x for x in self.current]
        # For a list, moving up or down is the same as moving 3 indices
        up_down_offset = 3
        # For a list, moving left or right is the same as moving 1 index
        left_right_offset = 1
        # Find the position of empty space at current game state
        current_position = current.index(0)
        # To find the new state, add or subtract an offset based on given action
        new_position = current_position
        # Exceptions are made when the empty space is on the left side and trying to move left, or when the empty
        # space in on the right side and trying to move right. These are illegal moves and therefore won't change
        # current state
        match action.lower():
            case 'up':
                new_position -= up_down_offset
            case 'down':
                new_position += up_down_offset
            case 'left':
                if current_position in [0, 3, 6]:
                    return current
                else:
                    new_position -= left_right_offset
            case 'right':
                if current_position in [0, 2, 5]:
                    return current
                else:
                    new_position += left_right_offset
        # A move is only possible if the new position of the empty space is within the indices of the game state list
        if 0 <= new_position <= 8:
        # After finding the new position of the empty space, swap its place with the element at that index
            current[current_position], current[new_position] = current[new_position], current[current_position]
        # Otherwise, return current state without changes
        return current

    def play_manual(self):
        while self.current != self.end:
            print(self.current)
            command = input("Enter action: ")
            self.move(command)
        print(self.current)
        print("You won the game!")

class State:
    def __init__(self, position: list, algorithm = 'other'):
        self.depth = 0
        self.position = position
        self.parent = 0
        self.children = []  # List of neighbors
        self.move = ''  # Action that got you to this state
        self.g = 0.0  # Cost to reach state from root
        self.h = 0.0  # Heuristic, approximated cost to reach goal from this state
        self.algorithm = algorithm

    """
    Cost function of the state depends on the search algorithm
    """
    def cost(self):
        match self.algorithm:
            case 'A*':
                return self.g + self.h
            case 'Greedy':
                return self.h
            case 'UCS':
                return self.g
            case 'other':
                return 0
    # heapq maintains heap invariant through '<' operations. This magic method makes sure any less than comparisons
    # compare only cost (making it the priority)
    def __lt__(self, other):
        return self.cost() < other.cost()
    # Child in frontier/visited comparisons will compare the position attribute only
    def __eq__(self, other):
        return self.position == other.position
    # Allow using state in a set, or as a key for a dictionary entry
    def __hash__(self):
        return hash(' '.join(map(str, self.position)))

