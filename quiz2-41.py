# --------------
# User Instructions
#
# Write a function, compile_word(word), that compiles a word
# of UPPERCASE letters as numeric digits. For example:
# compile_word('YOU') => '(1*U + 10*O +100*Y)' 
# Non-uppercase words should remain unchaged.

def compile_word(word):
    import string
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    num_word, results = [], []
    for w in word:
        if w in string.uppercase:
            num_word.append(w)
        else:
            results.append("+".join(["%s*%s" % (10*(len(num_word) - (idx+1)), s) for idx,s in enumerate(num_word)]))
            num_word = []
            results.append(w)

    results.append("+".join(["%s*%s" % (10 ** (len(num_word) - (idx+1)), s) for idx,s in enumerate(num_word)]))

    return "".join(results)

if __name__ == "__main__":
    print compile_word("YOU")
