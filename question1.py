"""
Question 1:
Given two strings s and t, determine whether
some anagram of t is a substring of s.
For example: if s = "udacity" and t = "ad",
then the function returns True. Your function
definition should look like: question1(s, t)
and return a boolean True or False.

I knew I needed to loop through both strings in
some fashion. I decided the fastest way to track
occurances of t would be to map it to a dictionary.

I wanted to loop through all substrings of s and
check the characters against the anagram
dictionary.

"""

def question1(s,t):
    """
    Covering my edge cases.
    """
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

    """
    Populate the dictionary.
    """
    reset(anagram)

    """
    I'm creating a helper function I can
    use to check each element of
    substring ss against the anagram
    dictionary.
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

"""
Trying my test cases.
"""
print('Expecting True:')
print(question1('udacity', 'ad'))

print('Expecting True:')
print(question1('citcity', 'city'))

print('Expecting False:')
print(question1('udacity', 'adda'))

print('Expecting True:')
print(question1('', ''))

print('Expecting True:')
print(question1('udacity', 'c'))

print('Expecting False:')
print(question1('', 'word'))
