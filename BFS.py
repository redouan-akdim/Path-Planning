from graph import Graph,Node
from queue import Queue

romania = Graph( ['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
 'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
 'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
[
   ('Or', 'Ze', 71), ('Or', 'Si', 151),
   ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
   ('Ia', 'Va', 92), ('Ar', 'Si', 140),
   ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
   ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
   ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
   ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
   ('Lu', 'Me', 70), ('Me', 'Dr', 75),
   ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
   ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
   ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
   ('Hi', 'Ef', 86)
] )


def breadthFirstSearch(initialState:str,goalState:str):
    if (initialState == goalState): return [initialState]   # Finished, if initialstate is goalstate
    
    myQueue = Queue()   # Frontier as FIFO Queue
    for node in romania.nodes:
        if node.name == initialState:   # Find the start node in the graph
            node.parent = -1    # Declare node as root node
            myQueue.put(node)    # enqueue the initialstate to the queue
            break

    visited = []    # Visited nodes

    # Expand the nodes from frontier
    while not myQueue.empty():    
        node = myQueue.get()    # Dequeue node from Queue (frontier)
        if node in visited:
            continue

        if node.name == goalState:      # Check if goalstate is reached
            visited.append(node)
            break

        for edge in node.edges:     # Traverse all edges going from the node
            if edge.start not in visited and edge.start != node:      # Check that node isn't visited and isn't the node himself
                edge.start.parent = node
                myQueue.put(edge.start)  # Enqueue child node to frontier

            elif edge.end not in visited and edge.end != node:        # Check that node isn't visited and isn't the node himself
                edge.end.parent = node
                myQueue.put(edge.end)   # Enqueue child node to frontier
            
            
        
        visited.append(node)        # Mark node as vistied

    return visited
             
def printBFSPath(visited_list:list): 
    """Prints the path and its costs from the given 'visited' list"""
    pathCost = 0
    node = visited_list[-1]     # Begin from last node
    path = [node.name]

    while node.parent != -1:    # Traverse nodes until root node
        for edge in node.edges:     # Traverse all edges going from the node
            if node.parent == edge.start or node.parent == edge.end:    # Find edge to parent node
                pathCost += edge.value      # Sum the costs of the path
                break
        
        path.append(node.parent.name)   # Append parent node to the path
        node = node.parent      # -> Next node
    
    # Print path and its costs
    print(list(reversed(path)))
    print('Path cost:',pathCost)

# Travelling from Bucharest to Timisoara
printBFSPath(breadthFirstSearch('Bu','Ti'))