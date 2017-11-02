def question1(s,t):
    if len(s) < len(t):
        return False
    if not t:
        return True
    if not s:
        return False

    """
    For every failed anagram search,
    I'll need to reset the dictionary.
    """
    anagram = {}
    def reset(anagram):
        anagram.clear()
        for i in range(len(t)):
            if anagram.get(t[i]):
                anagram[t[i]].append(1)
            else:
                anagram[t[i]] = [1]

    reset(anagram)

    """
    A helper function to check substrings
    against the dictionary.
    """
    def find_anagram(ss, anagram):
        for i in range(len(ss)):
            if anagram.get(ss[i]):
                anagram[ss[i]].pop()
            else:
                reset(anagram)
                return False
        return True

    """
    Iterating through substrings of s
    to check them for anagrams of t.
    """
    for i in range(len(s)-len(t)+1):
        if anagram.get(s[i]):
            anagram[s[i]].pop()
            if find_anagram(s[i+1:i+len(t)], anagram):
                return True
    return False


def question2(a):
    def format_string(s):
        formatted = ''
        for i in s:
            if i.isalnum():
                formatted += i
        return formatted.lower()

    def check_reverse(s):
        if s == s[::-1]:
            return True
        else:
            return False

    """
    I'm going to map all of the characters in my string
    and log the index at which they occur. These are
    going to act as "nodes".
    """
    def char_map(s):
        m = {}
        for i in range(len(s)):
            if m.get(s[i]):
                m[s[i]].append(i)
            else:
                m[s[i]] = [i]
        return m

    """
    I will draw edges between all of my nodes listed
    under the same character and add them to a list.
    """
    def get_edges(l):
        edges = []
        l.sort()
        for i in range(len(l)):
            for j in l[i+1:]:
                edge = (l[i], j)
                edges.append(edge)
        return edges

    a = format_string(a)
    if len(a)<= 1:
        return a
    if check_reverse(a):
        return a
    
    m = char_map(a)
    edges = []
    longest = ''

    """
    Find characters with more than one node and
    map their edges. Clear nodes at that key to prevent
    redundancy.
    """
    for c in a:
        if len(m[c]) > 1:
            edges += get_edges(m[c])
            m[c] = []

    """
    Get substrings from the indices of each edge, check if
    they are palindromes and if they are longer than the
    last recorded longest palindrome.
    """
    for e in edges:
        x = e[0]
        y = e[1]+1
        ss = a[x:y]
        if len(ss) > len(longest) and check_reverse(ss):
            longest = ss

    if longest:
        return longest
    else:
        return a[0]


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


print('Question 1 Tests:')
print('Expecting True')
print(question1('udacity', 'ad'))
# >>> True
print('Expecting True')
print(question1('citcity', 'city'))
# >>> True
print('Expecting False')
print(question1('udacity', 'adda'))
# >>> False
print('Expecting True')
print(question1('', ''))
# >>> True
print('Expecting False')
print(question1('', 'word'))
# >>> False
print('')

print('Question 2 Tests:')
print ('Expecting ""')
print (question2(''))
# >>> ''
print ('Expecting "a"')
print (question2('a'))
# >>> a
print ('Expecting "a"')
print (question2('abcd'))
# >>> a
print ('Expecting "amanaplanacanalpanama"')
print (question2('A man, a plan, a canal: Panama.'))
# >>> amanaplanacanalpanama
print ('Expecting "racecar"')
print (question2('The racecar is mine'))
# >>> racecar
print('')

print('Question 3 Tests:')
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
# >>> {'J': [('G', 2), ('F', 9)], 'A': [('C', 3), ('D', 10)],
# 'E': [('D', 8)], 'G': [('H', 2), ('J', 2)], 'C': [('B', 1),
# ('A', 3)], 'I': [('H', 3)], 'D': [('A', 10), ('E', 8)],
# 'B': [('F', 4), ('C', 1)], 'F': [('J', 9), ('B', 4)],
# 'H': [('I', 3), ('G', 2)]}
print ('Best possible answer for Test 2:')
print (None)
print ('My algorithm returns:')
print (question3(test2))
# >>> None
print ('Best possible answer for Test 3:')
print (None)
print ('My algorithm returns:')
print (question3(test3))
# >>> None
print('')

print('Question 4 Tests:')
test1 = [[0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [1, 0, 0, 0, 1],
         [0, 0, 0, 0, 0]]
print ('Expecting 3')
print (question4(test1, 3, 1, 4))
# >>> 3
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
print ('Expecting 15')
print (question4(test2, 10, 16, 15))
# >>> 15
print ('Expecting None')
print (question4([], None, None, None))
# >>> None
print('')

print('Question 5 Tests:')
ll1 = create_list(5)
ll2 = Node(6)
ll3 = None

print('Expecting "2"')
print(question5(ll1, 3))
# >>> 2
print('Expecting "None"')
print(question5(ll2, 3))
# >>> None
print('Expecting "None"')
print(question5(ll3, 3))
# >>> None
print('')
