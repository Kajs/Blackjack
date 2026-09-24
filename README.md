# Blackjack

A small Blackjack game written in Python, for the purpose of getting experience in designing a solution, planning how long each part might take and then executing the plan, by implementing the specified software architecture.

The game is played through separate dealer and player GUIs. The dealer controls the game logic and acts as the server, while the player connects as a client. Communication between the dealer and player is handled through TCP sockets.

The project started as a simple terminal-based Blackjack game and was gradually developed into a program with separate components for game logic, networking and graphical interfaces.

## Features

* Standard Blackjack game using one or more 52-card decks.
* Four-deck shoe in the current game configuration.
* Blackjack and soft/hard Ace handling.
* Dealer and player turns with Hit and Stand actions.
* Separate pygame GUI for the dealer and player.
* Dealer acts as the server and player as the client.
* Communication between dealer and player using TCP sockets.
* Player and dealer GUIs run separately from the main game/network logic, allowing the GUI to remain responsive while other parts of the program are waiting for input.
* Card images are loaded dynamically and cached for reuse.
* Player exit requests are handled at the end of a round rather than immediately interrupting the game.
* Dealer can also request that the game ends, with the current round being completed first.
* Unit tests covering the game logic, networking, main coordination logic and GUI behaviour.

## Project structure

### `Dealer_game.py`

Contains the main Blackjack game model and game-related functions.

This includes:

* The list of cards and creation of decks.
* Drawing and shuffling cards.
* Calculating Blackjack card and hand values.
* Handling Aces as either 1 or 11.
* Creating and resetting the shoe.
* Dealing cards and ending rounds.
* Creating facedown versions of dealer hands.
* Determining the winner of a round.

This module contains the core game logic and does not depend on the graphical interface.

### `Dealer_main.py`

Controls the overall game flow on the dealer side.

It coordinates:

* The Blackjack game logic.
* The dealer GUI.
* Communication with the player through the server.
* Dealer and player turns.
* Round progression and ending.
* Player exit requests and game shutdown.

The dealer GUI is run in a separate process so that blocking operations, such as waiting for network messages, do not prevent the GUI from processing pygame events.

### `Dealer_server.py`

Contains the server-side socket functionality.

It is responsible for:

* Starting and closing the server socket.
* Accepting player connections.
* Assigning player numbers.
* Sending and receiving text commands.
* Sending game-state updates to players.
* Requesting player actions and closing connections.

The current version supports one active player, although some of the data structures and message formats have been designed with multiple players in mind.

### `Dealer_gui.py`

Contains the dealer's pygame GUI.

It is responsible for:

* Drawing the dealer and player hands.
* Drawing the Hit, Stand and Exit buttons.
* Handling dealer input.
* Receiving GUI update commands through a queue.
* Sending dealer actions back to `Dealer_main` through a queue.
* Keeping the GUI responsive while the game or network code is waiting elsewhere.

### `Player_client.py`

Contains the client-side socket functionality.

It is responsible for:

* Connecting to the dealer/server.
* Sending player actions.
* Receiving messages from the dealer.
* Closing the client connection.

### `Player_main.py`

Controls the player-side program flow.

It is responsible for:

* Communicating with the dealer through `Player_client`.
* Parsing commands received from the server.
* Passing game-state updates to the player GUI.
* Requesting player actions from the GUI.
* Returning those actions to the server.

### `Player_gui.py`

Contains the player's pygame GUI.

It has the same basic structure as the dealer GUI, but displays the player and dealer hands from the player's perspective and returns the player's Hit, Stand or Quit actions.

The GUI communicates with `Player_main` through multiprocessing queues.

## Communication

The dealer and player communicate using simple text-based commands over TCP.

Examples include:

```text
REQUEST: ACTION
REQUEST: CLOSE
ACTION: HIT
ACTION: STAND
ACTION: QUIT
```

Game-state updates use a format such as:

```text
UPDATE:DEALER:FD,5S;PLAYER1:8C,AH
```

Cards are represented by short identifiers such as `7S`, `AC` and `10H`. These same identifiers are used by the game logic and as the names of the corresponding card image files.

Commands are terminated with a newline character (`\n`).

The current implementation assumes that received socket data contains complete commands. A more robust implementation would maintain a receive buffer and handle commands that are split across multiple TCP `recv()` calls.

## GUI and process structure

The GUI and main/network logic are separated so that waiting for network or game input does not make the pygame window unresponsive.

The player side can be thought of roughly as:

```text
Player_main
│
├── Player_client
│      └── TCP communication
│
├── GUI queue ──────► Player_gui
│
└── Action queue ◄── Player_gui
```

The dealer side uses a similar structure:

```text
Dealer_main
│
├── Dealer_game
│      └── Blackjack game logic
│
├── Dealer_server
│      └── TCP communication
│
├── GUI queue ──────► Dealer_gui
│
└── Action queue ◄── Dealer_gui
```

This separation also makes the project easier to extend and test.

## Testing

The project contains unit tests using Python's built-in `unittest` framework.

Tests currently cover:

* Blackjack deck and hand handling.
* Card values and Ace combinations.
* Dealing, drawing and round handling.
* Determining round winners.
* Dealer and player main-program coordination.
* Server/client communication.
* GUI message handling and player/dealer actions.

Some tests use mocks to simulate parts of the game that are outside the component being tested. For example, a GUI action can be simulated without opening an actual pygame window.

The graphical appearance and complete game experience are additionally tested manually by playing the game.

## Documentation

The `Dokumentation` folder contains additional project documentation, including UML diagrams describing the architecture and responsibilities of the main components and a requirements specification document, describing the planned architecture and the expected time needed to implement it (in danish though).

The UML documentation includes a component diagram showing the dealer and player parts of the system, including game logic, networking and GUI components and a second expanded component diagram (though showing a gui's to handle hosting and joining games, which was planned, but not implemented), a sequence diagram of a dealer hosting a game and a player joining it as well as a sequence diagram of a player taking a hit action.


## Known limitations

The current version is primarily a learning project rather than a production-ready multiplayer game.

Some examples of current limitations are:

* Only one player is fully supported.
* The connection setup currently assumes dealer and player are on the same computer using `127.0.0.1`.
* TCP message buffering does not currently handle partial commands.
* There is no reconnect or timeout system for clients that disconnect unexpectedly.
* Some GUI behaviour is tested manually rather than through automated visual tests.
* Multiple-player support would require additional turn and connection management.

The game is however quite playable locally with it's 2 separate gui's and making this work well has been prioritized over supporting more players or a more complete implementation of the blackjack rules. The separation of player and dealer, means the architecture remains scalable, if more players were to be supported in the future and likewise, although one would need to manually change the ip as is, the project isn't necessarily far from supporting play on 2 different pc's.

## Running the project

The dealer and player are separate programs and need to run as separate Python processes.

Start the dealer first so that the server is listening for a connection, and then start the player client.

The project uses `pygame` for the graphical interfaces and the standard Python socket and multiprocessing modules for communication and process separation.
