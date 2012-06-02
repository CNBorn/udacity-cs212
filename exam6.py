# Unit 6: Fun with Words

"""
A portmanteau word is a blend of two or more words, like 'mathelete',
which comes from 'math' and 'athelete'.  You will write a function to
find the 'best' portmanteau word from a list of dictionary words.
Because 'portmanteau' is so easy to misspell, we will call our
function 'natalie' instead:

    natalie(['word', ...]) == 'portmanteauword' 

In this exercise the rules are: a portmanteau must be composed of
three non-empty pieces, start+mid+end, where both start+mid and
mid+end are among the list of words passed in.  For example,
'adolescented' comes from 'adolescent' and 'scented', with
start+mid+end='adole'+'scent'+'ed'. A portmanteau must be composed
of two different words (not the same word twice).

That defines an allowable combination, but which is best? Intuitively,
a longer word is better, and a word is well-balanced if the mid is
about half the total length while start and end are about 1/4 each.
To make that specific, the score for a word w is the number of letters
in w minus the difference between the actual and ideal lengths of
start, mid, and end. (For the example word w='adole'+'scent'+'ed', the
start,mid,end lengths are 5,5,2 and the total length is 12.  The ideal
start,mid,end lengths are 12/4,12/2,12/4 = 3,6,3. So the final score
is

    12 - abs(5-3) - abs(5-6) - abs(2-3) = 8.

yielding a score of 12 - abs(5-(12/4)) - abs(5-(12/2)) -
abs(2-(12/4)) = 8.

The output of natalie(words) should be the best portmanteau, or None
if there is none. 

Note (1): I got the idea for this question from
Darius Bacon.  Note (2): In real life, many portmanteaux omit letters,
for example 'smoke' + 'fog' = 'smog'; we aren't considering those.
Note (3): The word 'portmanteau' is itself a portmanteau; it comes
from the French "porter" (to carry) + "manteau" (cloak), and in
English meant "suitcase" in 1871 when Lewis Carroll used it in
'Through the Looking Glass' to mean two words packed into one. Note
(4): the rules for 'best' are certainly subjective, and certainly
should depend on more things than just letter length.  In addition to
programming the solution described here, you are welcome to explore
your own definition of best, and use your own word lists to come up
with interesting new results.  Post your best ones in the discussion
forum. Note (5) The test examples will involve no more than a dozen or so
input words. But you could implement a method that is efficient with a
larger list of words.
"""

"""itertools.combination
find that have common parts
countteir score
"""

import itertools

def common_part(word1, word2):

    def get_common_part(start_pos1, start_pos2, word1, word2):
        debug = False
        if word1 == "morass" and word2== "assassination":
            debug = True
            
        word1_remain_length = len(word1) - start_pos1
        word2_remain_length = len(word2) - start_pos2
        #end_same_pos1 = 0
        end_same_pos2 = word1_remain_length
        same_word_break = False
        for add_pos in xrange(min([word1_remain_length, word2_remain_length])):

            if word1[start_pos1+add_pos] == word2[start_pos2+add_pos]:
                continue
            else:
                #end_same_pos1 = start_pos1+add_pos
                end_same_pos2 = start_pos2+add_pos
                break

        seems_common_part = word2[:end_same_pos2] if end_same_pos2 != 0 else word2[:1]
            
        res =  seems_common_part if seems_common_part and seems_common_part in word1 and (seems_common_part[-1] == word1[-1] if len(seems_common_part) != 1 else seems_common_part == word1[-1]) and seems_common_part == word1[0-len(seems_common_part):] else ""
        if debug:
            print seems_common_part, word1, word2, start_pos1, start_pos2, res
        return res
    
    result = [get_common_part(word1.index(w, i1), word2.index(w2, i2), word1, word2) for i1, w in enumerate(word1) for i2, w2 in enumerate(word2) if w==w2]
    result = list(set([r for r in result if r]))
    print word1, word2, result
    return result

def word_score(word1, word2):
    start = len(word1)
    #print word1, word2

    mid_strs = common_part(word1, word2)
    #print mid_strs

    if not mid_strs: return 0
    result = []

    for mid_str in mid_strs:
        try:
            end_str = word2[len(mid_str):]
        except IndexError:
            return 0
        start_str = word1[:len(word1)-len(mid_str)]
        if not start_str:
            return 0
        print "-", start_str, mid_str, end_str

        the_word = start_str + mid_str + end_str
        ideal_start_pos = len(the_word) / 4
        ideal_mid_pos = len(the_word) / 2

        word_score = len(the_word) - abs(len(start_str) - ideal_start_pos) - abs(len(mid_str) - ideal_mid_pos) - abs(len(end_str) - ideal_start_pos)
        result.append((word_score, the_word))

    result.sort(key=lambda x:x)
    print "result", result
    return result

def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    word_pairs = itertools.permutations(words, 2)
    word_list = itertools.chain.from_iterable([word_score(word1, word2) for (word1, word2) in word_pairs if word_score(word1, word2)])
    result = list(word_list)
    highest_score = max(result)[0] if result else 0
    print highest_score
    r =  [word for score, word in result if score == highest_score]
    print "r",r
    return r[0] if r else None

def test_natalie():
    "Some test cases for natalie"
    assert natalie(['adolescent', 'scented', 'centennial', 'always', 'ado']) in ('adolescented','adolescentennial')
    assert natalie(['eskimo', 'escort', 'kimchee', 'kimono', 'cheese']) == 'eskimono'
    assert natalie(['kimono', 'kimchee', 'cheese', 'serious', 'us', 'usage']) == 'kimcheese'
    assert natalie(['circus', 'elephant', 'lion', 'opera', 'phantom']) == 'elephantom'
    assert natalie(['programmer', 'coder', 'partying', 'merrymaking']) == 'programmerrymaking'
    assert natalie(['int', 'intimate', 'hinter', 'hint', 'winter']) == 'hintimate'
    assert natalie(['morass', 'moral', 'assassination']) == 'morassassination'
    assert natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist', 'neurotoxin', 'scientist', 'gist']) in ('entrepreneuropsychologist', 'entrepreneurotoxin')
    assert natalie(['perspicacity', 'cityslicker', 'capability', 'capable']) == 'perspicacityslicker'
    assert natalie(['backfire', 'fireproof', 'backflow', 'flowchart', 'background', 'groundhog']) == 'backgroundhog'
    assert natalie(['streaker', 'nudist', 'hippie', 'protestor', 'disturbance', 'cops']) == 'nudisturbance'
    assert natalie(['night', 'day']) == None
    assert natalie(['dog', 'dogs']) == None
    assert natalie(['test']) == None
    assert natalie(['']) ==  None
    assert natalie(['ABC', '123']) == None
    assert natalie([]) == None

    assert natalie(['freud', 'mormons', 'dianetics', 'shinrikyo', 'jonestown', 'moonies']) != None
    
    return 'tests pass'


print test_natalie()


