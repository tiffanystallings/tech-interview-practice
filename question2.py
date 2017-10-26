"""
Question 2:
Given a string a, find the longest palindromic
substring contained in a. Your function definition
should look like question2(a), and return a string.

Edge Cases:
An empty string will return itself, as will a string
with only one character.
A string with no palindromes will return the first
character, as a single letter is technically a palindrome.

I plan on eliminating spaces and special characters
in order to account for longer, more complex palindromic
phrases like "A man, a plan, a canal: Panama."

Once I've formatted my string, I plan to map the index of
each character in order to check reoccurances of that
character. I'll use that map to create "edges" between
two matching characters. I'll then check the substrings
along those edges for an anagram.

Average operation time seems to be about O(1/2 n^2), with
most of the operations occurring in the process of pairing
nodes.
Memory is also about O(1/2 n^2), most of which is the list
of edges.
"""

def question2(a):
    """
    I'm creating a helper function to seperate the
    string formatting.
    """
    def format_string(s):
        formatted = ''
        for i in s:
            if i.isalnum():
                formatted += i
        return formatted.lower()

    """
    This helper function is to test if a substring
    is the same as its reverse.
    """
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
    These will act as indices for a substring split.
    """
    def get_edges(l):
        edges = []
        l.sort()
        for i in range(len(l)):
            for j in l[i+1:]:
                edge = (l[i], j)
                edges.append(edge)
        return edges
        
    """
    Return empty or single character strings as
    already palindromes themselves. Also return
    any inputs that are already palindromes.
    """
    if len(a)<= 1:
        return a

    if check_reverse(a):
        return a
    
    a = format_string(a)
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

    """
    If a longest palindrome was found, return it. Else,
    return the first letter of the string as single letters
    can be palindromes.
    """
    if longest:
        return longest
    else:
        return a[0]

print ('Expecting ""')
print (question2(''))
print ('Expecting "a"')
print (question2('a'))
print ('Expecting "a"')
print (question2('abcd'))
print ('Expecting "amanaplanacanalpanama"')
print (question2('A man, a plan, a canal: Panama.'))
print ('Expecting "racecar"')
print (question2('The racecar is mine'))
