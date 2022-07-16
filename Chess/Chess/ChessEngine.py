# Creating a chess engine in python using pygame by Eddie Sharick.

"""
This class is responsible for storing all the information about the current state of a chess game. It will
also be responsinle for determining the volid moves at the current state . It will also keep a move log.
"""

class GameState():
	def __init__(self):
		# board is an 8x8 2nd list, each element of the list has 2 characters.
		# The first character represents the color of the peace, "b" or "w"
		# The second character represents the type of the peace, "K", "Q", "R", "B", "N" or "P".
		# "--" represents an empty space with no piece. 
		self.board = [
			["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
			["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["--", "--", "--", "--", "--", "--", "--", "--"],
			["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
			["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
		self.whiteToMove = True
		self.moveLog = []

	def makeMove(self, move):
		"""
		Take a Move as a parameter and executed it (this will not work for castling,
		pawn promotion and en-passant)
		"""
		self.board[move.startRow][move.startCol] = "--"
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.moveLog.append(move) # log the move so we can undo it later
		self.whiteToMove = not self.whiteToMove # swap players

	def undoMove(self):
		"""
		Undo the last move made 
		"""
		if len(self.moveLog) != 0: # Make sure that there is a move to undo
			move = self.moveLog.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove # switch turns back


class Move():
	# maps keys to values
	# key: value
	ranksToRaws = {"1": 7, "2": 6, "3": 5, "4": 4,
				   "5": 3, "6": 2, "7": 1, "8": 0}
	rowsToRanks = {v: k for k, v in ranksToRaws.items()}
	filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
				   "e": 4, "f": 5, "g": 6, "h": 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}

	def __init__(self, startSq, endSq, board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]

	def getChessNotation(self):
		# you can add to make this real chess notation
		return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

	def getRankFile(self, r, c):
		return self.colsToFiles[c] + self.rowsToRanks[r]
