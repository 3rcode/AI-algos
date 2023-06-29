'''
Function General-Search(problem, Queuing-Fn) returns a solution, or failure
	nodes <- make-queue(make-node(initial-state[problem]))
	loop do
		if nodes is empty then return failure
		node <- Remove-Front(nodes)
		if Goal-Test[problem] applied to State(node) succeeds then return node
		nodes <- Queuing-Fn(nodes, Expand(node, Operators[problem])
	end
'''	
#-----------------------------------------------------------------------------------------------
'''
Function tree_search(problem) returns a solution, or failure

	initialize frontier as a specific work list(stack, queue, priority queue)
	add initial state of problem to frontier
	loop do
		if the frontier is empty then
			return failure
		choose a node and remove it from the frontier
		if the node contains a goal state then
			return the corresponding solution
		
		for each resulting child from node
			add child to the frontier
	end
'''
#-----------------------------------------------------------------------------------------------
'''
Function graph_search(problem) returns a solution, or failure
	initialize the explored set to be empty
	initialize the frontier as a specific work list(stack, queue, priority queue)
	add initial state of problem to frontier
	loop do
		if the frontier is empty then 
			return failure
		choose a node and remove it from the frontier
		if the node contains a goal state then
			return the corresponding solution
			
		add node to explored set
		for each resulting child from node
			if the child not in explored set and not in frontier
				add child to frontier
	end
'''
#-----------------------------------------------------------------------------------------------
'''
Uninformed/ Blind search strategies

Breadth-first search
Depth-first search
Depth-limited search
Iterative deepening depth first search
Uniform-cost search
'''
#-----------------------------------------------------------------------------------------------
'''
Function uniform-cost-search(problem) returns a solution, or failure
	initialize the explored set to be empty
	initialize the frontier as a priority queue using node-path-cost
	add initial state of problem to frontier with path-cost = 0
	loop do
		if the frotier is empty then
			return failure
		
		choose a node and remove it from the frontier 
		if the node contains goal state then
			return the corresponding solution
		
		add the node to explored set
		for each resulting child from node
			if the child not in explored set	then
				if the child not in frontier then
					add the child with path-cost = node path-cost + path-from-node-to-child
				else
					if child path-cost > node path-cost + path-from-node-to-child then
						replace that frontier node with child
	end
'''	
#-----------------------------------------------------------------------------------------------
'''
Informed search strategies

Greedy/Best-first-search = Breadth first search + heuristic function
Beam-search
Hill-climbing-search
A* search
'''
#-----------------------------------------------------------------------------------------------
'''
Function best-first-search(problem) returns a solution, or failure
	initialize the explored set to be empty
	initialize queue L contains only start node
	loop do
		if L is empty then
			return failure
		remove node from L head
		if node contains goal state then
			return corresponding solution
		add the node to explored set
		for each child expand from node
			if node not in explored set and not in L then 
				put child in list L so that L is sorted in best to worse order of the eval-func
	end
'''
#-----------------------------------------------------------------------------------------------
'''
Function beam-search(problem) returns a solution, or failure
	initialize the explored set to be empty
	initialize queue L contains only start node
	loop do
		if L is empty then 
			return failure
		initialize priority queue L1 to be empty with prior is eval-func
		loop do
			if L is empty then
				 end loop
			remove node from L head
			if node contains goal state then
				return corresponding solution
			add the node to explored set
			for each child expand from node
				if child not in explored set and not in L then 
					put child in L1
		end
		
		L = get min(len(L1), beam_width) node from head of priority queue L1
	end
'''
#-----------------------------------------------------------------------------------------------
'''
Function hill-climbing-search(problem) returns a solution, or failure
	initialize the explored set to be empty
	initialize queue L contains only start node
	loop do
		if L is empty then
			return failure
		remove node from L head
		if node contains goal state then
			return corresponding solution
		for each child expand from node
			if child not in explored set and not in L then
				put child into L1
		sort L1 in ascending order of eval-func so that the best node is at the top of the L1
		move L1 to the beginning of L so that the beginning of L1 becomes the beginning of L
	end
'''
#-----------------------------------------------------------------------------------------------
'''
Function A-star-search(problem) returns a solution, or failure
	initialize the explored set to be empty
	initialize queue L contains only start node
	loop do
		if L is empty then
			return failure
		remove node from L head
		if node contains goal state then
			return corresponding solution
		for each child expand from node do
			g(child) = g(node) + path-cost-from-node-to-child
			f(child) = g(child) + h(child)
			put child into the queue L so that L is sorted in best to worst order of eval-func
	end

Example:
'''
from collections import deque

class Graph:
    # example of adjacency list (or rather map)
    # adjacency_list = {
    # 'A': [('B', 1), ('C', 3), ('D', 7)],
    # 'B': [('D', 5)],
    # 'C': [('D', 12)]
    # }

    def __init__(self, adjacency_list, heu_func):
        self.adjacency_list = adjacency_list
        self.heu_func = heu_func

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    # heuristic function with equal values for all nodes
    def h(self, n):
    #    H = {
    #        'A': 1,
    #        'B': 1,
    #        'C': 1,
    #        'D': 1
    #   }

        return self.heu_func[n]

    def a_star_algorithm(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v;

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                reconst_path = []
                print('Cost: {}'.format(g[n]))

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()
                

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for (m, weight) in self.get_neighbors(n):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None
adjacency_list = {
    'A': [('S', 1), ('B', 9)],
    'B': [('A', 9), ('S', 1), ('C', 6), ('G', 12)],
    'C': [('B', 6), ('G', 5)], 
    'S': [('A', 1), ('B', 1)],
    'G': [('C', 5), ('B', 12)]
}
heur_function = {
    'A': 10,
    'B': 9,
    'C': 5,
    'S': 7, 
    'G': 0
}

graph1 = Graph(adjacency_list,heur_function)
graph1.a_star_algorithm('A', 'G')
	

		
		
 
