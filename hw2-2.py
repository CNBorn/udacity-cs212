#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools

def is_top(foo):
    return foo == 5

def is_bottom(foo):
    return foo == 1

def adjacent(foo, bar):
    return abs(foo-bar) == 1

def floor_puzzle():
    # Your code here
    geneator = ((Hopper, Kay, Liskov, Perlis, Ritchie) for (Hopper, Kay, Liskov, Perlis, Ritchie) in itertools.permutations(xrange(1,6)) if \
            not is_top(Hopper) and
            not is_bottom(Kay) and
            not is_top(Liskov) and 
            not is_bottom(Liskov) and
            Perlis > Kay and
            not adjacent(Ritchie, Liskov) and
            not adjacent(Liskov, Kay))
    Hopper, Kay, Liskov, Perlis, Ritchie = next(geneator)
    return [Hopper, Kay, Liskov, Perlis, Ritchie]

if __name__ == "__main__":
    print floor_puzzle()
