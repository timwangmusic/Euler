"""Compares hand strength of the same rank
Functions returns +1 of hand A is stronger, returns -1 if hand B is stronger, returns 0 if it is a chop.
"""

from rank import Rank
from collections import Counter, namedtuple
from utils import compare

Hand = namedtuple("Hand", "cards")

# a Card consists of a suit and a rank, e.g. Ace of Heart (AH)
Card = namedtuple("Card", "value suit")


def high_card(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    for r_a, r_b in zip(sorted(ranks_a, reverse=True), sorted(ranks_b, reverse=True)):
        if r_a > r_b:
            return 1
        elif r_a < r_b:
            return -1
    return 0


def one_pair(hand_a, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    counts_a = Counter(ranks_a)
    counts_b = Counter(ranks_b)
    x = counts_a.most_common(1)[0]
    y = counts_b.most_common(1)[0]
    if x > y:
        return 1
    elif x < y:
        return -1
    # not a two pairs so the rest of the three cards have to have different ranks
    a_x, a_y, a_z = [x[0] for x in counts_a.most_common(4)[1:]]
    b_x, b_y, b_z = [x[0] for x in counts_b.most_common(4)[1:]]
    return high_card(Hand([Card(a_x, 'H'), Card(a_y, 'H'), Card(a_z, 'H')]),
                     Hand([Card(b_x, 'H'), Card(b_y, 'H'), Card(b_z, 'H')]))


def two_pairs(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    counts_a = Counter(ranks_a)
    counts_b = Counter(ranks_b)
    for x, y in zip(sorted(counts_a.most_common(2), key=lambda k: k[0], reverse=True),
                    sorted(counts_b.most_common(2), key=lambda k: k[0], reverse=True)):
        if x < y:
            return -1
        elif x > y:
            return 1
    return 0


def three_of_a_kind(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    counts_a = Counter(ranks_a)
    counts_b = Counter(ranks_b)
    x = counts_a.most_common(1)[0]
    y = counts_b.most_common(1)[0]
    if x > y:
        return 1
    if x < y:
        return -1
    # not a full house so the rest of two card ranks have to be different
    a_x, a_y = [x[0] for x in counts_a.most_common(3)[1:]]
    b_x, b_y = [x[0] for x in counts_b.most_common(3)[1:]]
    # suit does not matter in this case
    return two_pairs(Hand([Card(a_x, 'H'), Card(a_y, 'H')]), Hand([Card(b_x, 'H'), Card(b_y, 'H')]))


def straight(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    ranks_a.sort()
    ranks_b.sort()
    if ranks_a[-1] == ranks_b[-1]:
        if ranks_a[-2] == ranks_b[-2]:
            return 0
        # wheels vs nuts straight
        if ranks_a[-2] > ranks_b[-2]:
            return 1
        return -1
    if ranks_a[-1] > ranks_b[-1]:
        return 1
    return -1


# there cannot be 2 flushes of different suits at the same time and all 5 cards have to be of same suit
def flush(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    ranks_a.sort(reverse=True)
    ranks_b.sort(reverse=True)
    for x, y in zip(ranks_a, ranks_b):
        if x > y:
            return 1
        elif x < y:
            return -1
    return 0


def full_house(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    counts_a = Counter(ranks_a)
    counts_b = Counter(ranks_b)
    # x full of y
    a_major, b_major = counts_a.most_common(1)[0], counts_b.most_common(1)[0]
    if a_major > b_major:
        return 1
    elif a_major < b_major:
        return -1
    return compare(counts_a.most_common(2)[1][0], counts_b.most_common(2)[1][0])


def four_of_a_kind(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = [card.value for card in hand_a.cards]
    ranks_b = [card.value for card in hand_b.cards]
    counts_a = Counter(ranks_a)
    counts_b = Counter(ranks_b)
    a_major, b_major = counts_a.most_common(1)[0], counts_b.most_common(1)[0]
    if a_major > b_major:
        return 1
    elif a_major < b_major:
        return -1
    return compare(counts_a.most_common(2)[1][0], counts_b.most_common(2)[1][0])


# only needs to check which straight is higher
def straight_flush(hand_a: Hand, hand_b: Hand) -> int:
    ranks_a = sorted([card.value for card in hand_a.cards])
    ranks_b = sorted([card.value for card in hand_b.cards])
    # adjustments for 5-high straight flushes
    if ranks_a[-1] == 14 and ranks_a[-2] == 5:
        ranks_a = [1] + ranks_a[:-1]
    if ranks_b[-1] == 14 and ranks_b[-2] == 5:
        ranks_b = [1] + ranks_b[:-1]
    for x, y in zip(reversed(ranks_a), reversed(ranks_b)):
        if x > y:
            return 1
        elif x < y:
            return -1
    return 0


def hands_comparer(a, b: Hand, rank: Rank) -> Hand:
    empty_hand = Hand([])
    hands = [empty_hand, a, b]
    match rank:
        case Rank.HIGH_CARD:
            return hands[high_card(a, b)]
        case Rank.ONE_PAIR:
            return hands[one_pair(a, b)]
        case Rank.TWO_PAIRS:
            return hands[two_pairs(a, b)]
        case Rank.THREE_OF_A_KIND:
            return hands[three_of_a_kind(a, b)]
        case Rank.STRAIGHT:
            return hands[straight(a, b)]
        case Rank.FLUSH:
            return hands[flush(a, b)]
        case Rank.FULL_HOUSE:
            return hands[full_house(a, b)]
        case Rank.FOUR_OF_A_KIND:
            return hands[four_of_a_kind(a, b)]
        case Rank.STRAIGHT_FLUSH:
            return hands[straight_flush(a, b)]
    return empty_hand
