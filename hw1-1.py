# CS 212, hw1-1: 7-card stud
#
# -----------------
# User Instructions
#
# Write a function best_hand(hand) that takes a seven
# card hand as input and returns the best possible 5
# card hand. The itertools library has some functions
# that may help you solve this problem.
#
# -----------------
# Grading Notes
#
# Muliple correct answers will be accepted in cases
# where the best hand is ambiguous (for example, if
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

from itertools import groupby

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."

    # Your code here
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks_7(hand)
    if has_straight(hand) and has_flush(hand):
        return get_flush_card(hand)
    elif kind(4, ranks):
        four_kinds = get_specify_cards(hand, kind(4, ranks))
        last_card = get_max_cards(hand, 1, get_specify_cards(hand, kind(4, ranks)))
        return four_kinds + last_card
    elif kind(3, ranks) and kind(2, ranks):
        three_kinds = get_specify_cards(hand, kind(3, ranks))
        two_kinds = get_specify_cards(hand, kind(2, ranks))
        return three_kinds + two_kinds
    #Haven't got right answer to the following situation.
    elif has_flush(hand):
        return (5, max(card_ranks(get_flush_card(hand))))
    elif has_straight(hand):
        return (4, max(card_ranks(get_straight_card(hand))))
    elif kind(3, ranks):
        return (3, kind(3,ranks), get_max_cards(hand, 2, filterfalse=kind(3, ranks)))
    elif two_pair(ranks):
        return (2, two_pair(ranks), get_max_cards(hand, 1, filterfalse=two_pair(ranks)))
    elif kind(2, ranks):
        return (1, kind(2, ranks), get_max_cards(hand, 3, filterfalse=kind(2, ranks)))
    else:
        return (0, get_max_cards(hand, 5))

def get_max_cards(hand, count, filterfalse):
    filter_content = filterfalse() if hasattr(filterfalse, "__call__") else filterfalse
    remain_hand = filter(lambda x:x not in filter_content, hand)
    remain_hand.sort(key=lambda c:card_rank(c), reverse=True)
    return remain_hand[:count]

def get_specify_cards(hand, filter_func):
    filter_content = filter_func() if hasattr(filter_func, "__call__") else filter_func
    return filter(lambda c:card_rank(c[0]) == filter_content, hand)

def get_suits(hand):
    results = [c[1] for c in hand]
    results.sort(reverse=True)
    return results

def has_flush(hand):
    suit_results = [list(g) for k,g in groupby(get_suits(hand))]
    return any(filter(lambda s:len(s) >= 5, suit_results))

def get_flush_card(hand):
   suit_results = [list(g) for k,g in groupby(get_suits(hand))]
   flush_suits = filter(lambda s:len(s) >= 5, suit_results)
   flush_suits.sort(key=lambda x:len(x), reverse=True)
   flush_suit = list(set(flush_suits[0]))[0]
   hand.sort(reverse=True)
   results = filter(lambda c:c[1] == flush_suit, hand)
   results.sort(key=lambda x:card_rank(x), reverse=True)
   return results[:5]

def card_rank(card):
    return '--23456789TJQKA'.index(card[0])

def get_straight_card(hand):
    ranks = card_ranks_7(hand)
    results = []
    for r in xrange(max(ranks), max(ranks)-5, -1):
        results.extend(filter(lambda c:c[0] == r, hand))
    return results

def has_straight(hand):
    ranks = card_ranks_7(hand)
    return all([x in ranks for x in xrange(min(ranks), min(ranks)+5)])

def card_ranks_7(hand):
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [7, 6, 5, 4, 3, 2, 1] if (ranks == [14, 7, 6, 5, 4, 3, 2]) else ranks  #potential BUG

# ------------------
# Provided Functions
#
# You may want to use some of the functions which
# you have already defined in the unit to write
# your best_hand function.

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)
   
def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has
    exactly n-of-a-kind of. Return None if there
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None
   
def test_best_hand():
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_hand passes'

print test_best_hand()
