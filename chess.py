# this is the fifth time we've completley restated
# lock in fr this time

# TODO:
# Make chess pieces
# Make Board
# Create Save and Load States for the board
# Define GenerateMoves() for the board, which creates a list of all valid moves
# Then we make the engine.

from enum import Flag,auto
from typing import Tuple
class Piece(Flag):
    NONE = 0
    PAWN = auto()
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

    WHITE = auto()
    BLACK = auto()

    UNIT_MASK = PAWN | KNIGHT | BISHOP | ROOK | QUEEN | KING
    COLOR_MASK = WHITE | BLACK

    @property
    def getUnit(self): return self & Piece.UNIT_MASK

    def isUnit(self,other:'Piece') -> bool: return (self & other & Piece.UNIT_MASK).value.bit_count() == 1

    @property
    def getColor(self): return self & Piece.COLOR_MASK

    def isColor(self,other:'Piece') -> bool: return (self & other & Piece.COLOR_MASK).value.bit_count() == 1
    
    @property
    def isWhite(self) -> bool: return self.getColor == Piece.WHITE

    @property
    def isValid(self) -> bool:
        """A piece is consider valid if it contains exactly one
        Unit and exactly one Color"""
        VALIDUNIT = (self.getUnit).value.bit_count() == 1
        VALIDCOLOR = (self.getColor).value.bit_count() == 1
        return VALIDUNIT and VALIDCOLOR
    
    @property
    def toChr(self) -> str:
        if not self.isValid: return ' '
        WHITE_PIECES = {
            Piece.PAWN:   "♙",
            Piece.KNIGHT: "♘",
            Piece.BISHOP: "♗",
            Piece.ROOK:   "♖",
            Piece.QUEEN:  "♕",
            Piece.KING:   "♔",
        }
        BLACK_PIECES = {
            Piece.PAWN:   "🨩",
            Piece.KNIGHT: "♞",
            Piece.BISHOP: "♝",
            Piece.ROOK:   "♜",
            Piece.QUEEN:  "♛",
            Piece.KING:   "♚",
        }
        CORRECT_DICT = WHITE_PIECES if self.isWhite else BLACK_PIECES
        return CORRECT_DICT[self.getUnit]

board = list[Piece]
class Board:
    def __init__(self, 
                 pieceConfig:board,
                 whiteToPlay:bool,
                 castleRights: Tuple[bool,bool,bool,bool],
                 enPassantSquare:int,
                 halfmoveClock:int):
            """
            :board PieceConfig: A list of the starting Pieces. Must be 64 in length. pieceConfig[0]
            is the bottom right square, and then increases left to right, down to up.
            :bool whiteToPlay: If True, white is making a move.
            :bool[4] castleRights: White Kingside, White Queenside, Black Kingside, Black Queenside. 
            :int halfmoveClock: The numbers of reversible moves that have been made in a row. This is relevant for the 50 move rule.
            """
            
            if len(pieceConfig) != 64: raise ValueError(f"A board needs exactly 64 squares! Provided board has {len(pieceConfig)} instead.")
            self.boardState = pieceConfig
            self.whiteToPlay = whiteToPlay
            self.castleRights = castleRights
            self.enPassantSquare = enPassantSquare if 0 <= enPassantSquare < 64 else -1
            self.halfmoveClock = halfmoveClock if 0 <= halfmoveClock < 50 else 0

    # so the chessboard is set up like this:
    # a8 b8 c8 d8 e8 f8 g8 h8
    # a7 b7 c7 d7 e7 f7 g7 h7
    # a6 b6 c6 d6 e6 f6 g6 h6
    # a5 b5 c5 d5 e5 f5 g5 h5
    # a4 b4 c4 d4 e4 f4 g4 h4
    # a3 b3 c3 d3 e3 f3 g3 h3
    # a2 b2 c2 d2 e2 f2 g2 h2
    # a1 b1 c1 d1 e1 f1 g1 h1     
    # each corrseponding to one of 63 hex numbers

    @staticmethod
    def squareToRankFile(index:int) -> Tuple[int,int]:
        if 0 <= index < 64 : return (index % 8, index // 8)
        raise ValueError(f"Invalid square index: {index}")
    @staticmethod
    def rankFileToSquare(rankFile:Tuple[int,int]) -> int:
        rank = rankFile[0]
        file = rankFile[1]
        if 0 <= rank < 8 and 0 <= file < 8: return (8 * file) + rank
        raise ValueError(f"Invalid Rank-File pair: {rankFile}")