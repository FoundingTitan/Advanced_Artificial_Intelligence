import sys
from collections import deque

from utils import *
import random


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


# ______________________________________________________________________________

# ______________________________________________________________________________
# Informed (Heuristic) Search


greedy_best_first_graph_search = best_first_graph_search


# Greedy best-first search is accomplished by specifying f(n) = h(n).
def greedy_search(problem, h=None, display=False):
    
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: h(n), display)


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)


# ______________________________________________________________________________
# A* heuristics 

class BubblePuzzle(Problem):

    def __init__(self, initial, goal=None):
        self.initial = self.lists_to_tuples(initial)

    #Make the state hasable, so that it can be added to explored set
    def lists_to_tuples(self, state):
        for i in range(len(state)):
            state[i] = tuple(state[i])
        return tuple(state)

    #Retrive the state as list of lists from tuples
    def tuples_to_lists(self, state):
        state = list(state)
        for i in range(len(state)):
            state[i] = list(state[i])
        return state

    def actions(self, state):
        state = self.tuples_to_lists(state)
        total_tubes = len(state)
        all_actions = []
        for i in range(total_tubes):
            for j in range(total_tubes):
                if len(state[i]) > 0 and i != j: #tube has balls
                    if len(state[j]) == 0:
                        all_actions.append([i,j])
                    elif state[i][-1] == state[j][-1]:
                        all_actions.append([i,j])
        return all_actions

    def result(self, state, action):
        state = self.tuples_to_lists(state)
        tube_to_remove = action[0]
        tube_to_add = action[1]

        ball_removed = state[tube_to_remove].pop()

        #Add removed ball to the new tube
        state[tube_to_add].append(ball_removed)
        
        return self.lists_to_tuples(state)

    def num_of_colors(self, tube):
        unique_colors = list(set(tube))
        return len(unique_colors)

    def goal_test(self, state):
        state = self.tuples_to_lists(state)
        #If each tube is either empty or have same colors - its a goal state
        sorted_balls = []
        for tube in state:
            if len(tube) == 0:
                continue
            if self.num_of_colors(tube) == 1:
                ball_color = tube[0]
                if ball_color in sorted_balls:
                    return False
                else:
                    sorted_balls.append(ball_color)
            else:
                return False
        return True

    # Weaker Heuristic - Counts the number of unique color in a tube.
    def h(self, node):
        dist = 0

        for tube in node.state:
            unique_colors = list(set(tube))
            if len(unique_colors) > 1:
                dist += len(unique_colors) - 1

        return dist

    # Stronger Heuristic - Counts the number of balls inconsistent with ball color at the base.
    def h_better(self, node):
        dist = 0

        for tube in node.state:
            extra_balls = 0
            if len(tube) > 0:
                base_ball_color = tube[0]
                check_base = True
                for i in range(1,len(tube)):
                    if check_base and tube[i] == base_ball_color:
                        continue
                    else:
                        check_base = False
                        extra_balls += 1

            dist += extra_balls

        return dist


class EightPuzzle(Problem):
    """ The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
    squares is a blank. A state is represented as a tuple of length 9, where  element at
    index i represents the tile number  at index i (0 if it's an empty square) """

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        """Return the index of the blank square in a given state"""

        return state.index(0)

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square % 3 == 0:
            possible_actions.remove('LEFT')
        if index_blank_square < 3:
            possible_actions.remove('UP')
        if index_blank_square % 3 == 2:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """

        return state == self.goal

    def check_solvability(self, state):
        """ Checks if the given state is solvable """

        inversion = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                    inversion += 1

        return inversion % 2 == 0

    def h_MT(self, node):
        """ Return the heuristic value for a given state. Default heuristic function used is 
        h(n) = number of misplaced tiles """

        return sum(s != g for (s, g) in zip(node.state, self.goal))

    def h_Man(self, node):
        """ Return the heuristic value for a given state. Manhattan distance heuristic"""

        # The Manhattan Distance between two points (X1, Y1) and (X2, Y2) is given by |X1 – X2| + |Y1 – Y2|.
        # 9 points in the grid (in the same order as the node.state list)
        grid_points = [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)]

        man_dist = 0
        for i in range(len(self.goal)):
            if self.goal[i] != 0: #Done compute for the 0/empty position
                goal_grid_point = grid_points[i]
                node_state_position = list(node.state).index(self.goal[i])
                node_grid_point = grid_points[node_state_position]
     
                man_dist += abs(goal_grid_point[0] - node_grid_point[0]) + abs(goal_grid_point[1] - node_grid_point[1])
        return man_dist

# The heuristic below is admissable and inconsistent, in that it returns the optimal path AND number of opened-
# nodes are not consistent every time we run the code on any given problem state.
# All of the states given in the assignment were tested using this heuristic - as proof.
    def h_inconsistent(self, node):
        if random.uniform(0, 1) > 0.5:
            return self.h_Man(node)
        else:
            return self.h_MT(node)


greedy_search(EightPuzzle((1,2,3,4,0,6,7,5,8)), display=True)