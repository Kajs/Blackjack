import unittest
from unittest.mock import Mock, patch

import Dealer_gui


class TestDealerGUI(unittest.TestCase):

    def setUp(self):
        Dealer_gui.dealerHand = []
        Dealer_gui.playerHand = []
        Dealer_gui.hit_button = None
        Dealer_gui.stand_button = None
        Dealer_gui.exit_button = None

    # ---------------------------------------------------------
    # getDealerAction
    # ---------------------------------------------------------

    @patch("Dealer_gui.pygame.event.clear")
    @patch("Dealer_gui.updateScreen")
    @patch("Dealer_gui.pygame.event.get")
    def test_get_dealer_action_hit(
        self,
        mock_event_get,
        mock_update_screen,
        mock_event_clear
    ):
        Dealer_gui.hit_button = Mock()
        Dealer_gui.stand_button = Mock()
        Dealer_gui.exit_button = Mock()

        Dealer_gui.hit_button.collidepoint.return_value = True

        event = Mock()
        event.type = Dealer_gui.pygame.MOUSEBUTTONDOWN
        event.pos = (100, 100)

        mock_event_get.return_value = [event]

        result = Dealer_gui.getDealerAction(
            ["10S", "8C"],
            ["10D", "7H"]
        )

        self.assertEqual(result, "hit")

        Dealer_gui.hit_button.collidepoint.assert_called_once_with(
            event.pos
        )

    @patch("Dealer_gui.pygame.event.clear")
    @patch("Dealer_gui.updateScreen")
    @patch("Dealer_gui.pygame.event.get")
    def test_get_dealer_action_stand(
        self,
        mock_event_get,
        mock_update_screen,
        mock_event_clear
    ):
        Dealer_gui.hit_button = Mock()
        Dealer_gui.stand_button = Mock()
        Dealer_gui.exit_button = Mock()

        Dealer_gui.hit_button.collidepoint.return_value = False
        Dealer_gui.stand_button.collidepoint.return_value = True

        event = Mock()
        event.type = Dealer_gui.pygame.MOUSEBUTTONDOWN
        event.pos = (100, 100)

        mock_event_get.return_value = [event]

        result = Dealer_gui.getDealerAction(
            ["10S", "8C"],
            ["10D", "7H"]
        )

        self.assertEqual(result, "stand")

    @patch("Dealer_gui.pygame.event.clear")
    @patch("Dealer_gui.updateScreen")
    @patch("Dealer_gui.pygame.event.get")
    def test_get_dealer_action_quit(
        self,
        mock_event_get,
        mock_update_screen,
        mock_event_clear
    ):
        event = Mock()
        event.type = Dealer_gui.pygame.QUIT

        mock_event_get.return_value = [event]

        result = Dealer_gui.getDealerAction(
            ["10S", "8C"],
            ["10D", "7H"]
        )

        self.assertEqual(result, "quit")

    # ---------------------------------------------------------
    # startGameWindow message handling
    # ---------------------------------------------------------

    @patch("Dealer_gui.pygame.quit")
    @patch("Dealer_gui.closeGameWindow")
    @patch("Dealer_gui.updateScreen")
    @patch("Dealer_gui.pygame.display.set_caption")
    @patch("Dealer_gui.pygame.display.set_mode")
    @patch("Dealer_gui.pygame.init")
    def test_update_hand(
        self,
        mock_init,
        mock_set_mode,
        mock_set_caption,
        mock_update_screen,
        mock_close_game,
        mock_pygame_quit
    ):
        guiQueue = Mock()
        actionQueue = Mock()

        guiQueue.get_nowait.side_effect = [
            {
                "type": "UPDATE_HAND",
                "handType": "DEALER",
                "hand": ["FD", "5S"]
            },
            {
                "type": "CLOSE_GUI"
            }
        ]

        Dealer_gui.startGameWindow(
            guiQueue,
            actionQueue,
            400,
            500,
            60
        )

        self.assertEqual(
            Dealer_gui.dealerHand,
            ["FD", "5S"]
        )

    @patch("Dealer_gui.getDealerAction", return_value="hit")
    @patch("Dealer_gui.pygame.quit")
    @patch("Dealer_gui.closeGameWindow")
    @patch("Dealer_gui.updateScreen")
    @patch("Dealer_gui.pygame.display.set_caption")
    @patch("Dealer_gui.pygame.display.set_mode")
    @patch("Dealer_gui.pygame.init")
    def test_request_action_returns_action_to_queue(
        self,
        mock_init,
        mock_set_mode,
        mock_set_caption,
        mock_update_screen,
        mock_close_game,
        mock_pygame_quit,
        mock_get_dealer_action
    ):
        guiQueue = Mock()
        actionQueue = Mock()

        guiQueue.get_nowait.side_effect = [
            {
                "type": "REQUEST_ACTION"
            },
            {
                "type": "CLOSE_GUI"
            }
        ]

        Dealer_gui.startGameWindow(
            guiQueue,
            actionQueue,
            400,
            500,
            60
        )

        mock_get_dealer_action.assert_called_once_with(
            Dealer_gui.dealerHand,
            Dealer_gui.playerHand
        )

        actionQueue.put.assert_called_once_with(
            "hit"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)