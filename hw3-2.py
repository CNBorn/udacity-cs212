# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the 
# non-negative numbers. The runtime of your program should be 
# proportional to the LOGARITHM of the input. You may want to 
# do some research into binary search and Newton's method to 
# help you out.
#
# This function should return another function which computes the
# inverse of the input function. 
#
# Your inverse function should also take an optional parameter, 
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The 
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is 
# efficient enough. 

"""
int binary_search(int A[], int key, int imin, int imax)
{
  // test if array is empty
  if (imax < imin):
    // set is empty, so return value showing not found
    return KEY_NOT_FOUND;
  else
    {
      // calculate midpoint to cut set in half
      int imid = (imin + imax) / 2;
 
      // three-way comparison
      if (A[imid] > key):
        // key is in lower subset
        return binary_search(A, key, imin, imid-1);
      else if (A[imid] < key):
        // key is in upper subset
        return binary_search(A, key, imid+1, imax);
      else:
        // key has been found
        return imid;
    }
}

"""
def derivative(f):
    def df(x, h=0.1e-5):
        return ( f(x+h/2) - f(x-h/2) )/h
    return df

def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        #def b_search(f, key, imin, imax):
        #    imid = (x + y) / 2
        #    if f(imid) > key:
        #        return b_search(f, key, imin, imid-delta)
        #    elif f(imid) < key:
        #        return b_search(f, key, imid+delta, imax)
        #    else:
        #        return imid
       
        def newton(f, given_val, val):
            #return val - (f(val) /  derivative(f)(val))
            #http://zh.wikipedia.org/wiki/%E7%89%9B%E9%A1%BF%E6%B3%95
            return val +(given_val/val-val) * 0.5 

        result = newton(f, y, y)
        for i in xrange(10000):
            result = newton(f,y, result)

        print result
        return result

    return f_1 

def inverse(f, delta = 1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    return slow_inverse(square)
    
def square(x): return x*x
sqrt = slow_inverse(square)

print sqrt(100)
print sqrt(10000)
print sqrt(1000000000)

