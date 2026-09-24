import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
from collections import Counter

import Dealer_game


class TestDealerGame(unittest.TestCase):

    # ---------------------------------------------------------
    # getDeck / drawCard
    # ---------------------------------------------------------

    def test_get_deck(self):
        deck = Dealer_game.getDeck()

        self.assertEqual(len(deck), 52)
        self.assertEqual(len(set(deck)), 52)

        for card in Dealer_game.Cards:
            self.assertIn(card, deck)

    def test_draw_card(self):
        deck = ["AC", "5S", "KH"]

        card = Dealer_game.drawCard(deck)

        self.assertEqual(card, "AC")
        self.assertEqual(deck, ["5S", "KH"])

    # ---------------------------------------------------------
    # getCardValue
    # ---------------------------------------------------------

    def test_get_card_value(self):
        test_cases = [
            ("AC", (1, 11)),
            ("7S", (7, 7)),
            ("10H", (10, 10)),
            ("JC", (10, 10)),
            ("QD", (10, 10)),
            ("KS", (10, 10)),
        ]

        for card, expected_value in test_cases:
            with self.subTest(card=card):
                self.assertEqual(
                    Dealer_game.getCardValue(card),
                    expected_value
                )

    def test_get_card_value_invalid_card(self):
        output = StringIO()

        with redirect_stdout(output):
            result = Dealer_game.getCardValue("XX")

        self.assertIsNone(result)
        self.assertIn(
            "getCardValue didn't find a match for: XX",
            output.getvalue()
        )

    # ---------------------------------------------------------
    # Hand information / formatting
    # ---------------------------------------------------------

    def test_hand_to_string(self):
        hand = ["7S", "AC", "10H"]

        result = Dealer_game.handToString(hand)

        self.assertEqual(result, "7S,AC,10H")

    def test_hand_to_string_empty_hand(self):
        self.assertEqual(
            Dealer_game.handToString([]),
            ""
        )

    def test_get_facedown_hand(self):
        hand = ["AS", "KH"]

        result = Dealer_game.getFacedownHand(hand)

        self.assertEqual(result, ["FD", "KH"])

        # Make sure the original hand was not changed
        self.assertEqual(hand, ["AS", "KH"])

    def test_get_hand_info(self):
        hand = ["AS", "9H"]

        result = Dealer_game.getHandInfo(hand)

        self.assertEqual(
            result,
            "Your hand is AS 9H with a total of: 20."
        )

    # ---------------------------------------------------------
    # getHandTotal
    # ---------------------------------------------------------

    def test_get_hand_total(self):
        test_cases = [
            ([], 0),
            (["5H"], 5),
            (["10H", "7S"], 17),

            # One ace
            (["AS", "9H"], 20),
            (["AS", "9H", "5C"], 15),

            # Two aces
            (["AS", "AD"], 12),
            (["AS", "AD", "9C"], 21),
            (["AS", "AD", "9C", "5D"], 16),

            # Three aces
            (["AS", "AD", "AH"], 13),
            (["AS", "AD", "AH", "8C"], 21),

            # Four aces
            (["AS", "AD", "AH", "AC"], 14),

            # Blackjack
            (["AS", "KS"], 21),

            # Ace must become 1
            (["AS", "KS", "5D"], 16),
            (["AS", "2H", "3C"], 16),
        ]

        for hand, expected_total in test_cases:
            with self.subTest(hand=hand):
                self.assertEqual(
                    Dealer_game.getHandTotal(hand),
                    expected_total
                )

    # ---------------------------------------------------------
    # resetGame / shuffleDeck
    # ---------------------------------------------------------

    def test_shuffle_deck_preserves_cards(self):
        deck = Dealer_game.getDeck()
        original_deck = deck.copy()

        Dealer_game.shuffleDeck(deck)

        self.assertEqual(
            Counter(deck),
            Counter(original_deck)
        )

    def test_reset_game_one_deck(self):
        shoe, discard_pile, dealer_hand, player_hand = (
            Dealer_game.resetGame(1)
        )

        self.assertEqual(len(shoe), 52)
        self.assertEqual(discard_pile, [])
        self.assertEqual(dealer_hand, [])
        self.assertEqual(player_hand, [])

    def test_reset_game_four_decks(self):
        shoe, discard_pile, dealer_hand, player_hand = (
            Dealer_game.resetGame(4)
        )

        self.assertEqual(len(shoe), 208)
        self.assertEqual(discard_pile, [])
        self.assertEqual(dealer_hand, [])
        self.assertEqual(player_hand, [])

        # Every card should occur exactly four times
        card_counts = Counter(shoe)

        for card in Dealer_game.Cards:
            with self.subTest(card=card):
                self.assertEqual(card_counts[card], 4)

    # ---------------------------------------------------------
    # dealCards / endRound / takeHitAction
    # ---------------------------------------------------------

    def test_deal_cards(self):
        deck = ["AC", "2C", "3C", "4C"]
        dealer_hand = []
        player_hand = []

        Dealer_game.dealCards(
            deck,
            dealer_hand,
            player_hand
        )

        self.assertEqual(player_hand, ["AC", "3C"])
        self.assertEqual(dealer_hand, ["2C", "4C"])
        self.assertEqual(deck, [])

    def test_end_round(self):
        discard_pile = []
        dealer_hand = ["KS", "7H"]
        player_hand = ["AC", "9D"]

        Dealer_game.endRound(
            discard_pile,
            dealer_hand,
            player_hand
        )

        self.assertEqual(
            discard_pile,
            ["AC", "9D", "KS", "7H"]
        )
        self.assertEqual(player_hand, [])
        self.assertEqual(dealer_hand, [])

    def test_take_hit_action(self):
        deck = ["5H"]
        hand = ["10S"]

        result = Dealer_game.takeHitAction(deck, hand)

        self.assertEqual(result, 15)
        self.assertEqual(hand, ["10S", "5H"])
        self.assertEqual(deck, [])

    # ---------------------------------------------------------
    # declareRoundWinner
    # ---------------------------------------------------------

    def assert_round_result(
        self,
        dealer_hand,
        player_hand,
        expected_text
    ):
        output = StringIO()

        # declareRoundWinner waits two seconds after printing.
        # We don't want our tests to actually wait two seconds.
        with patch("Dealer_game.time.sleep"):
            with redirect_stdout(output):
                Dealer_game.declareRoundWinner(
                    dealer_hand,
                    player_hand
                )

        self.assertIn(
            expected_text,
            output.getvalue()
        )

    def test_player_wins_when_player_under_21_and_dealer_busts(self):
        self.assert_round_result(
            dealer_hand=["10H", "8C", "5S"],
            player_hand=["10D", "9H"],
            expected_text="PLAYER has won this round."
        )

    def test_dealer_wins_when_dealer_under_21_and_player_busts(self):
        self.assert_round_result(
            dealer_hand=["10H", "8C"],
            player_hand=["10D", "9H", "5S"],
            expected_text="DEALER has won this round."
        )

    def test_player_wins_with_higher_total(self):
        self.assert_round_result(
            dealer_hand=["10H", "6C"],
            player_hand=["10D", "8H"],
            expected_text="PLAYER has won this round."
        )

    def test_dealer_wins_with_higher_total(self):
        self.assert_round_result(
            dealer_hand=["10H", "8C"],
            player_hand=["10D", "6H"],
            expected_text="DEALER has won this round."
        )

    def test_tie_when_totals_are_equal_under_21(self):
        self.assert_round_result(
            dealer_hand=["10H", "7C"],
            player_hand=["9D", "8H"],
            expected_text="player is tied with dealer"
        )

    def test_player_blackjack_beats_dealer_21_with_three_cards(self):
        self.assert_round_result(
            dealer_hand=["7H", "7C", "7D"],
            player_hand=["AS", "KH"],
            expected_text="PLAYER has won this round."
        )

    def test_dealer_blackjack_beats_player_21_with_three_cards(self):
        self.assert_round_result(
            dealer_hand=["AS", "KH"],
            player_hand=["7H", "7C", "7D"],
            expected_text="DEALER has won this round."
        )

    def test_player_blackjack_beats_dealer_bust(self):
        self.assert_round_result(
            dealer_hand=["10H", "8C", "5S"],
            player_hand=["AS", "KH"],
            expected_text="PLAYER has won this round."
        )

    def test_dealer_blackjack_beats_player_bust(self):
        self.assert_round_result(
            dealer_hand=["AS", "KH"],
            player_hand=["10D", "8H", "5C"],
            expected_text="DEALER has won this round."
        )

    def test_both_blackjack_is_a_tie(self):
        self.assert_round_result(
            dealer_hand=["AS", "KH"],
            player_hand=["AD", "QC"],
            expected_text="player is tied with dealer"
        )

    def test_both_bust_is_a_tie(self):
        self.assert_round_result(
            dealer_hand=["10H", "8C", "5S"],
            player_hand=["10D", "9H", "4C"],
            expected_text="player is tied with dealer"
        )

    def test_both_have_21_with_three_cards_is_a_tie(self):
        self.assert_round_result(
            dealer_hand=["7H", "7C", "7D"],
            player_hand=["6S", "7S", "8S"],
            expected_text="player is tied with dealer"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)