import unittest
from unittest.mock import Mock, patch

import Player_gui


class TestPlayerGUI(unittest.TestCase):

    def setUp(self):
        Player_gui.dealerHand = []
        Player_gui.myHand = []
        Player_gui.hit_button = None
        Player_gui.stand_button = None
        Player_gui.exit_button = None

    # ---------------------------------------------------------
    # getPlayerAction
    # ---------------------------------------------------------

    @patch("Player_gui.pygame.event.clear")
    @patch("Player_gui.updateScreen")
    @patch("Player_gui.pygame.event.get")
    def test_get_player_action_hit(
        self,
        mock_event_get,
        mock_update_screen,
        mock_event_clear
    ):
        Player_gui.hit_button = Mock()
        Player_gui.stand_button = Mock()
        Player_gui.exit_button = Mock()

        Player_gui.hit_button.collidepoint.return_value = True

        event = Mock()
        event.type = Player_gui.pygame.MOUSEBUTTONDOWN
        event.pos = (100, 100)

        mock_event_get.return_value = [event]

        result = Player_gui.getPlayerAction(
            ["FD", "5S"],
            ["8C", "AH"]
        )

        self.assertEqual(result, "HIT")

        Player_gui.hit_button.collidepoint.assert_called_once_with(
            event.pos
        )

        mock_event_clear.assert_called_once_with(
            Player_gui.pygame.MOUSEBUTTONDOWN
        )

    @patch("Player_gui.pygame.event.clear")
    @patch("Player_gui.updateScreen")
    @patch("Player_gui.pygame.event.get")
    def test_get_player_action_stand(
        self,
        mock_event_get,
        mock_update_screen,
        mock_event_clear
    ):
        Player_gui.hit_button = Mock()
        Player_gui.stand_button = Mock()
        Player_gui.exit_button = Mock()

        Player_gui.hit_button.collidepoint.return_value = False
        Player_gui.stand_button.collidepoint.return_value = True

        event = Mock()
        event.type = Player_gui.pygame.MOUSEBUTTONDOWN
        event.pos = (100, 100)

        mock_event_get.return_value = [event]

        result = Player_gui.getPlayerAction(
            ["FD", "5S"],
            ["8C", "AH"]
        )

        self.assertEqual(result, "STAND")

        Player_gui.stand_button.collidepoint.assert_called_once_with(
            event.pos
        )

        mock_event_clear.assert_called_once_with(
            Player_gui.pygame.MOUSEBUTTONDOWN
        )

    @patch("Player_gui.pygame.event.clear")
    @patch("Player_gui.updateScreen")
    @patch("Player_gui.pygame.event.get")
    def test_get_player_action_quit(
        self,
        mock_event_get,
        mock_update_screen,
        mock_event_clear
    ):
        event = Mock()
        event.type = Player_gui.pygame.QUIT

        mock_event_get.return_value = [event]

        result = Player_gui.getPlayerAction(
            ["FD", "5S"],
            ["8C", "AH"]
        )

        self.assertEqual(result, "QUIT")

        mock_event_clear.assert_called_once_with(
            Player_gui.pygame.MOUSEBUTTONDOWN
        )

    # ---------------------------------------------------------
    # startGameWindow message handling
    # ---------------------------------------------------------

    @patch("Player_gui.pygame.quit")
    @patch("Player_gui.closeGameWindow")
    @patch("Player_gui.updateScreen")
    @patch("Player_gui.pygame.display.set_caption")
    @patch("Player_gui.pygame.display.set_mode")
    @patch("Player_gui.pygame.init")
    def test_update_dealer_hand(
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

        Player_gui.startGameWindow(
            guiQueue,
            actionQueue,
            400,
            500,
            60,
            "Blackjack - PLAYER1"
        )

        self.assertEqual(
            Player_gui.dealerHand,
            ["FD", "5S"]
        )

    @patch("Player_gui.pygame.quit")
    @patch("Player_gui.closeGameWindow")
    @patch("Player_gui.updateScreen")
    @patch("Player_gui.pygame.display.set_caption")
    @patch("Player_gui.pygame.display.set_mode")
    @patch("Player_gui.pygame.init")
    def test_update_player_hand(
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
                "handType": "MYHAND",
                "hand": ["8C", "AH"]
            },
            {
                "type": "CLOSE_GUI"
            }
        ]

        Player_gui.startGameWindow(
            guiQueue,
            actionQueue,
            400,
            500,
            60,
            "Blackjack - PLAYER1"
        )

        self.assertEqual(
            Player_gui.myHand,
            ["8C", "AH"]
        )

    @patch("Player_gui.getPlayerAction", return_value="HIT")
    @patch("Player_gui.pygame.quit")
    @patch("Player_gui.closeGameWindow")
    @patch("Player_gui.updateScreen")
    @patch("Player_gui.pygame.display.set_caption")
    @patch("Player_gui.pygame.display.set_mode")
    @patch("Player_gui.pygame.init")
    def test_request_action_returns_action_to_queue(
        self,
        mock_init,
        mock_set_mode,
        mock_set_caption,
        mock_update_screen,
        mock_close_game,
        mock_pygame_quit,
        mock_get_player_action
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

        Player_gui.startGameWindow(
            guiQueue,
            actionQueue,
            400,
            500,
            60,
            "Blackjack - PLAYER1"
        )

        mock_get_player_action.assert_called_once_with(
            Player_gui.dealerHand,
            Player_gui.myHand
        )

        actionQueue.put.assert_called_once_with(
            "HIT"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)