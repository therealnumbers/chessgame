# this is the third time weve completley restated
# lets go
import random as rand
from typing import Tuple, Optional, Generator

# First: we need a way to view the board and the pieces within
# Zeroth: we need a way to represent pieces
# Lets try the bitboard approach

# Any 5-bit integer can be a piece. The revelant consideration consists
# of two parts: type and color

PieceInt = int
class Piece:
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    WHITE = 8
    BLACK = 16

    COLORMASK = 24  # 0b11000
    TYPEMASK = 7    # 0b00111
    NONE = 0
    
    @staticmethod
    def isInvalid(n:PieceInt) -> bool:
        badColor = n & Piece.COLORMASK == Piece.COLORMASK
        badType = n & Piece.TYPEMASK == Piece.TYPEMASK
        outsideScope = (n & Piece.COLORMASK) + (n & Piece.TYPEMASK) != n
        return badColor or badType or outsideScope
    
    # Figure out if theres a way to make this symbol relation
    # Without hardcoding it

    PIECENUMBERS:Tuple[int,...] = (
        WHITE | PAWN,
        WHITE | KNIGHT,
        WHITE | BISHOP,
        WHITE | ROOK,
        WHITE | QUEEN,
        WHITE | KING,
        BLACK | PAWN,
        BLACK | KNIGHT,
        BLACK | BISHOP,
        BLACK | ROOK,
        BLACK | QUEEN,
        BLACK | KING,
        NONE)
    PIECESYMBOLS = tuple("♙♘♗♖♕♔🨩♞♝♜♛♚.")
    PIECELETTERS = tuple("PNBRQKpnbrqkX")

    @staticmethod
    def pieceToSymbol(p:PieceInt,*,FEN = False) -> str:
        index = Piece.PIECENUMBERS.index(p)
        return Piece.PIECELETTERS[index] if FEN else Piece.PIECESYMBOLS[index]
    
    @staticmethod
    def symbolToPiece(p:str) -> int:
        if p in Piece.PIECESYMBOLS:
            return Piece.PIECENUMBERS[Piece.PIECESYMBOLS.index(p)]
        if p in Piece.PIECELETTERS:
            return Piece.PIECENUMBERS[Piece.PIECELETTERS.index(p)]
        raise ValueError(f"Invalid Char {p}")

class Board:
    def __init__(self):
        """The Board is just a list of pieces. Starts counting from the bottom left corner moving
        right, going up when reaching the end of a rank."""
        self.board:list[PieceInt] = [Piece.NONE for _ in range(64)]
    
    
    @staticmethod
    def topDownIndex(square:int) -> int:
        """Takes the top down index and convert it to the regular index
        
        Board.topDownIndex(63) = 8 """
        file = square % 8
        rank = square // 8
        return 8*(7-rank) + file
            
    def __str__(self):
        pieces = ""
        for square in range(64):
            square = Board.topDownIndex(square)
            pieces += Piece.pieceToSymbol(self.board[square]) + ("" if (square + 1) % 8 else "\n")
        return pieces
    

    def saveFEN(self) -> str:
        #TODO: Add support for extended FEN, information such as castling.
        output = ""
        run = 0
        for square in range(64):
            square = Board.topDownIndex(square)
            if (square) % 8 == 0 and square != Board.topDownIndex(0):
                output += "/"
            if self.board[square] == Piece.NONE:
                run += 1
                if not ((square + 1) % 8):
                    output += str(run)
                    run  = 0
                continue
            if run != 0:
                output += str(run)
                run = 0
            output += Piece.pieceToSymbol(self.board[square], FEN = True)

        return output
    def loadFen(self,FEN:str):
        currentSquare = 0
        for char in FEN:
            if char == "/": continue
            if char.isnumeric():
                for _ in range(int(char)):
                    self.board[Board.topDownIndex(currentSquare)] = Piece.NONE
                    currentSquare += 1
                continue
            self.board[Board.topDownIndex(currentSquare)] = Piece.symbolToPiece(char)
            currentSquare += 1
    
            
if __name__ == '__main__':
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    a = Board()
    fen = "R1B4Q/pnPpr3/2PNr2q/p1bPP1p1/Rpbp1P2/3n2PP/3pPp1B/1KN1k3"
    a.loadFen(fen)
    try:
        assert a.saveFEN() == fen
    except AssertionError:
        print(f"a.saveFEN(): {a.saveFEN()},\nActual Fen: {fen}")
    
    print(a)
