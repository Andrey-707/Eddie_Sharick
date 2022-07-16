# Creating a chess engine in python using pygame by Eddie Sharick.

"""
This is our main driver file. It will be responsible for hand;ing user input and displaying the current GameState object.
"""

import pygame as p

from Chess import ChessEngine


WIDHT = HEIGHT = 512 # 400 is another option
p.display.set_caption("Chess")
DIMENSION = 8 # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}


def loadImages():
	"""
	Initialize a global dictionary of images. This will be called exactly once in the main
	"""
	pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load("images\\" + piece + ".png "), (SQ_SIZE, SQ_SIZE))
	# Note: we can access an image by saying "IMAGES["wp"]"


def main():
	"""
	The main driver for our code. This will handle user input and updating the graphics
	"""
	p.init()
	screen = p.display.set_mode((WIDHT, HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color("white"))
	gs = ChessEngine.GameState()
	loadImages() # only do this ones, before the while loop
	running = True
	sqSelected = () # not square is secected, keep track ofthe last click of the user (tuple: (raw, col))
	playerClicks = [] # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
			# mouse handler
			elif e.type == p.MOUSEBUTTONDOWN:
				location = p.mouse.get_pos() # (x, y) location of mouse
				col = location[0]//SQ_SIZE
				row = location[1]//SQ_SIZE
				if sqSelected  == (row, col): # the user clicked the same square twice
					sqSelected = () # deselect
					playerClicks = [] # clear player clicks
				else:
					sqSelected = (row, col)
					playerClicks.append(sqSelected) # append for both 1st and 2nd clicks
				# was that the users 2nd click?
				if len(playerClicks) == 2:
					move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
					print(move.getChessNotation())
					gs.makeMove(move)
					sqSelected = () # reset usel clicks
					playerClicks = [] # 
			# key handlers
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z: # undo when "z" is press
					gs.undoMove()

		drawGameState(screen, gs)
		clock.tick(MAX_FPS)
		p.display.flip()


def drawGameState(screen, gs):
	"""
	Responsible for all the graphics within a current game state.
	"""
	drawBoard(screen) # draw squares on the board
	# add in piece hightlighting or move suggestion (later)
	drawPieces(screen, gs.board) # draw a pieces on top of thous squares


def drawBoard(screen):
	"""
	Draw the squareson the board. The top left square is always light. 
	"""
	colors = [p.Color("White"), p.Color("Dark grey")]
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = colors[((r+c) % 2)]
			p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
	"""
	Draw the pieces on the board using the current GameState.board
	"""
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			if piece != "--": # not empty square
				screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# run
if __name__ == "__main__":
	main()
