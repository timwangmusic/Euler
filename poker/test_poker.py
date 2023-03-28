import unittest

from poker import calculate_rank
from hands import hands_comparer, Card, Hand
from rank import Rank


class RankCalculationTests(unittest.TestCase):
    def test_rank_calculations(self):
        test_cases = {
            # high card
            Rank.HIGH_CARD: Hand([Card(10, 'D'), Card(11, 'D'), Card(12, 'D'), Card(5, 'S'), Card(14, 'H')]),

            # one pair
            Rank.ONE_PAIR: Hand([Card(10, 'H'), Card(11, 'D'), Card(
                12, 'S'), Card(14, 'H'), Card(14, 'S')]),

            # two pairs
            Rank.TWO_PAIRS: Hand([Card(10, 'H'), Card(10, 'D'), Card(
                8, 'S'), Card(8, 'C'), Card(14, 'D')]),

            # three of a kind
            Rank.THREE_OF_A_KIND: Hand([Card(5, 'H'), Card(5, 'D'), Card(
                5, 'S'), Card(10, 'C'), Card(14, 'H')]),

            # straight (wheel)
            Rank.STRAIGHT: Hand([Card(14, 'H'), Card(2, 'D'), Card(
                3, '3'), Card(4, 'S'), Card(5, 'D')]),

            # king-high flush
            Rank.FLUSH: Hand([Card(5, 'S'), Card(10, 'S'), Card(
                11, 'S'), Card(12, 'S'), Card(13, 'S')]),

            # full house
            Rank.FULL_HOUSE: Hand([Card(5, 'H'), Card(5, 'D'), Card(
                5, 'S'), Card(10, 'C'), Card(10, 'H')]),
            # four of a kind
            Rank.FOUR_OF_A_KIND: Hand([Card(5, 'H'), Card(5, 'D'), Card(
                5, 'S'), Card(5, 'C'), Card(3, 'H')]),
            # straight flush
            Rank.STRAIGHT_FLUSH: Hand([Card(5, 'H'), Card(4, 'H'), Card(
                1, 'H'), Card(2, 'H'), Card(3, 'H')])
        }
        for rank, hand in test_cases.items():
            self.assertEqual(calculate_rank(hand), rank)


