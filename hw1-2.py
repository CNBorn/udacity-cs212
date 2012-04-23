# CS 212, hw1-2: Jokers Wild
#
# -----------------
# User Instructions
#
# Write a function best_wild_hand(hand) that takes as
# input a 7-card hand and returns the best 5 card hand.
# In this problem, it is possible for a hand to include
# jokers. Jokers will be treated as 'wild cards' which
# can take any rank or suit of the same color. The 
# black joker, '?B', can be used as any spade or club
# and the red joker, '?R', can be used as any heart 
# or diamond.
#
# The itertools library may be helpful. Feel free to 
# define multiple functions if it helps you solve the
# problem. 
#
# -----------------
# Grading Notes
# 
# Muliple correct answers will be accepted in cases 
# where the best hand is ambiguous (for example, if 
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

from copy import copy, deepcopy
import itertools
from itertools import chain, combinations

def best_wild_hand(origin_hand):
    "Try all values for jokers in all 5-card selections."
    hands = itertools.combinations(origin_hand, 5)
    hand_pool = []
    for hand in hands:
        if has_joker(hand):
            for hand_with_joker_processed in replace_joker_with_cards(hand):
                hand_pool.append(hand_with_joker_processed)
        else:
            hand_pool.append(hand)

    hand_pool = [hands for hands in hand_pool if hands] #[]
    hand_pool.sort(key=lambda hand:hand_rank(hand), reverse=True)
    return hand_pool[0]

def replace_joker_with_cards(hand):
    jokers = get_joker_card(hand)
    for joker_combination in powerset(jokers):
        result = get_hand_replaced_with_joker_list(hand, joker_combination)
        yield list(result)

def get_hand_replaced_with_joker_list(hand, joker_combination):

    suit_list = []
    available_suits = []
    hand_without_joker = list(deepcopy(hand))

    for rj, cj in joker_combination:
        hand_without_joker.remove("%s%s" % (rj, cj)) #remove joker
        suit_list.extend(get_joker_can_suit(cj))

    available_suits.extend(itertools.product(["23456789TJQKA"], suit_list))

    cards = []
    available_cards = []
    for r, s in available_suits:
        available_cards.append(itertools.product(r, s))
    available_ranks_suits = [list(i) for i in available_cards]
   
    hand_pool = []
    for t in available_ranks_suits:
        cards.extend(["%s%s" % (r,s) for (r, s) in t])

    #combinations for n_joker cards
    for card_set in combinations(cards, len(joker_combination)):
        r = list(itertools.chain.from_iterable([hand_without_joker, card_set]))
        r = list(set(r))
        #print card_set, r
        if len(r) == 5 and not has_joker(list(r)):
            hand_pool.append(list(r))

    hand_pool.sort(key=lambda hand:hand_rank(hand), reverse=True)
    return hand_pool and hand_pool[0] or []

#good stuff comes from Recipe
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def get_joker_can_suit(color):
    color_suit = {"B":["S", "C"], "R":["H", "D"]}
    return color_suit[color]

def get_joker_card(hand, suit=None):
    if suit:
        suit_color = {"S":"B", "C":"B", "H":"R", "D":"R"}
        return ["%s%s" % (r,s) for r, s in hand if r == "?" and s in suit_color[suit]]
    return ["%s%s" % (r, s) for r, s in hand if r == "?"]

def has_joker(hand, color=None):
    color_suit = {"B":["S", "C"], "R":["H", "D"]}
    return any([r == "?" if not color else r=="?" and s in color_suit[color] for r, s in hand])

def test_best_wild_hand():
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print sorted(best_wild_hand("6C 3C 8C 9C 2S ?B ?R".split()))
    assert (sorted(best_wild_hand("6C 3C 8C 9C 2S ?B ?R".split()))
            == ['3C', '6C', '8C', '9C', 'AC'])
    return 'test_best_wild_hand passes'

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
    ranks = ['?-23456789TJQKA'.index(r) for r, s in hand]
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

if __name__ == "__main__":
    test_best_wild_hand()
