import math


class Node:

    # Initialize the class
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    # Compare nodes
    def __eq__(self, other):
        return self.node == other.node


def astar(graph, start, end, heuristic={}):
    """Performs A-star search to find the shortest path from start to end

        Args:
            graph(dict): Dictionary representing the graph,
                    where keys are the nodes and the
                    value is a list of all neighbouring nodes
            start(tuple): Tuple representing key corresponding to the start point
            end(tuple): Tuple representing key corresponding to the end point
            heuristic(dict): Dictionary containing the heuristic values
                     for all the nodes, if not specified the default
                     heuristic is euclidean distance
        Returns:
            path(list):A list of points representing the path determined from
                    start to goal.An list containing just the start point means
                     path could not be planned.
    """
    if not (start in graph and end in graph):
        path = [start]
        return path
    open_ = []
    closed = []
    # calcula]tes heuristic for start if not provided by the user
    # pushes the start point in the open_ Priority Queue

    start_node = Node(start, None)
    if len(heuristic) == 0:
        start_node.h = math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)
    else:
        start_node.h = heuristic[start]
    start_node.g = 0
    start_node.f = start_node.g + start_node.h
    open_.append(start_node)
    # performs astar search to find the shortest path
    while len(open_) > 0:
        open_.sort()
        current_node = open_.pop(0)
        closed.append(current_node)
        # checks if the goal has been reached
        if current_node.node == end:
            path = []
            # forms path from closed list
            while current_node.parent is not None:
                for node in closed:
                    if node.node == current_node.parent:
                        path.append(current_node.node)
                        current_node = node
                        break
            path.append(start)
            # returns reversed path
            return path[::-1]
        # continues to search for the goal
        # makes a list of all neighbours of the current_node
        neighbours = graph[current_node.node]
        # adds them to open_ if they are already present in open_
        # checks and updates the total cost for all the neighbours
        for node in neighbours:
            # creates neighbour which can be pushed to open_ if required
            neighbour = Node(node, current_node.node)
            # checks if neighbour is in closed
            if neighbour in closed:
                continue
            # calculates weight cost
            neighbour.g = (
                math.sqrt(
                    (node[0] - current_node.node[0]) ** 2
                    + (node[1] - current_node.node[1]) ** 2
                )
                + current_node.g
            )
            # calculates heuristic for the node if not provided by the user
            if len(heuristic) == 0:
                neighbour.h = math.sqrt(
                    (node[0] - end[0]) ** 2 + (node[1] - end[1]) ** 2
                )
            else:
                neighbour.h = heuristic[node]
            # calculates total cost
            neighbour.f = neighbour.g + neighbour.h
            # checks if the total cost of neighbour needs to be updated
            # if it is presnt in open_ else adds it to open_
            flag = 1
            for new_node in open_:
                if neighbour == new_node and neighbour.f < new_node.f:
                    new_node = neighbour
                    flag = 0
                    break
                elif neighbour == new_node and neighbour.f > new_node.f:
                    flag = 0
                    break
            if flag == 1:
                open_.append(neighbour)
    # if path doesn't exsist it returns just the start point as the path
    path = [start]
    return path