class HandsComparerTests(unittest.TestCase):
    def test_high_card_return_hand_with_king_high(self):
        king_high = Hand([Card(13, 'S'), Card(12, 'D'), Card(10, 'S'), Card(8, 'H'), Card(5, 'H')])
        queen_high = Hand([Card(12, 'S'), Card(11, 'D'), Card(10, 'S'), Card(8, 'H'), Card(5, 'H')])
        self.assertEqual(hands_comparer(king_high, queen_high, Rank.HIGH_CARD), king_high)

    def test_one_pair_return_hand_with_pair_of_queens(self):
        pair_of_queens = Hand([Card(12, 'S'), Card(12, 'D'), Card(10, 'S'), Card(8, 'H'), Card(5, 'H')])
        pair_of_eights = Hand([Card(8, 'S'), Card(8, 'H'), Card(10, 'S'), Card(12, 'S'), Card(5, 'H')])
        self.assertEqual(hands_comparer(pair_of_queens, pair_of_eights, Rank.ONE_PAIR), pair_of_queens)

    def test_one_pair_return_hand_with_pair_of_stronger_kicker(self):
        pair_of_queens = Hand([Card(12, 'S'), Card(12, 'D'), Card(10, 'S'), Card(8, 'H'), Card(5, 'H')])
        pair_of_queens_weaker_kicker = Hand([Card(12, 'S'), Card(12, 'D'), Card(10, 'S'), Card(6, 'H'), Card(5, 'H')])
        self.assertEqual(hands_comparer(pair_of_queens, pair_of_queens_weaker_kicker, Rank.ONE_PAIR), pair_of_queens)

    def test_two_pairs_return_hand_with_higher_two_pairs(self):
        jacks_and_threes = Hand([Card(11, 'S'), Card(11, 'D'), Card(3, 'S'), Card(3, 'H'), Card(2, 'D')])
        tens_and_fives = Hand([Card(10, 'S'), Card(10, 'D'), Card(5, 'S'), Card(5, 'H'), Card(2, 'S')])
        self.assertEqual(hands_comparer(jacks_and_threes, tens_and_fives, Rank.TWO_PAIRS), jacks_and_threes)

    def test_three_of_a_kind_kicker_matters(self):
        jacks_ace_king = Hand([Card(11, 'S'), Card(11, 'H'), Card(11, 'D'), Card(14, 'C'), Card(13, 'C')])
        jacks_ace_queen = Hand([Card(11, 'S'), Card(11, 'H'), Card(11, 'D'), Card(14, 'C'), Card(12, 'C')])
        self.assertEqual(hands_comparer(jacks_ace_queen, jacks_ace_king, Rank.THREE_OF_A_KIND), jacks_ace_king)

    def test_three_of_a_kind_trips_kings_over_trips_queens(self):
        trips_queens = Hand([Card(12, 'S'), Card(12, 'H'), Card(12, 'D'), Card(10, 'C'), Card(9, 'C')])
        trips_kings = Hand([Card(13, 'S'), Card(13, 'H'), Card(13, 'D'), Card(14, 'C'), Card(5, 'C')])
        self.assertEqual(hands_comparer(trips_kings, trips_queens, Rank.THREE_OF_A_KIND), trips_kings)

    def test_straight_wheel_loses_to_nuts_straight(self):
        wheel = Hand([Card(14, 'S'), Card(2, 'D'), Card(3, 'S'), Card(4, 'D'), Card(5, 'H')])
        nuts_straight = Hand([Card(14, 'S'), Card(13, 'D'), Card(12, 'S'), Card(11, 'D'), Card(10, 'H')])
        self.assertEqual(hands_comparer(wheel, nuts_straight, Rank.STRAIGHT), nuts_straight)

    def test_flush_king_high_flush_loses_to_nuts_flush(self):
        nuts_flush = Hand([Card(14, 'S'), Card(10, 'S'), Card(9, 'S'), Card(7, 'S'), Card(6, 'S')])
        king_high_flush = Hand([Card(13, 'S'), Card(12, 'S'), Card(9, 'S'), Card(7, 'S'), Card(6, 'S')])
        self.assertEqual(hands_comparer(nuts_flush, king_high_flush, Rank.FLUSH), nuts_flush)

    def test_full_house_kings_full_over_tens_full(self):
        kings_full = Hand([Card(13, 'S'), Card(13, 'C'), Card(13, 'D'), Card(10, 'H'), Card(10, 'S')])
        tens_full = Hand([Card(10, 'H'), Card(10, 'S'), Card(10, 'D'), Card(13, 'C'), Card(10, 'S')])
        self.assertEqual(hands_comparer(kings_full, tens_full, Rank.FULL_HOUSE), kings_full)

    def test_full_house_aces_full_of_sixes_loses_to_aces_full_of_nines(self):
        aces_full_of_sixes = Hand([Card(14, 'S'), Card(14, 'C'), Card(14, 'D'), Card(6, 'H'), Card(6, 'S')])
        aces_full_of_nines = Hand([Card(14, 'S'), Card(14, 'C'), Card(14, 'D'), Card(9, 'H'), Card(9, 'S')])
        self.assertEqual(hands_comparer(aces_full_of_nines, aces_full_of_sixes, Rank.FULL_HOUSE), aces_full_of_nines)

    def test_four_of_a_kind_four_aces_over_four_deuces(self):
        four_aces = Hand([Card(14, 'S'), Card(14, 'C'), Card(14, 'H'), Card(14, 'D'), Card(10, 'S')])
        four_deuces = Hand([Card(2, 'S'), Card(2, 'C'), Card(2, 'H'), Card(2, 'D'), Card(10, 'S')])
        self.assertEqual(hands_comparer(four_deuces, four_aces, Rank.FOUR_OF_A_KIND), four_aces)

    # this is possible when all four kings are on the board
    def test_four_of_a_kind_kicker_problem(self):
        four_kings_with_ace = Hand([Card(13, 'S'), Card(13, 'C'), Card(13, 'H'), Card(13, 'D'), Card(14, 'S')])
        four_kings_with_ten = Hand([Card(13, 'S'), Card(13, 'C'), Card(13, 'H'), Card(13, 'D'), Card(10, 'S')])
        self.assertEqual(hands_comparer(four_kings_with_ten, four_kings_with_ace, Rank.FOUR_OF_A_KIND),
                         four_kings_with_ace)

    def test_straight_flush(self):
        five_high_straight_flush = Hand([Card(14, 'S'), Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S')])
        six_high_straight_flush = Hand([Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'), Card(6, 'S')])
        self.assertEqual(hands_comparer(five_high_straight_flush, six_high_straight_flush, Rank.STRAIGHT_FLUSH),
                         six_high_straight_flush)


if __name__ == '__main__':
    unittest.main()
