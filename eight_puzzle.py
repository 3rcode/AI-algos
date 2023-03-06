import argparse
import timeit
from collections import deque


class PuzzleState:
    def __init__(self, state, parent, action, depth, cost, key):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost
        self.key = key

        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map

    def __gt__(self, other):
        return self.map > other.map

    def __str__(self):
        return str(self.map)


# Global Variables
GoalState = None
GoalNode = None
NodesExpanded = 0
MaxFrontierSize = 0
MaxSearchDepth = 0


# BFS
def bfs(initial_state):
    global MaxFrontierSize, MaxSearchDepth, GoalNode
    board_visited = set()
    queue = deque([PuzzleState(initial_state, None, None, 0, 0, 0)])
    while queue:
        node = queue.popleft()
        board_visited.add(node.map)
        if node.state == GoalState:
            GoalNode = node
            return "Goal!"

        possible_paths = get_possible_paths(node)
        for path in possible_paths:
            if path.map not in board_visited:
                queue.append(path)
                board_visited.add(path.map)
                if path.depth > MaxSearchDepth:
                    MaxSearchDepth = path.depth
        if len(queue) > MaxFrontierSize:
            MaxFrontierSize = len(queue)
    return "No Solution"


# get_possible_paths
def get_possible_paths(node):
    global NodesExpanded
    NodesExpanded += 1
    possible_paths = list()
    possible_paths.append(PuzzleState(move(node.state, 'Up'), node, 'Up', node.depth + 1, node.cost + 1, 0))
    possible_paths.append(PuzzleState(move(node.state, 'Down'), node, 'Down', node.depth + 1, node.cost + 1, 0))
    possible_paths.append(PuzzleState(move(node.state, 'Left'), node, 'Left', node.depth + 1, node.cost + 1, 0))
    possible_paths.append(PuzzleState(move(node.state, 'Right'), node, 'Right', node.depth + 1, node.cost + 1, 0))

    return list(filter(lambda path: path.state is not None, possible_paths))


# move
def move(state, direction):
    new_state = state[:]
    zero_index = new_state.index(0)
    if direction == 'Up':
        if zero_index not in [0, 1, 2]:
            new_state[zero_index], new_state[zero_index - 3] = new_state[zero_index - 3], new_state[zero_index]
            return new_state
    if direction == 'Down':
        if zero_index not in [6, 7, 8]:
            new_state[zero_index], new_state[zero_index + 3] = new_state[zero_index + 3], new_state[zero_index]
            return new_state
    if direction == 'Left':
        if zero_index not in [0, 3, 6]:
            new_state[zero_index], new_state[zero_index - 1] = new_state[zero_index - 1], new_state[zero_index]
            return new_state
    if direction == 'Right':
        if zero_index not in [2, 5, 8]:
            new_state[zero_index], new_state[zero_index + 1] = new_state[zero_index + 1], new_state[zero_index]
            return new_state
    return None


# DFS
def dfs(initial_state):
    global MaxFrontierSize, MaxSearchDepth, GoalNode
    board_visited = set()
    stack = list([PuzzleState(initial_state, None, None, 0, 0, 0)])
    while stack:
        node = stack.pop()
        board_visited.add(node.map)
        if node.state == GoalState:
            GoalNode = node
            return "Goal!"

        possible_paths = reversed(get_possible_paths(node))
        for path in possible_paths:
            if path.map not in board_visited:
                stack.append(path)
                board_visited.add(path.map)
                if path.depth > MaxSearchDepth:
                    MaxSearchDepth = path.depth
        if len(stack) > MaxFrontierSize:
            MaxFrontierSize = len(stack)
    return "No Solution"


# Because there are 9! states can be reached in 8-puzzle, and the numbers of branch from each node is more than 2, so
# the depth of the tree is smaller log2(9!) = 18.5, so the max depth of the tree is 19 (if we make a balance tree).
Limit = 20


def ids(initial_state):
    global Limit, MaxSearchDepth

    def dls(node, limit):
        global MaxFrontierSize, GoalNode
        if node.state == GoalState:
            GoalNode = node
            return "Goal!"

        if limit == 0:
            return "Cutoff"

        cutoff_occurred = False
        possible_paths = get_possible_paths(node)
        for path in possible_paths:
            _result = dls(path, limit - 1)
            if _result == "Cutoff":
                cutoff_occurred = True
            elif _result == "Goal!":
                return "Goal!"
        return "Cutoff" if cutoff_occurred else "No Solution"

    for depth in range(Limit):
        result = dls(PuzzleState(initial_state, None, None, 0, 0, 0), depth)
        if result != "Cutoff":
            MaxSearchDepth = depth
            return result


def puzzle():
    global GoalNode
    global GoalState
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', action="store", dest="method", help="Method to use", type=str,
                        choices=['bfs', 'dfs', 'ast', 'ids'])
    parser.add_argument('-i', action="store", dest="initial_state", help="Initial state of the board", type=int,
                        nargs=9)
    parser.add_argument('-g', action="store", dest="goal_state", help="Goal state of the board", type=int, nargs=9)

    args = parser.parse_args()

    initial_state = args.initial_state
    GoalState = args.goal_state
    function = args.method
    start_time = timeit.default_timer()
    if function == 'bfs':
        bfs(initial_state)
    elif function == 'dfs':
        dfs(initial_state)
    elif function == 'ids':
        ids(initial_state)
    else:
        GoalNode = PuzzleState(GoalState, None, None, 0, 0, 0)
    stop = timeit.default_timer()
    run_time = stop - start_time
    deep = GoalNode.depth
    moves = []
    while GoalNode.parent is not None:
        moves.insert(0, GoalNode.action)
        GoalNode = GoalNode.parent

    print("path_to_goal: {}".format(moves))
    print("cost_of_path: {}".format(len(moves)))
    print("nodes_expanded: {}".format(NodesExpanded))
    print("search_depth: {}".format(deep))
    print("max_search_depth: {}".format(MaxSearchDepth))
    print("running_time: {}".format(run_time))


