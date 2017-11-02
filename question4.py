"""
Question 4:
Find the least common ancestor between two nodes on
a binary search tree. The least common ancestor is
the farthest node from the root that is an ancestor
of both nodes. For example, the root is a common
ancestor of all nodes on the tree, but if both nodes
are descendents of the root's left child, then that
left child might be the lowest common ancestor. You
can assume that both nodes are in the tree, and the
tree itself adheres to all BST properties. The function
definition should look like question4(T, r, n1, n2),
where T is the tree represented as a matrix, where
the index of the list is equal to the integer stored
in that node and a 1 represents a child node, r is a
non-negative integer representing the root, and n1
and n2 are non-negative integers representing the two
nodes in no particular order. For example, one test
case might be:

question4([[0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [1, 0, 0, 0, 1],
           [0, 0, 0, 0, 0]],
          3,
          1,
          4)
and the answer would be 3.

Outputs:
If the function is provided an empty matrix, I'll
output None. Otherwise, I'll output an integer.

Since I can assume the BST follows normal rules and the
inputs will be represented in the tree, the only other
edge case I will test for is a very large BST.

As this is a binary search tree, it should be fairly
simple for me to conduct a binary search to locate
my elements. As I traverse the tree for the first
element, I plan on keeping a log of the path taken.
I can traverse that path again and see where it
breaks with the path to the second element.

I know that a basic binary search algorithm will
run at O(log n), so I know that mine will be about
the same on a best case. Average case will run at
O(√n), because I'll be iterating over about 1/2 of
√n elements for a depth of log n and repeating
the path up to log n times.

The memory efficiency will also be about O(log n), as
I will be saving the path I take as I traverse the
tree, and I know that traversing a binary search tree
happens in log n time.
"""

def question4(T, r, n1, n2):
    """
    I created a seperate binary search function
    that I can run recursively.
    """
    def binary_search(num, root, T):
        """
        I'll add every root element to the path so
        I can iterate over it for the next number. I
        utilize the BST structure here to split the
        array at root between indices lower than the
        root number and indices higher than the root
        number, allowing me to iterate through more
        efficiently.
        """
        path.append(root)
        if num == root:
            return root
        elif num < root:
            current = T[root][:root]
            for i in range(len(current)):
                if current[i] == 1:
                    return binary_search(num, i, T)
        elif num > root:
            current = T[root][root+1:]
            for i in range(len(current)):
                if current[i] == 1:
                    return binary_search(num, root+1+i, T)
    """
    Handling my empty matrix edge case.
    """
    if not T:
        return None
    
    path = []
    binary_search(n1, r, T)

    """
    I check each element in the path against the next,
    to see if it follows the same rules as a binary
    search for n2 would follow. Once I get to a point
    in the path where n2 doesn't follow the same rules,
    I return that point.
    """
    for i in range(len(path)-1):
        if path[i] < path[i+1] and n2 < path[i]:
            return path[i]
        elif path[i] > path[i+1] and n2 > path[i]:
            return path[i]
        elif path[i] == n2:
            return path[i]

    """
    If an ancestor hasn't returned by now, the last
    element of the path is the last common ancestor.
    """
    return path[-1]

test1 = [[0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [1, 0, 0, 0, 1],
         [0, 0, 0, 0, 0]]

print (question4(test1, 3, 1, 4))

test2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

print (question4(test2, 10, 16, 15))

print (question4([], None, None, None))
