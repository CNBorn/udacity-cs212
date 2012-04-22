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

from copy import copy
import itertools

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    hands = itertools.combinations(hand, 5)
    hand_pool = []
    for hand in hands:

        if flush_with_joker(hand) and straight_with_joker(card_ranks_with_joker(hand)):
            if has_joker_by_suit(hand, get_flush_suit(hand)):
                result_hand = list(hand)
                for joker_card in get_joker_card(hand, suit=get_flush_suit(hand)):
                    result_hand.remove(joker_card)
                    result_hand.append(make_card(get_straight_highest_rank(hand)+1,get_flush_suit(hand)))
                hand_pool.append(result_hand)
            else:
                hand_pool.append(hand)

        elif kind_with_joker(4, hand):
            result_hand = list(hand)
            for joker_card in get_joker_card(hand):
                result_hand.remove(joker_card)
            result_hand.extend(get_missing_4_kind_card(hand)[:len(get_joker_card(hand))])
            hand_pool.append(result_hand)

    hand_pool.sort(key=lambda hand:hand_rank(hand), reverse=True)
    return hand_pool[0]

def get_missing_4_kind_card(hand):
    ranks = card_ranks(hand)
    missing_cards, missing_rank, missing_suit = get_missing_for_kind(4, hand)
    results = []
    for (missing_rank, missing_suit) in itertools.product(missing_rank, missing_suit):
        results.append(make_card(missing_rank, missing_suit))
    return results

def get_missing_for_kind(n, hand):
    remain_suits = ["C", "H", "D", "S"]
    used_suits = []
    original_hand = copy(hand)
    hand = [card for card in hand if card[0] != "?"] #filter out joker
    max_result = max([(k, len(list(g))) for k,g in itertools.groupby([r for r,s in hand])])
    max_rank, max_rank_count = max_result
    missing_cards = n - max_rank_count
    missing_rank = max_rank
    for r,s in original_hand:
        if r == missing_rank and s in remain_suits:
            used_suits.append(s)
            remain_suits.remove(s)

    for r,s in original_hand:
        if r == "?":
            joker_suits = get_joker_can_suit(s)
            remain_suits.extend(list(set(joker_suits) & set(remain_suits) - set(used_suits)))

    return missing_cards, missing_rank, list(set(remain_suits))

def get_joker_can_suit(color):
    color_suit = {"B":["S", "C"], "R":["H", "D"]}
    return color_suit[color]

def kind_with_joker(n, hand):
    """Return the first rank that this hand has 
    exactly n-of-a-kind of. Return None if there 
    is no n-of-a-kind in the hand."""
    ranks = card_ranks_with_joker(hand)
    joker_count = ranks.count(15)
    for r in ranks:
        if ranks.count(r) == n or ranks.count(r) + joker_count == n:
            return r
    return None

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
    """Return True if the ordered 
    ranks form a 5-card straight."""
    ranks_without_joker = copy(ranks)
    if 15 in ranks:
        ranks_without_joker.remove(15)
    return ((max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5) or \
            ((max(ranks_without_joker)-min(ranks_without_joker) == 3) and len(set(ranks_without_joker)) < 5 and 15 in ranks)

def make_card(rank, suit):
    rank_str = '-A23456789TJQKA'
    if isinstance(rank, int):
        rank = rank_str[rank] 
    return "%s%s" % (rank, suit)

def get_flush_suit(hand):
    suits = [s for r,s in hand]
    return list(set(suits))[0]# and len(set(suits)) == 1

def get_straight_highest_rank(hand):
    ranks = card_ranks(hand)
    return max(ranks)# and stright(ranks)

def get_joker_card(hand, suit=None):
    if suit:
        suit_color = {"S":"B", "C":"B", "H":"R", "D":"R"}
        return ["%s%s" % (r,s) for r, s in hand if r == "?" and s in suit_color[suit]]
    return ["%s%s" % (r, s) for r, s in hand if r == "?"]

def has_joker_by_suit(hand, suit):
    suit_color = {"S":"B", "C":"B", "H":"R", "D":"R"}
    return any([r == "?" and s in suit_color[suit] for r, s in hand])

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
