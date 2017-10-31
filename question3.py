"""
Question 3:
Given an undirected graph G, find the minimum
spanning tree within G. A minimum spanning tree
connects all vertices in a graph with the
smallest possible total weight of edges. Your
function should take in and return an adjacency
list structured like this:
{'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)], 
 'C': [('B', 5)]}

This reminds me of the travelling salesman
problem, which means finding an efficient answer
could be tricky.

Edge cases:
A graph with no edges will return None. ie:
{'A': [],
 'B': [],
 'C': []...

 >>> None

Empty adjacency lists will return None.

I'll also be testing with the following graph from
the wikipedia article on minimum spanning trees.
{'A': [('B', 4), ('C', 3), ('D', 10), ('E', 18)],
 'B': [('A', 4), ('C', 1), ('F', 4)],
 'C': [('A', 3), ('B', 1), ('F', 5), ('D', 9)],
 'D': [('A', 10), ('C', 9), ('E', 8), ('F', 7), ('G', 8), ('H', 9)],
 'E': [('A', 18), ('D', 8), ('H', 9), ('I', 9)],
 'F': [('B', 4), ('C', 5), ('D', 7), ('G', 9), ('J', 9)],
 'G': [('D', 8), ('F', 9), ('H', 2), ('J', 2)],
 'H': [('D', 9), ('E', 9), ('G', 2), ('I', 3), ('J', 4)],
 'I': [('E', 9), ('H', 3), ('J', 6)],
 'J': [('F', 9), ('G', 2), ('H', 4), ('I', 6)]}

 I decided to conduct a breadth-first search to find a path from the
 first node to the last. To keep track of lineage, I alter the
 dictionary to include parents and children. The breadth-first search
 runs at about O(n), as it needs to check all nodes and edges once.

 In order to find the shortest tree, I need to check this algorithm
 using each node of G. I'll simplify this to say that running the
 breadth-first search will happen about O(n) times.

 Overall, the runtime of this algorithm is about O(n^2).

 While it doesn't find the exact best answer, it gets pretty close.
 In the case of the example from wikipedia, it's over by about 4.
 """

"""
Deque has a great efficiency for managing queues, so I chose to
use it for this problem.
"""
from collections import deque
def question3(G):
    """
    I wanted a helper for my breadth-first search, so I can run
    it on each node of my graph.
    """
    def breadth_search(active, d, head, checked):
        """
        To find the shortest edge(s), I use an array to hold the
        last best result. I don't want to go over any edges I have
        already looked at, so I check them against another array.
        I also make sure that I didn't just find the parent edge
        again.
        """
        best = []
        for edge in active[head]['edges']:
            if edge[0] not in checked and edge != active[head]['parent']:
                if not best:
                    best.append(edge)
                elif edge[1] < best[0][1]:
                    best = []
                    best.append(edge)
                elif edge[1] == best[0][1]:
                    best.append(edge)
        """
        I add my head element as the parent of the best children
        and save the best children to my head element. I also add
        the best elements to my deque so I can check them next.
        """
        for e in best:
            d.append(e[0])
            active[e[0]]['parent'] = (head, e[1])
        active[head]['children'] = best

    """
    I wanted another function for building my spanning trees. This
    will allow me to make trees with all possible different bases.
    """
    def create_tree(G, base):
        result = {}
        active = {}
        checked = []
        total = 0
        d = deque(base)

        """
        I opted to use extra memory here for the sake of efficiency.
        I knew if I altered the initial input my parents and children
        would remain from previous trees. So I created a copy that I
        can alter seperately. I also used this loop to create an empty
        adjacency list.
        """
        for key in G:
            result[key] = []
            active[key] = G[key]

        """
        While I have elements in my deque, I need to perform my breadth-
        first search on them.
        """
        while d:
            head = d.popleft()
            breadth_search(active, d, head, checked)
            checked.append(head)

        """
        Once all parents and children are found, I'll build my
        adjacency list.
        """
        for key in result:
            if active[key]['parent']:
                total += active[key]['parent'][1]
                result[key].append(active[key]['parent'])
            if active[key]['children']:
                result[key].extend(active[key]['children'])

        """
        As it's possible for my tree to hit a dead-end without
        seeing all elements, I will check for that and return
        None if it happens.
        """
        if len(checked) < len(active):
            return None, None

        return result, total

    """
    If my adjacency list is empty, return None.
    """
    if not G:
        return None
    
    best_result = None
    best_total = None

    """
    I wanted to restructure my input to make more sense of
    the information I was collecting.
    """
    for key in G:
        G[key] = {'edges': G[key],
                  'parent': None,
                  'children': []}
        
    """
    For every node, I build a spanning tree with that node
    as its base. I hold the returned values in a variable
    so I can check each subsequent tree weight against the
    last best option. Once I've checked all trees, I return
    the best.
    """
    for key in G:
        result, total = create_tree(G, key)
        if result and total:
            if not best_result:
                best_result = result
                best_total = total
            elif best_total > total:
                best_result = result
                best_total = total

    return best_result

test1 = {
     'A': [('B', 4), ('C', 3), ('D', 10), ('E', 18)],
     'B': [('A', 4), ('C', 1), ('F', 4)],
     'C': [('A', 3), ('B', 1), ('F', 5), ('D', 9)],
     'D': [('A', 10), ('C', 9), ('E', 8), ('F', 7), ('G', 8), ('H', 9)],
     'E': [('A', 18), ('D', 8), ('H', 9), ('I', 9)],
     'F': [('B', 4), ('C', 5), ('D', 7), ('G', 9), ('J', 9)],
     'G': [('D', 8), ('F', 9), ('H', 2), ('J', 2)],
     'H': [('D', 9), ('E', 9), ('G', 2), ('I', 3), ('J', 4)],
     'I': [('E', 9), ('H', 3), ('J', 6)],
     'J': [('F', 9), ('G', 2), ('H', 4), ('I', 6)]
}

expected1 = {
    'A': [('C', 3)],
    'B': [('C', 1), ('F', 4)],
    'C': [('A', 3), ('B', 1)],
    'D': [('F', 7), ('E', 8), ('G', 8)],
    'E': [('D', 8)],
    'F': [('B', 4), ('D', 7)],
    'G': [('D', 8), ('H', 2), ('J', 2)],
    'H': [('G', 2), ('I', 3)],
    'I': [('H', 3)],
    'J': [('G', 2)]
}

test2 = {}

test3 = {'a': [], 'b': [], 'c': []}

print ('Best possible answer for Test 1:')
print (expected1)
print ('My algorithm returns:')
print (question3(test1))

print ('Best possible answer for Test 2')
print (None)
print ('My algorithm returns:')
print (question3(test2))

print ('Best possible answer for Test 3:')
print (None)
print ('My algorithm returns:')
print (question3(test3))




    
