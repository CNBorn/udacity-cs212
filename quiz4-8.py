# -----------------
# User Instructions
# 
# Write a function, bsuccessors(state), that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# A state is a (here, there, t) tuple, where here and there are 
# frozensets of people (indicated by their times), and potentially
# the 'light,' t is a number indicating the elapsed time.
#
# An action is a tuple (person1, person2, arrow), where arrow is 
# '->' for here to there or '<-' for there to here. When only one 
# person crosses, person2 will be the same as person one, so the
# action (2, 2, '->') means that the person with a travel time of
# 2 crossed from here to there alone.

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
    '<-' for there to here."""
    here, there, t = state
    here = list(here)
    there = list(there)

    is_torch_here = "light" in here
    if is_torch_here:
        here.remove("light")
    else:
        there.remove("light")

    if here > there:
        from_list = here
        target = there
        direction = "->"
    else:
        from_list = there
        target = here
        direction = "<-"

    from_list = list(from_list)
    chosen = from_list.pop()
    try:
        chosen2 = from_list.pop()
    except IndexError:
        chosen2 = chosen
  
    target.append(chosen)
    if chosen2 is not None:
        target.append(chosen2)
    target.append("light")
    target = frozenset(target)

    arrow = direction

    action = (chosen, chosen2, arrow)

    t = t + max([chosen, chosen2])

    state = (frozenset(from_list), target, t)
    
    return {state:action}

    # your code here  

def test():

    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
                (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    print bsuccessors((frozenset([]), frozenset([2, 'light']), 0))
    print { (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) =={
                (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    
    return 'tests pass'

print test()

