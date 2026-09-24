import unittest
from unittest.mock import Mock, patch

import Player_main


class TestPlayerMain(unittest.TestCase):

    def setUp(self):
        # Reset global state before every test
        Player_main.myPlayerNumber = None
        Player_main.dealerHand = []
        Player_main.myHand = []

    def createQueues(self):
        guiQueue = Mock()
        actionQueue = Mock()
        return guiQueue, actionQueue

    # ---------------------------------------------------------
    # setMyPlayerNumber
    # ---------------------------------------------------------

    def test_set_player_number(self):
        Player_main.setMyPlayerNumber("1")

        self.assertEqual(
            Player_main.myPlayerNumber,
            1
        )

    def test_set_player_number_only_once(self):
        Player_main.setMyPlayerNumber("1")
        Player_main.setMyPlayerNumber("2")

        self.assertEqual(
            Player_main.myPlayerNumber,
            1
        )

    # ---------------------------------------------------------
    # YOURNUMBERIS
    # ---------------------------------------------------------

    def test_parse_player_number(self):
        guiQueue, actionQueue = self.createQueues()

        result = Player_main.parseMessage(
            "YOURNUMBERIS: 1\n",
            guiQueue,
            actionQueue
        )

        self.assertTrue(result)

        self.assertEqual(
            Player_main.myPlayerNumber,
            1
        )

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def test_parse_update(self):
        guiQueue, actionQueue = self.createQueues()

        Player_main.myPlayerNumber = 1

        message = (
            "UPDATE:DEALER:FD,5S;PLAYER1:8C,AH\n"
        )

        result = Player_main.parseMessage(
            message,
            guiQueue,
            actionQueue
        )

        self.assertTrue(result)

        self.assertEqual(
            Player_main.dealerHand,
            ["FD", "5S"]
        )

        self.assertEqual(
            Player_main.myHand,
            ["8C", "AH"]
        )

        self.assertEqual(
            guiQueue.put.call_count,
            2
        )

    def test_parse_update_sends_correct_gui_messages(self):
        guiQueue, actionQueue = self.createQueues()

        Player_main.myPlayerNumber = 1

        message = (
            "UPDATE:DEALER:FD,5S;PLAYER1:8C,AH\n"
        )

        Player_main.parseMessage(
            message,
            guiQueue,
            actionQueue
        )

        calls = guiQueue.put.call_args_list

        self.assertEqual(
            calls[0].args[0],
            {
                "type": "UPDATE_HAND",
                "handType": "DEALER",
                "hand": ["FD", "5S"]
            }
        )

        self.assertEqual(
            calls[1].args[0],
            {
                "type": "UPDATE_HAND",
                "handType": "MYHAND",
                "hand": ["8C", "AH"]
            }
        )

    # ---------------------------------------------------------
    # REQUEST: ACTION
    # ---------------------------------------------------------

    @patch("Player_main.sendMessage")
    def test_request_action_hit(self, mock_send_message):
        guiQueue, actionQueue = self.createQueues()

        actionQueue.get.return_value = "HIT"

        result = Player_main.parseMessage(
            "REQUEST: ACTION\n",
            guiQueue,
            actionQueue
        )

        self.assertTrue(result)

        guiQueue.put.assert_called_once_with(
            {"type": "REQUEST_ACTION"}
        )

        actionQueue.get.assert_called_once()

        mock_send_message.assert_called_once_with(
            "ACTION: HIT"
        )

    @patch("Player_main.sendMessage")
    def test_request_action_stand(self, mock_send_message):
        guiQueue, actionQueue = self.createQueues()

        actionQueue.get.return_value = "STAND"

        result = Player_main.parseMessage(
            "REQUEST: ACTION\n",
            guiQueue,
            actionQueue
        )

        self.assertTrue(result)

        guiQueue.put.assert_called_once_with(
            {"type": "REQUEST_ACTION"}
        )

        mock_send_message.assert_called_once_with(
            "ACTION: STAND"
        )

    @patch("Player_main.sendMessage")
    def test_request_action_quit(self, mock_send_message):
        guiQueue, actionQueue = self.createQueues()

        actionQueue.get.return_value = "QUIT"

        result = Player_main.parseMessage(
            "REQUEST: ACTION\n",
            guiQueue,
            actionQueue
        )

        self.assertTrue(result)

        guiQueue.put.assert_called_once_with(
            {"type": "REQUEST_ACTION"}
        )

        mock_send_message.assert_called_once_with(
            "ACTION: QUIT"
        )

    # ---------------------------------------------------------
    # REQUEST: CLOSE
    # ---------------------------------------------------------

    @patch("Player_main.closeClient")
    def test_request_close(self, mock_close_client):
        guiQueue, actionQueue = self.createQueues()

        result = Player_main.parseMessage(
            "REQUEST: CLOSE\n",
            guiQueue,
            actionQueue
        )

        self.assertFalse(result)

        guiQueue.put.assert_called_once_with(
            {"type": "CLOSE_GUI"}
        )

        mock_close_client.assert_called_once()

    # ---------------------------------------------------------
    # Multiple commands
    # ---------------------------------------------------------

    def test_multiple_commands(self):
        guiQueue, actionQueue = self.createQueues()

        message = (
            "YOURNUMBERIS: 1\n"
            "UPDATE:DEALER:FD,5S;PLAYER1:8C,AH\n"
        )

        result = Player_main.parseMessage(
            message,
            guiQueue,
            actionQueue
        )

        self.assertTrue(result)

        self.assertEqual(
            Player_main.myPlayerNumber,
            1
        )

        self.assertEqual(
            Player_main.dealerHand,
            ["FD", "5S"]
        )

        self.assertEqual(
            Player_main.myHand,
            ["8C", "AH"]
        )

        self.assertEqual(
            guiQueue.put.call_count,
            2
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)