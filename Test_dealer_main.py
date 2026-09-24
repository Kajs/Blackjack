import unittest
from unittest.mock import Mock, patch

import Dealer_main


class TestDealerMain(unittest.TestCase):

    def createQueues(self):
        guiQueue = Mock()
        actionQueue = Mock()
        return guiQueue, actionQueue

    # ---------------------------------------------------------
    # takeDealerTurn
    # ---------------------------------------------------------

    @patch("Dealer_main.time.sleep")
    @patch("Dealer_main.getHandTotal", return_value=18)
    @patch("Dealer_main.getHandInfo", return_value="Dealer hand")
    @patch("Dealer_main.updatePlayerBoard")
    def test_dealer_stands(
        self,
        mock_update_player_board,
        mock_get_hand_info,
        mock_get_hand_total,
        mock_sleep
    ):
        guiQueue, actionQueue = self.createQueues()

        actionQueue.get.return_value = "stand"

        deck = ["5H"]
        dealerHand = ["10S", "8C"]
        playerHand = ["10D", "7H"]

        result = Dealer_main.takeDealerTurn(
            guiQueue,
            actionQueue,
            deck,
            dealerHand,
            playerHand
        )

        self.assertTrue(result)

        guiQueue.put.assert_any_call({
            "type": "UPDATE_HAND",
            "handType": "DEALER",
            "hand": dealerHand
        })

        guiQueue.put.assert_any_call({
            "type": "REQUEST_ACTION"
        })

        actionQueue.get.assert_called_once()

    @patch("Dealer_main.time.sleep")
    @patch("Dealer_main.getHandInfo", return_value="Dealer hand")
    @patch("Dealer_main.takeHitAction", return_value=20)
    @patch("Dealer_main.updatePlayerBoard")
    def test_dealer_hits_then_stands(
        self,
        mock_update_player_board,
        mock_take_hit_action,
        mock_get_hand_info,
        mock_sleep
    ):
        guiQueue, actionQueue = self.createQueues()

        actionQueue.get.side_effect = [
            "hit",
            "stand"
        ]

        deck = ["2H"]
        dealerHand = ["10S", "8C"]
        playerHand = ["10D", "7H"]

        result = Dealer_main.takeDealerTurn(
            guiQueue,
            actionQueue,
            deck,
            dealerHand,
            playerHand
        )

        self.assertTrue(result)

        mock_take_hit_action.assert_called_once_with(
            deck,
            dealerHand
        )

        self.assertEqual(
            actionQueue.get.call_count,
            2
        )

        calls = guiQueue.put.call_args_list

        self.assertEqual(
            calls[0].args[0],
            {
                "type": "UPDATE_HAND",
                "handType": "DEALER",
                "hand": dealerHand
            }
        )

        self.assertEqual(
            calls[1].args[0],
            {
                "type": "REQUEST_ACTION"
            }
        )

        self.assertEqual(
            calls[2].args[0],
            {
                "type": "UPDATE_HAND",
                "handType": "DEALER",
                "hand": dealerHand
            }
        )

        self.assertEqual(
            calls[3].args[0],
            {
                "type": "REQUEST_ACTION"
            }
        )

    @patch("Dealer_main.time.sleep")
    @patch("Dealer_main.getHandInfo", return_value="Dealer hand")
    @patch("Dealer_main.updatePlayerBoard")
    def test_dealer_hits_then_stands_with_real_hit(
        self,
        mock_update_player_board,
        mock_get_hand_info,
        mock_sleep
    ):
        guiQueue, actionQueue = self.createQueues()

        actionQueue.get.side_effect = [
            "hit",
            "stand"
        ]

        deck = ["2H"]
        dealerHand = ["10S", "8C"]
        playerHand = ["10D", "7H"]

        result = Dealer_main.takeDealerTurn(
            guiQueue,
            actionQueue,
            deck,
            dealerHand,
            playerHand
        )

        self.assertTrue(result)

        # takeHitAction should have drawn the 2H
        self.assertEqual(
            dealerHand,
            ["10S", "8C", "2H"]
        )

        self.assertEqual(
            deck,
            []
        )

        # The resulting hand should have a total of 20
        self.assertEqual(
            Dealer_main.getHandTotal(dealerHand),
            20
        )

        # Dealer chose hit and then stand
        self.assertEqual(
            actionQueue.get.call_count,
            2
        )

        self.assertEqual(
            guiQueue.put.call_count,
            4
        )

    @patch("Dealer_main.time.sleep")
    @patch("Dealer_main.getHandTotal", return_value=23)
    @patch("Dealer_main.getHandInfo", return_value="Dealer hand")
    @patch("Dealer_main.updatePlayerBoard")
    def test_dealer_busts_after_hit(
        self,
        mock_update_player_board,
        mock_get_hand_info,
        mock_get_hand_total,
        mock_sleep
    ):
        guiQueue, actionQueue = self.createQueues()

        actionQueue.get.return_value = "hit"

        deck = ["5H"]
        dealerHand = ["10S", "8C"]
        playerHand = ["10D", "7H"]

        with patch(
            "Dealer_main.takeHitAction",
            return_value=23
        ) as mock_take_hit:

            result = Dealer_main.takeDealerTurn(
                guiQueue,
                actionQueue,
                deck,
                dealerHand,
                playerHand
            )

        self.assertTrue(result)

        mock_take_hit.assert_called_once()
        mock_sleep.assert_called_once_with(1)

    def test_dealer_quit_toggle(self):
        guiQueue, actionQueue = self.createQueues()

        # First quit activates the exit request.
        # Second action is stand, so the turn ends.
        actionQueue.get.side_effect = [
            "quit",
            "stand"
        ]

        with patch("Dealer_main.getHandTotal", return_value=18), \
             patch("Dealer_main.getHandInfo", return_value="Dealer hand"), \
             patch("Dealer_main.updatePlayerBoard"), \
             patch("Dealer_main.time.sleep"):

            result = Dealer_main.takeDealerTurn(
                guiQueue,
                actionQueue,
                ["5H"],
                ["10S", "8C"],
                ["10D", "7H"]
            )

        self.assertFalse(result)

    # ---------------------------------------------------------
    # takePlayerTurn
    # ---------------------------------------------------------

    @patch("Dealer_main.time.sleep")
    @patch("Dealer_main.getHandTotal", return_value=17)
    @patch("Dealer_main.getHandInfo", return_value="Player hand")
    @patch("Dealer_main.updatePlayerBoard")
    def test_player_stands(
        self,
        mock_update_player_board,
        mock_get_hand_info,
        mock_get_hand_total,
        mock_sleep
    ):
        guiQueue, _ = self.createQueues()

        with patch(
            "Dealer_main.requestAction",
            return_value="ACTION: STAND"
        ) as mock_request:

            result = Dealer_main.takePlayerTurn(
                guiQueue,
                1,
                ["5H"],
                ["10D", "7H"],
                ["10S", "8C"]
            )

        self.assertTrue(result)

        mock_request.assert_called_once_with(1)

    @patch("Dealer_main.time.sleep")
    @patch("Dealer_main.getHandTotal", return_value=17)
    @patch("Dealer_main.getHandInfo", return_value="Player hand")
    @patch("Dealer_main.updatePlayerBoard")
    def test_player_hits(
        self,
        mock_update_player_board,
        mock_get_hand_info,
        mock_get_hand_total,
        mock_sleep
    ):
        guiQueue, _ = self.createQueues()

        playerHand = ["10D", "7H"]
        deck = ["3C"]

        with patch(
            "Dealer_main.requestAction",
            side_effect=[
                "ACTION: HIT",
                "ACTION: STAND"
            ]
        ):

            with patch(
                "Dealer_main.drawCard",
                return_value="3C"
            ) as mock_draw:

                result = Dealer_main.takePlayerTurn(
                    guiQueue,
                    1,
                    deck,
                    playerHand,
                    ["10S", "8C"]
                )

        self.assertTrue(result)

        mock_draw.assert_called_once_with(
            deck
        )

        self.assertEqual(
            playerHand,
            ["10D", "7H", "3C"]
        )

    @patch("Dealer_main.time.sleep")
    @patch("Dealer_main.getHandTotal", return_value=17)
    @patch("Dealer_main.getHandInfo", return_value="Player hand")
    @patch("Dealer_main.updatePlayerBoard")
    def test_player_quit_toggle(
        self,
        mock_update_player_board,
        mock_get_hand_info,
        mock_get_hand_total,
        mock_sleep
    ):
        guiQueue, _ = self.createQueues()

        with patch(
            "Dealer_main.requestAction",
            side_effect=[
                "ACTION: QUIT",
                "ACTION: STAND"
            ]
        ):

            result = Dealer_main.takePlayerTurn(
                guiQueue,
                1,
                ["5H"],
                ["10D", "7H"],
                ["10S", "8C"]
            )

        self.assertFalse(result)

    # ---------------------------------------------------------
    # removeExitingPlayers
    # ---------------------------------------------------------

    @patch("Dealer_main.closeConnection")
    @patch("Dealer_main.requestClose")
    def test_remove_exiting_player(
        self,
        mock_request_close,
        mock_close_connection
    ):
        exitingPlayers = [1]
        activePlayers = [1]

        Dealer_main.removeExitingPlayers(
            exitingPlayers,
            activePlayers
        )

        mock_request_close.assert_called_once_with(1)
        mock_close_connection.assert_called_once_with(1)

        self.assertEqual(activePlayers, [])
        self.assertEqual(exitingPlayers, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)