# this is the third time weve completley restated
# lets go
import re
import random as rand
from typing import Tuple, Optional

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
    @staticmethod
    def stringifyPiece(p:PieceInt):
        if p == Piece.NONE: return "."
        match p & Piece.TYPEMASK:
            case Piece.PAWN: chars = "♙🨩" # Why is the black pawn stupid
            case Piece.KNIGHT: chars = "♘♞"
            case Piece.BISHOP: chars = "♗♝"
            case Piece.ROOK: chars= "♖♜"
            case Piece.QUEEN: chars = "♕♛"
            case Piece.KING: chars = "♔♚"
            case _: raise AssertionError("HOW")

        index = 0 if p & Piece.COLORMASK == Piece.WHITE else 1
        return chars[index]

class Board:
    def __init__(self):
        self.board:list[PieceInt] = [Piece.NONE for _ in range(64)]
        
    def __str__(self):
        rows = [""]
        for i in range(64):
            if i % 8 == 0:
                rows.insert(0,"")
            rows[0] += Piece.stringifyPiece(self.board[i])
        return "\n".join(rows)
