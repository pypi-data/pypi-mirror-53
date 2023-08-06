from collections import deque

infinity = float('inf')

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action 
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self): # to print node objects
        return "<Node "+ self.state + ">"

    def expand(self, problem): # to extract children
        children = []
        for action in problem.actions(self.state):
            x=self.child_node(problem,action)
            children.append(x)
        return children
        
    def child_node(self, problem, action): # to make node object of each child
        next_state = problem.result(self.state, action)
        new_cost = problem.path_cost(self.path_cost, self.state,action, next_state)
        print("Current State = ", self.state, ",New Child = ", next_state)
        next_node = Node(next_state, self, action,new_cost )      
        return next_node
    
    def solution(self): # extracts the path of solution
        return [node.state for node in self.path()]

    def path(self): # extracts the path of any node starting from current to source
        node, path_back = self, []
        while node: 
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back)) # order changed to show from source to current


class Problem(object): # same as given in theory
    def __init__(self, initial, goal=None):
       self.initial = initial
       self.goal = goal

    def actions(self, state):
         raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError


class GraphProblem(Problem): # subclass of problem, few functions overriden
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def actions(self, A):
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or infinity)

      
class Graph: # to represent graph 
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def get(self, a, b=None):
        links = self.graph_dict.get(a) 
        if b is None:
            return links
        else:
            cost = links.get(b)
            return cost

    def nodes(self):        
        nodelist = list()              
        for key in self.graph_dict.keys() :
            nodelist.append(key)
        return nodelist
    

def depthLimitedSearch(problem, limit): #returns a solution, or "failure"/"cutoff"
    return recursiveDLS(Node(problem.initial), problem, limit)

def recursiveDLS(node, problem, limit): #returns a solution, or "failure"/"cutoff"
    if problem.goal_test(node.state):
        return node.solution()
    elif limit == 0:
        return "cutoff"
    else:
        cutoff_occurred = False
        for action in problem.actions(node.state):
            child = node.child_node(problem, action)
            result = recursiveDLS(child, problem, limit - 1)
            if result == "cutoff":
                cutoff_occurred = True
            elif result != "failure":
                return result
        if cutoff_occurred:
            return "cutoff"
        else:
            return "failure"

def iterativeDepthSearch(problem): #returns a solution, or failure
    for depth in range(0, 4):
        result = depthLimitedSearch(problem, depth)
        print("Result for depth " + str(depth) + " is " + str(result))

#we are giving full description of graph through dictionary.  the Graph class is not building any additional links

mumbaigraph=Graph({
    'kurla':{'sion':5,'chembur':6, 'thane':9},
    'chembur':{'kurla': 6, 'vashi':2},
    'vashi':{'chembur':2},
    'sion':{'kurla':5},
    'thane':{'kurla':9}
    })

mumbaigraph_problem = GraphProblem('thane','vashi', mumbaigraph)
#print("Keys of kurla ", mumbaigraph_problem.actions( 'thane'))
solution = iterativeDepthSearch(mumbaigraph_problem)
#print("solution of ", mumbaigraph_problem.initial, " to ", mumbaigraph_problem.goal, solution)
