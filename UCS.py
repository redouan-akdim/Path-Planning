from graph import Graph
from queue import PriorityQueue

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


def uniformCostSearch(initialState:str,goalState:str):
    if (initialState == goalState): return [initialState]   # Finished, if initialstate is goalstate
    
    myQueue = PriorityQueue()   # Frontier as Priority Queue
    visited = []    # Visited nodes
    
    for node in romania.nodes:
        if node.name == initialState:   # Find the start node in the graph
            node.value = 0      # Value of root node is 0
            node.parent = -1    # Declare node as root node
            myQueue.put((node.value,node))    # enqueue the initialstate to the queue
            break


    # Expand the nodes from frontier
    while not myQueue.empty():    
        node = myQueue.get()[1]    # Dequeue node from Queue (frontier)

        if node.name == goalState:      # Check if goalstate is reached
            visited.append(node)
            break

        if node in visited:     # Skip the node if it has already been visited
            continue

        for edge in node.edges:     # Traverse all edges from the node
            otherNode = edge.end     # Other node of the edge

            # Check that node isn't visited or in frontier and isn't the node himself
            if otherNode not in visited and otherNode not in [tup[1] for tup in myQueue.queue]:
                otherNode.parent = node     # Specify the parent node
                otherNode.value = otherNode.parent.value + edge.value   # 
                myQueue.put((otherNode.value,otherNode))   # Enqueue child node to frontier

            # If node is in frontier, replace nodes...
            elif otherNode not in visited and otherNode != node and otherNode in myQueue.queue:
                i = 0   # counter variable to set the index
                for _,node in myQueue.queue:
                    if otherNode == node and otherNode.value < node.value:      #...if the actaul node has lower path-cost
                        myQueue.queue[i] = otherNode
                    i += 1
            
        visited.append(node)        # Mark node as vistied

    return visited
             
def printPath(visited_list:list): 
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
printPath(uniformCostSearch('Bu','Ti'))