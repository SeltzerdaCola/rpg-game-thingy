import pygame as p

class Camera:
	def __init__(self, game, pos, mapmaker = False):
		
		self.mapmaker = mapmaker
		
		if self.mapmaker:
			self.pos = pos
		else:
			self.pos = p.math.Vector2(pos.x - (game.settings.windowSize[0]/2), pos.y - (game.settings.windowSize[1]/2))
		
		self.lerp_weight = 5
		self.lerp_overlook = 50
		self.rect = p.Rect(self.pos.x, self.pos.y, *game.settings.windowSize)
		self.static = [False, False]
		self.map_boundaries = []
		
		self.zoom_target = 1
		self.zoom = 1
		
		self.tile_surface = p.Surface(game.settings.windowSize, p.SRCALPHA)
		self.ui_surface = p.Surface(game.settings.windowSize, p.SRCALPHA)
		
		
	def update(self, game):
		
		if self.mapmaker:
			self.rect.topleft = self.pos
			return
		
		if not self.static[0]:
			self.pos.x = p.math.lerp(self.pos.x, min(max(game.player.pos.x-(game.settings.windowSize[0]/2), 0), self.map_boundaries[0] - self.rect.w), self.lerp_weight * game.dt)
		if not self.static[1]:
			self.pos.y = p.math.lerp(self.pos.y, min(max(game.player.pos.y-(game.settings.windowSize[1]/2), 0), self.map_boundaries[1] - self.rect.h), self.lerp_weight * game.dt)
		
		
		self.rect.topleft = self.pos
	def draw_all(self, game):
		
		game.window.blit(self.tile_surface, (0, 0))
		game.window.blit(self.ui_surface, (0, 0))
		
		self.tile_surface.fill((0, 0, 0, 0))
		self.ui_surface.fill((0, 0, 0, 0))
		
	def viewpos(self, x, y):
		
		return [x - self.pos.x, y - self.pos.y]
	def ui_blit(self, sprite):
		
		self.ui_surface.blit(sprite.image, sprite.pos)
	def tile_blit(self, sprite):
		
		self.tile_surface.blit(sprite.image, (sprite.pos.elementwise() - self.pos.elementwise()))
