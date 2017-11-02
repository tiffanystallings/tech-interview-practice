"""
Question 5:
Find the element in a singly linked list that's
m elements from the end. For example, if a linked
list has 5 elements, the 3rd element from the end
is the 3rd element. The function definition should
look like question5(ll, m), where ll is the first
node of a linked list and m is the "mth number
from the end". You should copy/paste the Node class
below to use as a representation of a node in the
linked list. Return the value of the node at that
position.

class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None

Inputs and outputs:
If the algorithm takes in a None type object, or a
linked list that has fewer elements than m, it will
return None. Otherwise, it will return the data from
the node it selects.

I plan on traversing the linked list first and
storing the values in an array, from which I will
return the -mth element in the array.

Since I only have to traverse the linked list once,
this will run at O(n) speed to traverse the list.

It will also require O(n) memory, as the size of the
array I'll be saving is the size of the linked list.
"""

class Node(object):
    def __init__ (self, data):
        self.data = data
        self.next = None

def question5(ll, m):
    """
    I'm going to store a list of all the values I come
    across.
    """
    elems = []
    current = ll

    """
    Handling one of my edge cases
    """
    if not ll:
        return None

    """
    I'm going to traverse the linked list until current
    becomes None, meaning the last element was the end
    of the linked list.
    """
    while current:
        elems.append(current.data)
        current = current.next

    """
    Handling my other edge case, where the length of the
    linked list is less than m.
    """
    if len(elems) < m:
        return None

    """
    I plan to make m negative, which won't work if m is 0.
    I also know that a singly linked list has no direct
    connection to its start, so I won't consider -m elements
    from the end to be m elements from the beginning. Instead,
    I'll just return the final element of the list in both of
    these cases.
    """
    if m <= 0:
        return elems[-1]

    """
    Otherwise, return the -mth index of elems.
    """
    return elems[-m]

"""
I'm going to create a helper function for creating
linked lists for my algorithm to traverse. It will
create a linked list n elements long. For the sake
of simplicity, I'll have it assign numbers in
ascending order as the data for each node.
"""
def create_list(n):
    head = Node(0)
    current = head
    for i in range(1, n):
        current.next = Node(i)
        current = current.next
    return head

ll1 = create_list(5)
ll2 = Node(6)
ll3 = None

print('Expecting "2":')
print(question5(ll1, 3))
print('Expecting "None":')
print(question5(ll2, 3))
print('Expecting "None":')
print(question5(ll3, 3))
