# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

import itertools

def iter_all_same_char_pos(c, text):
    pos = 0
    result = text.find(c, pos)
    while result != -1:
        yield result
        pos = result + 1
        result = text.find(c, pos)

def iter_whether_subpalindrome(pos_list, text):
    poss = itertools.combinations(pos_list,2)
    poss_l = [l for l in poss if l[0] < l[1]]

    for pos_b, pos_l in poss_l:
        palindrome_break = False
        d_pos_b, d_pos_l = pos_b, pos_l 
        while d_pos_b != d_pos_l:
            result = text[d_pos_b] == text[d_pos_l]
            if not result:
                palindrome_break = True
                break
            if abs(d_pos_b-d_pos_l) == 1:
                break
            else:
                if d_pos_b < len(text)-1:
                    d_pos_b += 1
                if d_pos_l > 0:
                    d_pos_l -= 1
                #print text, d_pos_b, d_pos_l
            #print
        if not palindrome_break:
            yield True, (pos_b, pos_l)

def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if not text:
        return (0,0)

    r_list = []
    text = text.upper()
    for c in set(list(text)):
        r_list.extend([(abs(pos[0] - pos[1]), pos) for is_pal, pos in iter_whether_subpalindrome(iter_all_same_char_pos(c, text), text) if is_pal])

    if r_list:
        r = max(r_list)
        #print text, (r[1][0], r[1][1]+1)
        return (r[1][0], r[1][1]+1)
    
def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()

