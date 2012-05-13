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
import cProfile

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
    txt = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nunc libero, venenatis id porttitor et, pharetra et urna. Donec nec velit varius massa lacinia placerat. Fusce vulputate mollis nunc, et tincidunt erat imperdiet at. Aliquam sit amet tortor in sem tempor condimentum. Curabitur vel mauris lectus. Nulla at metus ac turpis malesuada accumsan vitae et arcu. Sed semper pellentesque est quis tristique. Mauris egestas porttitor risus, lobortis accumsan ligula sollicitudin eu. Ut sollicitudin nibh ac quam viverra id euismod velit posuere. Nullam ut ultrices arcu.

    Quisque et turpis massa, quis faucibus libero. Sed nulla nunc, pellentesque in congue id, dictum eget sem. Vivamus ultrices interdum velit ac pulvinar. Curabitur facilisis, purus nec commodo vulputate, purus magna dictum dolor, at fringilla arcu ante nec est. Nulla rutrum semper ullamcorper. Praesent fermentum ultrices sem id auctor. Sed eget euismod tortor. Vestibulum vestibulum, massa faucibus semper laoreet, dui arcu viverra turpis, eu rhoncus ante mauris suscipit velit. Phasellus vitae nisi molestie ligula eleifend fermentum at vel est. Aliquam quis erat massa, sit amet fringilla mi. Nulla ac dolor nisl. Pellentesque egestas felis id ante bibendum sed aliquet augue mollis. Maecenas condimentum lacinia mauris, ut egestas est bibendum quis. Donec vel sem nec turpis bibendum ultricies eget sed diam. Vestibulum sed metus vel ipsum convallis adipiscing.

    Nulla eu lacus eget est pellentesque pulvinar eu nec libero. Nullam orci ligula, consectetur eget adipiscing at, scelerisque quis neque. Curabitur tempor urna ac nisi placerat nec tincidunt magna pulvinar. Praesent id congue augue. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum pretium ullamcorper dolor sit amet consectetur. Curabitur vehicula ultricies commodo. In erat massa, condimentum nec elementum id, ullamcorper in felis.

    Integer nec imperdiet ante. Vestibulum pellentesque libero eget odio mollis at ullamcorper ipsum cursus. Curabitur quis justo a leo porta aliquam vitae eu nunc. In dolor sem, viverra non euismod at, auctor sit amet turpis. Phasellus convallis egestas dui, sed pharetra leo dignissim in. Praesent mi tortor, posuere ut gravida at, facilisis vel nisl. Integer orci metus, volutpat sit amet tincidunt eu, tincidunt vitae sapien. In imperdiet elementum lobortis. Vestibulum viverra augue eu urna vehicula feugiat. Aliquam sapien velit, posuere ut egestas at, bibendum nec risus. Vestibulum lacus elit, semper sit amet laoreet at, bibendum non risus.

    Duis turpis dolor, tincidunt sed condimentum ut, sodales vitae eros. Morbi urna odio, eleifend at adipiscing vitae, pretium ut mi. In consequat, tellus quis scelerisque aliquam, turpis metus sagittis mi, semper dapibus sem ligula et felis. Curabitur turpis ante, pretium id mollis vitae, fringilla nec turpis. In enim ligula, porta nec posuere quis, vestibulum ac justo. Vestibulum laoreet nisi ac magna accumsan aliquet. Pellentesque sed metus bibendum enim sodales rutrum. Nullam pretium arcu quis erat eleifend tempus. Suspendisse lacinia, est nec mollis lobortis, dui leo commodo nulla, a aliquam diam orci ut mauris. Aenean non purus in eros fermentum ultrices. In at libero dolor, ut venenatis ante. Phasellus turpis quam, laoreet at porta nec, gravida a erat. Morbi purus augue, fermentum non aliquet blandit, fermentum viverra tortor. Donec consequat sodales libero et venenatis. Nam a felis non massa aliquet pharetra dictum quis erat. ingirumimusnocteetconsumimurigni"""
    assert L(txt) == (3532, 3564)

    return 'tests pass'

print cProfile.run('print test()')


