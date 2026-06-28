from enum import Enum, auto
from typing import List,Tuple
class Color(Enum):
    NONE = 0
    WHITE = auto()
    BLACK = auto()
class Unit(Enum):
    NONE = 0
    PAWN = auto() # 1
    KNIGHT = auto() # 2
    BISHOP = auto() # etc.
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

class Piece:
    def __init__(self,color:Color = Color.NONE,unit:Unit = Unit.NONE):
        if color is Color.NONE or unit is Unit.NONE:
            self.color = Color.NONE
            self.unit = Unit.NONE
        else:
            self.color = color
            self.unit = unit

    def __str__(self) -> str:
        match self.color:
            case Color.NONE: return "."
            case Color.WHITE: return "♙♘♗♖♕♔"[self.unit.value - 1] # auto() starts from 1
            case Color.BLACK: return "♟♞♝♜♛♚"[self.unit.value - 1]
    
    def __repr__(self) -> str:
        match self.color:
            case Color.NONE: return "None"
            case Color.WHITE: return "PNBRQK"[self.unit.value - 1] # auto() starts from 1
            case Color.BLACK: return "pnbrqk"[self.unit.value - 1] # auto() starts from 1

Coordinate = Tuple[int,int]
class Board:
    def __init__(self,
                 Pieces:List[Piece],
                 WhiteToMove:bool = True,
                 CastleRights:Tuple[bool,bool,bool,bool] = (True,True,True,True),
                 EnPassantSquare:int = -1,
                 ReversibleMoves:int = 0):
        assert len(Pieces) == 64, f"Invalid Board, length ({len(Pieces)} must be exactly 64.)"
        self.Pieces = Pieces
        self.WhiteToMove = WhiteToMove
        self.CastleRights = CastleRights
        self.EnPassantSquare = EnPassantSquare
        self.ReversibleMoves = 0 if ReversibleMoves < 0 or ReversibleMoves > 50 else ReversibleMoves

    @staticmethod
    def indexToFileRank(index:int) -> Coordinate:
        """Converts the direct index to a pair corresponding to horizontal(file) and vertical(rank) components.
        Raises a ValueError if index is less than 0 or greater than 63"""
        if index < 0 or index >= 64: raise ValueError(f"index ({index} must be in [0,64)")
        return (index % 8, index // 8)
    
    @staticmethod
    def fileRankToIndex(location:Coordinate) -> int:
        """Converts the horizontal(file) and vertical(rank) coordinates into the direct index associated with Board.Pieces.
        Raises a ValueError if the location is off the board."""
        file,rank = location
        if not (0 <= rank < 8 and 0 <= file < 8): raise ValueError(f"file({file}) and rank({rank}) must be in [0,8)")
        return 8 * rank + file
    @staticmethod
    def fileRankToStr(location:Coordinate) -> str:
        """Converts a location to the name of the square. I.E. (0,0) -> a1, (1,0) -> b1, (0,1) -> a2, etc.
        Raises a ValueError if loaction is not on the board/"""
        file,rank = location
        if not (0 <= rank < 8 and 0 <= file < 8): raise ValueError(f"file({file}) and rank({rank}) must be in [0,8)")
        return "abcdefgh"[file] + str(rank+1)

    @staticmethod
    def strToFileRank(space:str) -> Coordinate:
        return ("abcdefgh".index(space[0]),int(space[1]) - 1)
    
    def __str__(self) -> str:
        output = f"{'W' if self.WhiteToMove else 'B'} "
        if self.CastleRights == [False,False,False,False]: output += "-   "
        else:
            for i in range(4):
                output += "KQkq"[i] if self.CastleRights[i] else "-"
        
        output += " "
        if self.ReversibleMoves < 10: output += "0" + str(self.ReversibleMoves)
        else: output += str(self.ReversibleMoves)
        
        output += "\n"
        for rank in range(7,-1,-1): # read ranks downwards
            for file in range(8): # read files across
                output += str(self.Pieces[8 * rank + file])
            output += "\n"
        output += f"EnPassantSquare: {'None' if self.EnPassantSquare == -1 else self.fileRankToStr(self.indexToFileRank(self.EnPassantSquare))}"
        return output

# we can now convert between numerical index, a location, and the string name of that index
    