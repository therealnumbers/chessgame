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
    
    @property
    def isNone(self) -> bool:
        return self.color is Color.NONE
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
    
    @staticmethod
    def strToPiece(char:str) -> "Piece":
        if char in "PNBRQK": return Piece(Color.WHITE,Unit("PNBRQK".index(char) + 1))
        if char in "♙♘♗♖♕♔": return Piece(Color.WHITE,Unit("♙♘♗♖♕♔".index(char) + 1))
        if char in "pnbrqk": return Piece(Color.BLACK,Unit("pnbrqk".index(char) + 1))
        if char in "♟♞♝♜♛♚": return Piece(Color.BLACK,Unit("♟♞♝♜♛♚".index(char) + 1))
        return Piece(Color.NONE,Unit.NONE)

Coordinate = Tuple[int,int]
class Board:
    def __init__(self,
                 Pieces:List[Piece],
                 WhiteToMove:bool = True,
                 CastleRights:Tuple[bool,bool,bool,bool] = (True,True,True,True),
                 EnPassantSquare:int = -1,
                 HalfMoveClock:int = 0):
        assert len(Pieces) == 64, f"Invalid Board, length ({len(Pieces)} must be exactly 64.)"
        self.Pieces = Pieces
        self.WhiteToMove = WhiteToMove
        self.CastleRights = CastleRights
        self.EnPassantSquare = EnPassantSquare
        self.HalfMoveClock = 0 if HalfMoveClock < 0 or HalfMoveClock > 100 else HalfMoveClock

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
    
    def getPiece(self,location:Coordinate) -> Piece:
        return self.Pieces[Board.fileRankToIndex(location)]

    def __str__(self) -> str:
        output = f"{'W' if self.WhiteToMove else 'B'} "
        if self.CastleRights == [False,False,False,False]: output += "----"
        else:
            for i in range(4):
                output += "KQkq"[i] if self.CastleRights[i] else "-"
        
        output += " "
        if self.HalfMoveClock < 10: output += "0" + str(self.HalfMoveClock)
        else: output += str(self.HalfMoveClock)
        
        output += "\n"
        for rank in range(7,-1,-1): # read ranks downwards
            for file in range(8): # read files across
                output += str(self.Pieces[8 * rank + file])
            output += "\n"
        output += f"EnPassantSquare: {'None' if self.EnPassantSquare == -1 else self.fileRankToStr(self.indexToFileRank(self.EnPassantSquare))}"
        return output

# we can now convert between numerical index, a location, and the string name of that index

    def LoadFEN(self,FEN:str):
        """Parses a Forsyth-Edwards Notation string and updates the board to match. FEN consists of 5 space-seperated fields:
        Pieces on the Board: a list from top rank to bottom, where a letter represents that piece as according to repr() and a number is a run of empty squares.
        Side to Move: W if white otherwise B for black.
        Castling Ability: a subset of 'KQkq' for each pair of castling player and castle side, or '-' if no one can castle.
        En Passant Square: either '3' or '6' followed by the file of the last double pawn push,'-' if the last move is not a double pawn push.
        Half-Move Clock: The number of moves since the last irreversible move. If it reaches greater than 100, the game is drawn due to the 50 move rule."""
        self.Pieces = [Piece(Color.NONE, Unit.NONE) for _ in range(64)] # clear the board
        args = FEN.split(' ')

        # Handle Piece Locations
        rank = 7
        file = 0
        for char in args[0]:
            if char in "PNBRQKpnbrqk":
                self.Pieces[Board.fileRankToIndex((file,rank))] = Piece.strToPiece(char)
                file += 1
            elif char in "12345678":
                file += int(char)
            elif char == "/":
                rank -= 1
                file = 0
        
         
        self.WhiteToMove = args[1] == "w" # Side to Move
        self.CastleRights = [(right in args[2]) for right in "KQkq"] # Castling Ability
        self.EnPassantSquare = -1 if args[3] == "-" else Board.fileRankToIndex(Board.strToFileRank(args[3])) # En Passant Square
        self.HalfMoveClock = int(args[4]) # Half Move Clock

    def SaveFEN(self) -> str:
        output = ""
        
        rank = 7
        file = 0
        seenEmptyTiles = 0 # The number of empty spaces seen thus far
        while rank >= 0:
            if file == 8:
                if seenEmptyTiles:
                    output += str(seenEmptyTiles)
                    seenEmptyTiles = 0
                output += "/"
                rank -= 1
                file = 0
                continue
            currentPiece = self.getPiece((file,rank))
            if currentPiece.isNone:
                seenEmptyTiles += 1
            else:
                if seenEmptyTiles:
                    output += str(seenEmptyTiles)
                    seenEmptyTiles = 0
                output += repr(currentPiece)
            file += 1
        output = output.strip("/")
        output += " " + ("w" if self.WhiteToMove else "b")
        output += " " + (''.join("KQkq"[i] for i in range(4) if self.CastleRights[i]) if any(self.CastleRights) else '-')
        output += " " + ("-" if self.EnPassantSquare == -1 else (Board.fileRankToStr(Board.indexToFileRank(self.EnPassantSquare))))
        output += " " + str(self.HalfMoveClock)
        return output