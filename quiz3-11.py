#----------------
# User Instructions
#
# Write the compiler for alt(x, y) in the same way that we 
# wrote the compiler for lit(s) and seq(x, y). 

'''
def matchset(pattern, text):
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
'''

def lit(s): return lambda text: set([text[len(s):]]) if text.startswith(s) else null

def seq(x, y): return lambda text: set().union(*map(y, x(text)))

def alt(x, y): return lambda text: x(text) | y(text)
        
null = frozenset([])

def test():
    g = alt(lit('a'), lit('b'))
    assert g('abc') == set(['bc'])
    return 'test passes'

print test()

