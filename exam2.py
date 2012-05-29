"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""
import itertools
def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    Monday, Tuesday, Wednesday, Thursday, Friday = xrange(5)
    for Hamming, Knuth, Minsky, Simon, Wilkes in itertools.permutations(xrange(5)):
        for writer, manager, designer, Programmer, person in itertools.permutations(xrange(5)):
            for droid, laptop, iphone, tablet in itertools.permutations(xrange(4)):
                if Wednesday == laptop and \
                    Wilkes != Programmer and \
                    Wilkes in (Programmer, droid) and Hamming in (Programmer, droid) and \
                    Minsky != writer and \
                    Knuth != manager and tablet != manager and \
                    Knuth == manager + 1 and \
                    Simon == manager and \
                    designer != Thursday and \
                    Friday != tablet and \
                    designer != droid and \
                    (Wilkes in (Monday, writer) and laptop in (Monday, writer)) and \
                    Tuesday in (iphone, tablet):
                    result = {Hamming:"Hamming", Knuth:"Knuth", Minsky:"Minsky", Simon:"Simon", Wilkes:"Wilkes"}
                    res = []
                    for x in range(0,5):
                        res.append(result[x])
                    return res
                        
print logic_puzzle()
