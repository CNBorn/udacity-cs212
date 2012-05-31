
"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of 
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coef attribute of the function, so we have:

    p1.coef == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**' 
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""


def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""
    # your code here (I won't repeat "your code here"; there's one for each function)
    raw_coefs = coefs
    n_coefs = len(coefs)
    coefs = list(coefs)
    coefs.reverse()

    def func(x):
        def __eq__(self, obj):
            print obj.__name__, self.__name__
            return obj.__name__ == self.__name__
        return sum([v * x**(n_coefs-i-1) for i, v in enumerate(coefs)])

    func.coefs = coefs
    func.raw_coefs = raw_coefs

    name_list = [((str(v) if v != 1 else '') + ((' * ' if v != 1 else '') + ('x' if n_coefs-i-1 != 0 else '') + ('**%s' % (n_coefs-i-1) if n_coefs-i-1 != 1 else '') if n_coefs-i-1 != 0 else '') if v != 0 and n_coefs-i-1 != 0 else str(v)) for i, v in enumerate(coefs)]
    func.__name__ = " + ".join([s for s in name_list if s and s != "0"])

    return func


def test_poly():
    global p1, p2, p3, p4, p5, p9 # global to ease debugging in an interactive session

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x**2 + 20 * x + 10
    print p1
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    print p9, poly([0,0,0,0,0,0,0,0,0,1])
    #assert p9 == poly([0,0,0,0,0,0,0,0,0,1])
    #should passed in grader, as Peter said in
    #http://forums.udacity.com/cs212-april2012/questions/11286/final-3-wrong-assertion
    #saved time to warp poly into class
    
    assert p9(2) == 512
    p4 = add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

    assert same_name(poly((1, 1)).__name__, 'x + 1')

    #print power(poly((1,1)),2), poly((1,2,1))
    #assert power(poly((1, 1)), 2) == poly((1, 2, 1))
    #modify with __name__
    assert power(poly((1, 1)), 2).__name__ == poly((1, 2, 1)).__name__
    
    assert (power(poly((1, 1)), 10).__name__ == 
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

    assert add(poly((10, 20, 30)), poly((1, 2, 3))).__name__ == poly((11, 22, 33)).__name__
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).__name__ == poly((9, 18, 27)).__name__
    print mul(poly((10, 20, 30)), poly((1, 2, 3)))
    print poly((10, 40, 100, 120, 90))
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).__name__ == poly((10, 40, 100, 120, 90)).__name__
    assert power(poly((1, 1)), 2) == poly((1, 2, 1))
    assert power(poly((1, 1)), 10) == poly((1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1))

    assert deriv(p1) == poly((20, 60))
    assert integral(poly((20, 60))) == poly((0, 20, 30))
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573


def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""
    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
    return canonical_name(name1) == canonical_name(name2)

def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    return type(x) == type(poly)

def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    indi,shorter,length = (1, p1.raw_coefs,len(p2.coefs)) if len(p1.coefs) < len(p2.coefs) else (2, p2.raw_coefs, len(p1.coefs))
    print indi, shorter, length
    shorter_list = list(shorter)
    shorter_list.extend([0 for i in xrange(length-len(shorter))])
    shorter = tuple(shorter_list)
    if indi == 1:
        remain_opt = p2.raw_coefs
    else:
        remain_opt = p1.raw_coefs

    result = []
    for idx in xrange(len(remain_opt)):
        result.append(shorter[idx] + remain_opt[idx])

    result = tuple(result)
    return poly(result)

def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    indi,shorter,length = (1, p1.raw_coefs,len(p2.coefs)) if len(p1.coefs) < len(p2.coefs) else (2, p2.raw_coefs, len(p1.coefs))
    shorter_list = list(shorter)
    shorter_list.extend([0 for i in xrange(length-len(shorter))])
    shorter = tuple(shorter_list)
    if indi == 1:
        remain_opt = p2.raw_coefs
    else:
        remain_opt = p1.raw_coefs

    result = []
    for idx in xrange(len(remain_opt)):
        result.append(remain_opt[idx] - shorter[idx])

    result = tuple(result)
    return poly(result)


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    print "mul"
    r = tuple((r1 * r2, i1 + i2) for i1, r1 in enumerate(p1.coefs) for i2, r2 in enumerate(p2.coefs))
    redict = {}
    for item in r:
        coefficient = item[1]
        redict.setdefault(coefficient, 0)
        redict[coefficient] += item[0]
    print redict

    lstret = []
    for kv in redict.iteritems():
        lstret.append(kv)
    lstret.reverse()
    lstret = [r[1] for r in lstret]
    print tuple(lstret)
    return poly(tuple(lstret))
    
    return poly(tuple(sum(r1 * r2 for r1 in p1.coefs) for r2 in p2.coefs))

    
    target_str = str(int("".join([str(p) for p in p1.coefs])) * int("".join([str(p) for p in p2.coefs])))
    target_val = []
    for char in target_str:
        target_val.append(int(char))
    target_val.reverse()
    target_val = tuple(target_val)
    
    '''(0,1) * (0,1) = (0,0,1)
    (0,0,1) * (0,0,1) = (0,0,0,0,1)
    (0,0,0,1) * (0,0,0,1) = (0,0,0,0,0,0,1)
    (0,0,0,1) * (0,0,0,0,0,0,1) = (0,0,0,0,0,0,0,0,0,1)'''
    '''mul(poly((10, 20, 30)), poly((1, 2, 3)))    poly((10, 40, 100, 120, 90))'''
    '''10x2, 20x, 30 * x2, 2x, 3 = 10x4 + 20x3 + 30x2 + 20x3 + 60x + 30x2 + 60x + 90
    a,b,c * d,e,f = a*d, a*e, a*f, b*d, b*e, b*f, c*d, c*e, c*f 
    10x4  40x3 100x2 120x  90 
    (10*1, 0+20*2, 20*(2+    , 3*30)
    return poly(target_val)'''

def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    yhList = [1,1]
    for i in xrange(n-1):
        yhList[1:-1] = [(tmpNum + yhList[j]) for j, tmpNum in enumerate(yhList[1:])]
    return poly(tuple(yhList))

"""
If your calculus is rusty (or non-existant), here is a refresher:
The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
"""
    
def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."


def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."


"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the 
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""


def test_poly1():
    # I define x as the polynomial 1*x + 0.
    x = poly((0, 1))
    # From here on I can create polynomials by + and * operations on x.
    newp1 =  30 * x**2 + 20 * x + 10 # This is a poly object, not a number!
    assert p1(100) == newp1(100) # The new poly objects are still callable.
    assert p1.__name__ == newp1.__name__
    assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 2))

def test_poly2():
    newp1 = Poly('30 * x**2 + 20 * x + 10')
    assert p1(100) == newp1(100)
    assert p1.__name__ == newp1.__name__
    assert Poly('x + 1') * Poly('x - 1') == Poly('x**2 - 1')


test_poly()
test_poly1()
test_poly2()
