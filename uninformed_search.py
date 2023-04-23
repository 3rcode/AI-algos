# Exercise 1
import heapq
from collections import deque


class Graph:
    def __init__(self, adjacency_lst):
        self.adjacency_list = adjacency_lst

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def bfs(self, start_node, stop_node):
        queue = deque([start_node])
        parents = {start_node: start_node}
        visited = set()
        while queue:
            node = queue.popleft()
            if node == stop_node:
                path = [node]
                while parents[node] != node:
                    node = parents[node]
                    path.append(node)
                return path[::-1]
            visited.add(node)
            for neighbor, weight in self.get_neighbors(node):
                if neighbor not in visited:
                    if neighbor not in parents:
                        parents[neighbor] = node
                    queue.append(neighbor)
        return "No path found"

    def dfs(self, start_node, stop_node):
        stack = [start_node]
        parents = {start_node: start_node}
        visited = set()
        while stack:
            node = stack.pop()
            if node == stop_node:
                path = [node]
                while parents[node] != node:
                    node = parents[node]
                    path.append(node)
                return path[::-1]
            visited.add(node)
            for neighbor, weight in self.get_neighbors(node):
                if neighbor not in visited:
                    if neighbor not in parents:
                        parents[neighbor] = node
                    stack.append(neighbor)
        return "No path found"

    def ids(self, start_node, stop_node):
        limit = 10

        def dls(node, depth):
            if node == stop_node:
                return [node]
            if depth == limit:
                return None
            for neighbor, weight in self.get_neighbors(node):
                path = dls(neighbor, depth + 1)
                if path:
                    return [node] + path
            return None

        for i in range(limit):
            path = dls(start_node, i)
            if path:
                return path

    def ucs(self, start_node, stop_node):
        queue = [(0, start_node)]
        parents = {start_node: start_node}
        visited = set()
        while queue:
            cost, node = heapq.heappop(queue)

            if node == stop_node:
                path = [node]
                while parents[node] != node:
                    node = parents[node]
                    path.append(node)
                return path[::-1]
            visited.add(node)
            for neighbor, weight in self.get_neighbors(node):
                if neighbor not in visited:
                    if neighbor not in parents:
                        parents[neighbor] = node
                        heapq.heappush(queue, (cost + weight, neighbor))
                    else:
                        for q in queue:
                            if q[1] == neighbor and q[0] > cost + weight:
                                queue.remove(q)
                                parents[neighbor] = node
                                heapq.heappush(queue, (cost + weight, neighbor))
                                break

        return "No path found"


adjacency_list = {
    'S': [('A', 3), ('C', 2), ('D', 2)],
    'A': [],
    'C': [('F', 1)],
    'D': [('B', 3), ('G', 8)],
    'F': [('E', 0), ('G', 4)],
    'B': [('E', 2)],
    'E': [('G', 2)],
    'G': []
}

graph = Graph(adjacency_list)
print(graph.bfs('S', 'G'))
print(graph.dfs('S', 'G'))
print(graph.ids('S', 'G'))
print(graph.ucs('S', 'G'))
