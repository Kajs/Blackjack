import unittest
import threading
from unittest.mock import Mock

import Dealer_server
import Player_client


class TestDealerServer(unittest.TestCase):

    def setUp(self):
        Dealer_server.serverSocket = None
        Dealer_server.clients = {}
        Dealer_server.playerNumber = 0

    def test_player_number_to_name(self):
        self.assertEqual(
            Dealer_server.playerNumberToName(1),
            "PLAYER1"
        )

        self.assertEqual(
            Dealer_server.playerNumberToName(3),
            "PLAYER3"
        )

    def test_send_message(self):
        mockConnection = Mock()

        Dealer_server.clients[1] = (
            mockConnection,
            ("127.0.0.1", 12345)
        )

        Dealer_server.sendMessage(1, "REQUEST: ACTION\n")

        mockConnection.sendall.assert_called_once_with(
            b"REQUEST: ACTION\n"
        )

    def test_send_player_number(self):
        mockConnection = Mock()

        Dealer_server.clients[1] = (
            mockConnection,
            ("127.0.0.1", 12345)
        )

        Dealer_server.sendPlayerNumber(1)

        mockConnection.sendall.assert_called_once_with(
            b"YOURNUMBERIS: 1\n"
        )

    def test_update_player_board(self):
        mockConnection = Mock()

        Dealer_server.clients[1] = (
            mockConnection,
            ("127.0.0.1", 12345)
        )

        Dealer_server.updatePlayerBoard(
            1,
            "FD,5S",
            "8C,AH"
        )

        mockConnection.sendall.assert_called_once_with(
            b"UPDATE:DEALER:FD,5S;PLAYER1:8C,AH\n"
        )


class TestPlayerClient(unittest.TestCase):

    def setUp(self):
        Player_client.clientSocket = None

    def test_get_message(self):
        mockSocket = Mock()
        mockSocket.recv.return_value = b"REQUEST: ACTION\n"

        Player_client.clientSocket = mockSocket

        message = Player_client.getMessage()

        self.assertEqual(
            message,
            "REQUEST: ACTION\n"
        )

        mockSocket.recv.assert_called_once_with(1024)

    def test_send_message(self):
        mockSocket = Mock()

        Player_client.clientSocket = mockSocket

        Player_client.sendMessage("ACTION: HIT")

        mockSocket.sendall.assert_called_once_with(
            b"ACTION: HIT"
        )


class TestServerClientIntegration(unittest.TestCase):

    def setUp(self):
        # Make sure both modules start from a clean state.
        Dealer_server.serverSocket = None
        Dealer_server.clients = {}
        Dealer_server.playerNumber = 0

        Player_client.clientSocket = None

        # Port 0 means: let Windows choose an available port.
        Dealer_server.startServer("127.0.0.1", 0)

        self.port = Dealer_server.serverSocket.getsockname()[1]

    def tearDown(self):
        # Close the client if it is still open.
        if Player_client.clientSocket is not None:
            try:
                Player_client.clientSocket.close()
            except OSError:
                pass

        Player_client.clientSocket = None

        # Close any server-side client connections.
        for connection, address in Dealer_server.clients.values():
            try:
                connection.close()
            except OSError:
                pass

        Dealer_server.clients.clear()

        if Dealer_server.serverSocket is not None:
            try:
                Dealer_server.serverSocket.close()
            except OSError:
                pass

        Dealer_server.serverSocket = None
        Dealer_server.playerNumber = 0

    def connect_player(self):
        """
        Start acceptConnection in another thread because it blocks
        while waiting for the client to connect.
        """

        acceptThread = threading.Thread(
            target=Dealer_server.acceptConnection,
            daemon=True
        )

        acceptThread.start()

        Player_client.startClient(
            "127.0.0.1",
            self.port
        )

        acceptThread.join(timeout=2)

        self.assertFalse(
            acceptThread.is_alive(),
            "Server was still waiting for the client connection."
        )

    def test_client_can_connect_to_server(self):
        self.connect_player()

        message = Player_client.getMessage()

        self.assertEqual(
            message,
            "YOURNUMBERIS: 1\n"
        )

        self.assertIn(
            1,
            Dealer_server.clients
        )

    def test_server_and_client_can_exchange_messages(self):
        self.connect_player()

        # Consume the player number message.
        Player_client.getMessage()

        Dealer_server.sendMessage(
            1,
            "REQUEST: ACTION\n"
        )

        message = Player_client.getMessage()

        self.assertEqual(
            message,
            "REQUEST: ACTION\n"
        )

        Player_client.sendMessage(
            "ACTION: HIT"
        )

        message = Dealer_server.getMessage(1)

        self.assertEqual(
            message,
            "ACTION: HIT"
        )

    def test_request_action(self):
        self.connect_player()

        # Consume the player number message.
        Player_client.getMessage()

        result = {}

        def requestAction():
            result["action"] = Dealer_server.requestAction(1)

        requestThread = threading.Thread(
            target=requestAction,
            daemon=True
        )

        requestThread.start()

        # The server should now be waiting for the player's action.
        message = Player_client.getMessage()

        self.assertEqual(
            message,
            "REQUEST: ACTION\n"
        )

        Player_client.sendMessage(
            "ACTION: HIT"
        )

        requestThread.join(timeout=2)

        self.assertFalse(
            requestThread.is_alive(),
            "Server was still waiting for the player's action."
        )

        self.assertEqual(
            result["action"],
            "ACTION: HIT"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)