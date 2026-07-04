import pygame as p


class Debug_UI_Visuals(p.sprite.DirtySprite):
	def __init__(self, game):
		super().__init__()
		
		self.image = p.Surface(game.settings.windowSize, p.SRCALPHA)
		self.rect = self.image.get_rect()
		self.isUiElement = True
		self.pos = p.math.Vector2(0, 0)
		self.visible = 1
		
		self.font =  p.font.SysFont(None, 20, bold=False)
		self.fps = 1/game.dt
		self.player_speed = game.player.Vel.x * game.player.speed
		self.dt_dtimer = 0
		
		
	def update(self, game):
		self.image.fill((0, 0, 0, 0))
		
		self.dt_dtimer += game.dt
		if self.dt_dtimer >= 0.5:
			self.fps = 1//game.dt
			self.dt_dtimer = 0
		self.player_speed = abs(int(game.player.Vel.x or game.player.Vel.y) * game.player.speed)
		
		psc = [0, 0, 0]
			
		psc[1] = (200/game.player.stamina_limit)*game.player.stamina
		psc[0] = 255-((255/game.player.stamina_limit)*game.player.stamina)
		
		stamina = ((game.player.stamina / game.player.stamina_limit) * 250)
		
		p.draw.rect(self.image, (0, 100, 0), (0, 200, 20, 250))
		p.draw.rect(self.image, psc, (0, 200 + (250 - stamina), 20, stamina))
		
		p.draw.rect(self.image, (20, 20, 20), [0, 0, game.fps_limit*3, 10])
		p.draw.rect(self.image, (00, 100, 00), [0, 0, self.fps*3, 10])
		
		self.image.blit(game.font.render(str(self.fps) + " FPS", True, (0, 0, 0)), (0, 10))
		self.image.blit(game.font.render(str(round(self.player_speed, 2)) + " Units per second", True, (0, 0, 0)), (0, 30))
		self.image.blit(game.font.render("E to tp, I to camlock X, O to camlock Y, Q to exit", True, (0, 0, 0)), (0, 50))
		
		
		self.dirty = 1	

class StaticTile_(p.sprite.DirtySprite):
	def __init__(self, surface, blockdata, pos, layer, game):
		super().__init__()
		
		self.image = surface
		self.tilepos = p.math.Vector2(pos)
		self.pos = self.tilepos * game.settings.TileSize
		
		self.rect = p.Rect(*self.pos, game.settings.TileSize, game.settings.TileSize)
		self.hitbox = blockdata["Hitbox"]
		
		self.layer = int(layer)
		self.visible = 0
		
	def update(self, game):
		
		if self.rect.colliderect(game.camera.rect):
			self.visible = 1
			
		else:
			self.visible = 0
		self.dirty = 1


class TileGroup(p.sprite.Group):
	def __init__(self):
		super().__init__()
		self.sorted_sprites = {}
		
	def sort_sprites(self):
		
		for i in self.sprites():
			
			if i.layer not in self.sorted_sprites:
				self.sorted_sprites.update({i.layer: []})
			self.sorted_sprites[i.layer].append(i)
				
		self.sorted_sprites = {k: v for k, v in sorted(self.sorted_sprites.items())}
		
	def sort_add(self, sprite):
		
		self.add(sprite)
		new_layer = False
		
		if sprite.layer not in self.sorted_sprites:
			new_layer = True
			self.sorted_sprites.update({sprite.layer: []})
		self.sorted_sprites[sprite.layer].append(sprite)
		
		if new_layer:
			self.sorted_sprites = {k: v for k, v in sorted(self.sorted_sprites.items())}
	def draw_all(self, game):
		
		
		for l in self.sorted_sprites:
			for s in self.sorted_sprites[l]:
				
				if not s.alive():
					self.sorted_sprites[l].remove(s)
				if bool(s.visible):
					game.camera.tile_blit(s)
		
class UiGroup(p.sprite.Group):
	def __init__(self):
		super().__init__()
		
		self.ui_sprites = []
		
	def draw_all(self, game):
		
		[game.camera.ui_blit(s) for s in self.sprites() if bool(s.visible)]
