"""Euler problem #54 https://projecteuler.net/problem=54"""
from collections import Counter

from utils import is_arithmetic_progression
from rank import Rank
from hands import hands_comparer, Card, Hand
from pprint import pprint as pp


class PokerHandComparer:
    @classmethod
    def print_hand(cls, hand: Hand) -> str:
        suit_unicode = {
            'S': '\u2664',
            'C': '\u2662',
            'H': '\u2661',
            'D': '\u2662',
        }
        result = ", ".join(str(card.value) + suit_unicode[card.suit] for card in hand.cards)
        return f"hand: {result} wins"

    @classmethod
    def show_result(cls, hand: Hand, rank: Rank) -> None:
        pp(f"{cls.print_hand(hand)} with rank {rank}!")

    @classmethod
    def compare(cls, hand_a, hand_b: Hand) -> None:
        rank_a = calculate_rank(hand_a)
        rank_b = calculate_rank(hand_b)
        if rank_a < rank_b:
            cls.show_result(hand_b, rank_b)
        elif rank_b < rank_a:
            cls.show_result(hand_a, rank_a)
        cls.show_result(hands_comparer(hand_a, hand_b, rank_a), rank_a)

    @classmethod
    def is_card_valid(cls, card: Card) -> bool:
        return 2 <= card.value <= 14 and str(card.suit).upper() in {'S', 'C', 'H', 'D'}

    @classmethod
    def is_hand_valid(cls, hand: Hand) -> bool:
        if len(hand.cards) != 5:
            return False

        # all cards have to be different
        seen = set()
        for card in hand.cards:
            if card in seen:
                return False
            seen.add(card)

        return True

    @classmethod
    def main(cls):
        while True:
            pp("please enter the first hand")
            cards_a = []
            skip_second_hand = False
            for s in ["first", "second", "third", "fourth", "fifth"]:
                pp(f"enter {s} card:")
                rank = int(input("rank:"))
                suit = input("suit:")
                card = Card(rank, suit)
                if not cls.is_card_valid(card):
                    skip_second_hand = True
                    break
                cards_a.append(card)

            if skip_second_hand:
                pp("first hand input error, skipping second hand input...")
                continue

            if not cls.is_hand_valid(Hand(cards_a)):
                pp("invalid first hand, skipping second hand input...")
                continue

            pp("please enter the second hand")
            cards_b = []
            skip_comparison = False
            for s in ["first", "second", "third", "fourth", "fifth"]:
                pp(f"enter {s} card:")
                rank = int(input("rank:"))
                suit = input("suit:").upper()
                card = Card(rank, suit)
                if not cls.is_card_valid(card):
                    skip_comparison = True
                    break
                cards_b.append(card)

            if skip_comparison:
                pp("second hand input error")
                continue

            if not cls.is_hand_valid(Hand(cards_b)):
                pp("invalid second hand")
                continue

            cls.compare(Hand(cards_a), Hand(cards_b))


def calculate_rank(hand: Hand) -> Rank:
    """calculates rank of the hand"""
    # first we determine if the hand has pairs, trips or quads
    value_counter = Counter()
    for card in hand.cards:
        value_counter[card.value] += 1

    rank = Rank.HIGH_CARD
    if len(value_counter) == 2:
        if value_counter.most_common(1)[0][1] == 4:
            rank = Rank.FOUR_OF_A_KIND
        else:
            rank = Rank.FULL_HOUSE
    if len(value_counter) == 3:
        items = value_counter.most_common(3)
        if items[0][1] == items[1][1]:
            rank = Rank.TWO_PAIRS
        else:
            rank = Rank.THREE_OF_A_KIND
    if len(value_counter) == 4:
        rank = Rank.ONE_PAIR

    rank = check_straights_and_flushes(rank, hand)
    return rank


def check_straights_and_flushes(rank: Rank, hand: Hand) -> Rank:
    """straights and flushes require all cards have different values"""
    suit_counter = Counter()
    for card in hand.cards:
        suit_counter[card.suit] += 1
    if len(suit_counter) == 1:
        rank = Rank.FLUSH

    values = [card.value for card in hand.cards]
    values.sort()
    # handles the case of wheel
    if is_arithmetic_progression(values, 1) or (values == [2, 3, 4, 5, 14]):
        if rank == Rank.FLUSH:
            rank = Rank.STRAIGHT_FLUSH
        else:
            rank = Rank.STRAIGHT
    return rank


if __name__ == "__main__":
    PokerHandComparer.main()
