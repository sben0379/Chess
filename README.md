# Chess
## Summary 
This is the first stage of a long term project to create a chess engine using Python. As much as the programme as possible will be written from scratch (e.g. not using 
existing Python chess modules). So far, only the Pygame module is being used in the code in order to help handle graphics and user input. The point of the 
project is to put everything I have learnt about Python up to this point to the test, and to learn more about algorithms and ML as we progress further into
the project. Our initial goal will be to create a 2000 ELO strength engine. But, before we get to that stage, we'll have to start by making a 
working chess game in Python.
## Latest Update
### Version 0.6
* Began adding special rules. 
* Game now allows for promotion to a queen if a pawn reaches the final rank.
## Planned updates
* Add drag and drop functionality for moving pieces
* Get programme to recognise check, checkmate and stalemate game states
* Add special rules (eg. en passant, castling)
## Update history
### Version 0.5
* Game can now evaluate whether the king is in check and prevent the user both from making a move that does not address the check or from making a move that would move the king into check on the next turn (eg. moving a piece that's pinned to the king).
### Version 0.4
* Game now checks for whose turn it is and only allows one move per side.
### Version 0.3
* All pieces now have the correct movement restrictions, with the exception of en passant, promotion and castling.
### Version 0.2
* Pieces can now be moved by clicking on the piece and then on the target square
### Version 0.1
* Piece images mapped to corresponding piece codes
* Starting position represented using 2D list 
* Board and pieces graphically represented using Pygame