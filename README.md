# Chessengine with Pygame

![Image of chess in pygame](https://github.com/LimIvan336/LimIvan336/blob/main/images/chessengine_screenshot.PNG)

## Description

A simple chess engine implemented in pygame with legitimate chess rules and moves such as castling, pawn promotion and en-passant.

## Getting Started

Install [python3](https://www.python.org/downloads/)

<br>

### Dependencies

* pygame v2.0.1

Download and install the latest release:

`pip install pygame`

Upgrading to the latest version with the `-U` flag:

`pip install -U pygame`

<br>

### Setup
Download the files manually or clone the repository into your machine.

Locate the main driver file (main.py).

<br>

## Running

* How to run the program:

</t>`python3 main.py`


* How to play

1. White first, click on any piece of white and make a valid move by pressing the destination square.
2. Black goes next and the rules of chess follows.
3. Game ends until either side got checkmate/stalemate.


* Special keys

1. To undo a move, press Ctrl - Z on keyboard.
2. To reset the game, press Ctrl - R on keyboard.

## Remarks

For pawn promotion, the pawn will and only be promoted to a queen, i.e. cannot make selection of what piece to change into.

Rules for chess can be found [here](https://www.chesscoachonline.com/chess-articles/chess-rules)

<!-- ## Authors

Contributors names and contact info

ex. Dominique Pizzie  
[@DomPizzie](https://twitter.com/dompizzie) -->

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [Eddie Sharick](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)
* [Implementing a chess engine from scratch](https://towardsdatascience.com/implementing-a-chess-engine-from-scratch-be38cbdae91)
