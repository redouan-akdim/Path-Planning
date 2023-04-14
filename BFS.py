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

# Travelling from Bucharest to Timisoara
def breadthFirstSearch(initialState:str,goalState:str):
    if (initialState == goalState): return [initialState]   # Finished, if initialstate is goalstate
    
    myQueue = Queue()   # Frontier as FIFO Queue
    for node in romania.nodes:
        if node.name == initialState:
            node.parent = -1    # Declare node as root node
            myQueue.put(node)    # enqueue the initialstate to the queue
            break

    #node = Node(initialState)
    visited = []    # Visited nodes

    # Expand the nodes from frontier
    while not myQueue.empty():    
        #print("Test")  
        node = myQueue.get()    # Dequeue node from Queue (frontier)
        if node in visited:
            continue

        if node.name == goalState:      # Check if goalstate is reached
            visited.append(node)
            break

        for edge in node.edges:
            #if actualNode == node.state:   
            if edge.end not in visited and edge.end.name != node.name:#any(n.name != edge.end.name for n in visited):      # if next node isn't visited
                edge.end.parent = node
                myQueue.put(edge.end)   # Add child nodes
            
            if edge.start not in visited and edge.start.name != node.name:
                edge.start.parent = node
                myQueue.put(edge.start)
        
        visited.append(node)        # Mark node as vistied

    return visited
                
def printBFSPath(visited_list:list): 
    node = visited_list[-1]
    path = [node.name]
    while node.parent != -1:
        #print(node.name)
        path.append(node.parent.name)
        node = node.parent
    
    print(list(reversed(path)))


printBFSPath(breadthFirstSearch('Bu','Ti'))
#romania.print()