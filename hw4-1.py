# -----------------
# User Instructions
# 
# In this problem you will be refactoring the bsuccessors function.
# Your new function, bsuccessors3, will take a state as an input
# and return a dict of {state:action} pairs. 
#
# A state is a (here, there, light) tuple. Here and there are 
# frozensets of people (each person is represented by an integer
# which corresponds to their travel time), and light is 0 if 
# it is on the `here` side and 1 if it is on the `there` side.
#
# An action is a tuple of (travelers, arrow), where the arrow is
# '->' or '<-'. See the test() function below for some examples
# of what your function's input and output should look like.
from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def bsuccessors3(state):
    """Return a dict of {state:action} pairs.  State is (here, there, light)
    where here and there are frozen sets of people, light is 0 if the light is 
    on the here side and 1 if it is on the there side.
    Action is a tuple (travelers, arrow) where arrow is '->' or '<-'"""
    here, there, light = state
    if not light:
        return dict([((here - frozenset(list(e1)), 
                 there | frozenset(list(e1)),
                 abs(light-1)),(set(list(e1)), '->')) for e1 in powerset(here) if e1 ])
    else:
        return dict([((here | frozenset(list(e1)), 
                 there - frozenset(list(e1)),
                 abs(light-1)),(set(list(e1)), '<-')) for e1 in powerset(there) if e1 ])
             

def test():
    assert bsuccessors3((frozenset([1]), frozenset([]), 0)) == {
            (frozenset([]), frozenset([1]), 1)  :  (set([1]), '->')}

    assert bsuccessors3((frozenset([1, 2]), frozenset([]), 0)) == {
            (frozenset([1]), frozenset([2]), 1)    :  (set([2]), '->'), 
            (frozenset([]), frozenset([1, 2]), 1)  :  (set([1, 2]), '->'), 
            (frozenset([2]), frozenset([1]), 1)    :  (set([1]), '->')}

    assert bsuccessors3((frozenset([2, 4]), frozenset([3, 5]), 1)) == {
            (frozenset([2, 4, 5]), frozenset([3]), 0)   :  (set([5]), '<-'), 
            (frozenset([2, 3, 4, 5]), frozenset([]), 0) :  (set([3, 5]), '<-'), 
            (frozenset([2, 3, 4]), frozenset([5]), 0)   :  (set([3]), '<-')}
    return 'tests pass'

print test()

