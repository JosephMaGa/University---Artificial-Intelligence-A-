from search import *
import math
import heapq

class MapGraph(Graph):

    def __init__(self, map_str):
        self.map_str = map_str
        self.weird_list = [('N' , -1, 0),
 ('NE', -1, 1),
 ('E' ,  0, 1),
 ('SE',  1, 1),
 ('S' ,  1, 0),
 ('SW',  1, -1),
 ('W' ,  0, -1),
 ('NW', -1, -1)]

        

    def is_goal(self, node):
        
        i, row, col = 0, 0, 0
    
        while i < len(self.map_str):
        
            if math.ceil(row) == node[0] and col == node[1]:
                if self.map_str[i] == 'G':
                    return True
                else:
                    return False

            elif self.map_str[i] == '|':
                row += 0.5
                col = 1
                i += 1
                continue
                    
            col += 1
            i+=1
    

    
    def find_goal(self):
              
        col, row, i = 0, 0, 0
        
        while i < len(self.map_str):

            if self.map_str[i] == '|':
                row += 0.5
                col = 1
                i += 1
                continue

            elif self.map_str[i] == 'G':
                return (math.ceil(row), col)
            
            col += 1
            i+=1
    
    
    def starting_nodes(self):
        col, row, i = 0, 0, 0
        starts = []
        while i < len(self.map_str):

            if self.map_str[i] == '|':
                row += 0.5
                col = 1
                i += 1
                continue

            elif self.map_str[i] == 'S':
                starts.append((math.ceil(row), col))
                
            col += 1
            i+=1
            
        return starts
            
    def outgoing_arcs(self, tail_node):
        """Given a node it returns a sequence of arcs (Arc objects)
        which correspond to the actions that can be taken in that
        state (node)."""

        nodes = self.map_str.split('\n')
        i = 0
        row, col = tail_node
        outgoing = []
        
        for line in nodes:
            line = line.replace("\t", "")
        
        for label, X, Y in self.weird_list:
            if col + Y > 0 and col + Y < len(nodes[0]) - 1:
                if row + X > 0 and row + X < len(nodes) - 1:
                    if nodes[row+X][col+Y] not in 'X+-|':
                        outgoing.append(Arc(tail_node, (row + X, col + Y), label=label ,cost=1))
                        
        return outgoing
    
    def estimated_cost_to_goal(self, node):
        
        goal = self.find_goal()
        return max(abs(goal[0]-node[0]), abs(goal[1]-node[1]))

class AStarFrontier(Frontier):

    def __init__(self, map_graph):
        
        self.map_graph = map_graph
        self.container = []
        self.checked_nodes = []
        self.tie_breaker = 0
        
    def add(self, path):

        if path[-1].head not in self.checked_nodes:
            heapq.heappush(self.container, (self.f_value_calculator(path),self.tie_breaker, path))
            self.tie_breaker += 1

    def __iter__(self):
        
        while self.container:
            
            next_path = heapq.heappop(self.container)[-1]
            if next_path[-1].head not in self.checked_nodes:
                self.checked_nodes.append(next_path[-1].head)
                yield next_path

    def f_value_calculator(self, path):
        
        cost = self.cost_calculator(path)
        heuristic = self.map_graph.estimated_cost_to_goal(path[-1].head)
        return cost + heuristic
    
    def cost_calculator(self, path):
        total_cost = 0
        for arc in path:
            total_cost += arc.cost
        return total_cost

class LCFSFrontier(Frontier):
    def __init__(self):
        self.container = []
        self.checked_nodes = []
        self.tie_breaker = 0
        
    def add(self, path):
        heapq.heappush(self.container, (sum(arc.cost for arc in path),self.tie_breaker, path))
        self.tie_breaker += 1
        
        
    def __iter__(self):
                
        while self.container:
            next_path = heapq.heappop(self.container)[-1]
            if next_path[-1].head not in self.checked_nodes:
                self.checked_nodes.append(next_path[-1].head)            
            yield next_path
 
def euclidean_dist(start, goal):
    
    if goal[0] == start[0]:
        e_dist = goal[1] - start[1]
    
    elif goal[1] == start[1]:
        e_dist = goal[0] - start[0]
            
    else:
        e_dist = math.ceil(((goal[0] - start[0])**2 + goal[1] -start[1]**2)**0.5)
    return e_dist
        
def chebyshev_dist(start, goal):
    return max(abs(goal[0]-start[0]), abs(goal[1]-start[1]))

def print_map(map_graph, frontier, solution):
    pathway = [] #asterisks
    checked_nodes = [] #periods
    if solution:
        for i in solution:
            pathway.append(i.head)

    if pathway:
        pathway.pop(-1)
    if pathway:
        pathway.pop(0)
    
    starts = map_graph.starting_nodes() 
    
    for i in frontier.checked_nodes:
        if not map_graph.is_goal(i):
            if i not in starts:
                checked_nodes.append(i)
            
    
        
    
    result = ''
    nodes = map_graph.map_str.split('\n')
    for line in nodes:
        line = line.replace("\t", "")
    row, col = 0, 0
    for line in nodes:
        new_line = []
        for character in line:
            if (row, col) in pathway:
                new_line.append('*')
            elif (row,col) not in pathway and (row, col) in checked_nodes:
                new_line.append('.')
            else:
                
                new_line.append(character)
            col+=1
        col = 0
        new_line = ''.join(new_line)
        print(new_line)
        new_line = ''
        row+=1

    

map_str = """\
+-------------+
|             |
|  X          |
|  X S        |
|  XXXXXX     |
| G           |
+-------------+
"""

map_graph = MapGraph(map_str)
frontier = LCFSFrontier()
solution = next(generic_search(map_graph, frontier), None)
print_map(map_graph, frontier, solution)