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
    FILENAMES = "abcdefgh"
    RANKNAMES = "12345678"
    def __init__(self):
        # The actual board is a list of PieceInts.
        self.board:list[PieceInt] = [Piece.NONE for _ in range(64)]
        self.whiteToMove = True
        self.castlingRights = [True,True,True,True] # White kingside, White queenside, Black kingside, Black Queenside
        self.enPassantSquare = -1
        self.halfMoves = 0

    
    @staticmethod
    def topDownIndex(square:int) -> int:
        """Takes the top down index and convert it to the regular index
        
        Board.topDownIndex(63) = 8 """
        file = square % 8
        rank = square // 8
        return 8*(7-rank) + file
    
    @staticmethod
    def indexToName(index:int) -> str:
        """Takes in a square and returns its coordinates. Bottom left is a1, top right is h8 """
        if index < 0 or index >= 64:
            return "-"
        file = index % 8
        rank = index // 8
        return Board.FILENAMES[file] + Board.RANKNAMES[rank]
    
    @staticmethod
    def nameToIndex(squareName):
        if squareName == "-":
            return -1
        file = Board.FILENAMES.index(squareName[0])
        rank = Board.RANKNAMES.index(squareName[1])
        return (8 * rank) + file
    

        
            
    def __str__(self):
        position = ""
        for square in range(64):
            square = Board.topDownIndex(square)
            position += Piece.pieceToSymbol(self.board[square]) + ("" if (square + 1) % 8 else "\n")
        return position
    

    def saveFEN(self) -> str:
        #TODO: Add support for extended FEN, information such as castling.
        position = ""
        run = 0
        for square in range(64):
            square = Board.topDownIndex(square)
            if (square) % 8 == 0 and square != Board.topDownIndex(0):
                position += "/"
            if self.board[square] == Piece.NONE:
                run += 1
                if not ((square + 1) % 8):
                    position += str(run)
                    run  = 0
                continue
            if run != 0:
                position += str(run)
                run = 0
            position += Piece.pieceToSymbol(self.board[square], FEN = True)

        turn = 'w' if self.whiteToMove else "b"
        castle = ''.join(["KQkq"[i] for i in range(4) if self.castlingRights[i]])
        if castle == '': castle = '-'
        enPassant = Board.indexToName(self.enPassantSquare)
        halfMoves = self.halfMoves

        return f'{position} {turn} {castle} {enPassant} {halfMoves}'
    
    def loadFen(self,FEN:str):
        position, turn, castle, enPassant ,halfMoves = FEN.split(' ')
        currentSquare = 0
        for char in position:
            if char == "/": continue
            if char.isnumeric():
                for _ in range(int(char)):
                    self.board[Board.topDownIndex(currentSquare)] = Piece.NONE
                    currentSquare += 1
                continue
            self.board[Board.topDownIndex(currentSquare)] = Piece.symbolToPiece(char)
            currentSquare += 1
        self.whiteToMove = (turn == "w")
        self.castlingRights = [(i in castle) for i in "KQkq"]
        self.enPassantSquare = Board.nameToIndex(enPassant)
        self.halfMoves = int(halfMoves)
    
            
if __name__ == '__main__':
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    fen = "8/2PK1NQB/qppP1PPB/1n2p3/P1r1RpPb/p2P1ppR/rP2Nkbp/2n5 w - - 0"
    a = Board()
    a.loadFen(fen)
    assert a.saveFEN() == fen, f"\noutput: {a.saveFEN()}\nactual: {fen}"
    print(a)
