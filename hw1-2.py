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

import itertools

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    hands = itertools.combinations(hand, 5)
    hand_pool = []
    for hand in hands:
        #print hand, straight_with_joker(card_ranks_with_joker(hand))
        if flush_with_joker(hand) and straight_with_joker(card_ranks_with_joker(hand)):
            #print hand, get_flush_suit(hand), has_joker_by_suit(hand, get_flush_suit(hand))
            if has_joker_by_suit(hand, get_flush_suit(hand)):
                result_hand = list(hand)
                #result_hand.remove(get_hand_lowest_card(hand))
                result_hand.remove(get_joker_card(hand, suit=get_flush_suit(hand)))
                result_hand.append(make_card(get_straight_highest_rank(hand)+1,get_flush_suit(hand)))
                print "rh", result_hand
                hand_pool.append(result_hand)
            else:
                hand_pool.append(hand)

    hand_pool.sort(key=lambda hand:hand_rank(hand), reverse=True)
    print "hp", hand_pool
    return hand_pool[0]

def get_hand_lowest_card(hand):
    min_rank = str(min(card_ranks_with_joker(hand)))
    for r,s in hand:
        if make_card(min_rank, s) == "%s%s" % (r,s):
            return make_card(min_rank, s)

def card_ranks_with_joker(hand):
    ranks = ['--23456789TJQKA?'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush_with_joker(hand):
    suits = [s for r,s in hand]
    return len(set(suits)) == 1 or (len(set(suits)) == 2 and has_joker(hand))

def straight_with_joker(ranks):
    from copy import copy
    """Return True if the ordered 
    ranks form a 5-card straight."""
    ranks_without_joker = copy(ranks)
    #print ranks
    if 15 in ranks:
        ranks_without_joker.remove(15)
    
    #print (max(ranks_without_joker)-min(ranks_without_joker) == 3), len(set(ranks_without_joker)) < 5, ranks 
    return ((max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5) or \
            ((max(ranks_without_joker)-min(ranks_without_joker) == 3) and len(set(ranks_without_joker)) < 5 and 15 in ranks)

def make_card(rank, suit):
    rank_str = '-A23456789TJQKA'
    if isinstance(rank, int):
        rank = rank_str[rank] 
    else:
        rank = rank_str.index(rank)
    return "%s%s" % (rank, suit)

def get_flush_suit(hand):
    suits = [s for r,s in hand]
    return list(set(suits))[0]# and len(set(suits)) == 1

def get_straight_highest_rank(hand):
    ranks = card_ranks(hand)
    return max(ranks)# and stright(ranks)

def get_joker_card(hand, suit):
    suit_color = {"S":"B", "C":"B", "H":"R", "D":"R"}
    return ["%s%s" % (r,s) for r, s in hand if r == "?" and s in suit_color[suit]][0]

def has_joker_by_suit(hand, suit):
    suit_color = {"S":"B", "C":"B", "H":"R", "D":"R"}
    return any([r == "?" and s in suit_color[suit] for r, s in hand])

def has_joker(hand, color=None):
    color_suit = {"B":["S", "C"], "R":["H", "D"]}
    return any([r == "?" if not color else r=="?" and s in color_suit[color] for r, s in hand])

def test_best_wild_hand():
    print sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
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
