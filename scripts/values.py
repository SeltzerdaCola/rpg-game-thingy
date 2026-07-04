import pygame as p

class Settings:
	def __init__(self):
		self.ogTileSize = 16
		self.scale = 3
		self.windowScale = (16, 12)
		
		self.TileSize = self.ogTileSize * self.scale
		self.TileArea = (self.TileSize, self.TileSize)
		self.windowSize = (self.TileSize * self.windowScale[0], self.TileSize * self.windowScale[1])
		
		self.TileMultiply = lambda x, y: (x * self.TileSize, y * self.TileSize)
		self.PixelProduct = lambda x, y: (x * self.scale, y * self.scale)
