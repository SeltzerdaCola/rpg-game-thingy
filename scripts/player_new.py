import pygame as p
from .helperfunc import Metronome

class Player(p.sprite.DirtySprite):
	def __init__(self, x, y, game):
		super().__init__()
		
		#Sprite image
		self.spritesheet = p.transform.scale(p.image.load("assets/player-sprites.png").convert_alpha(), (game.settings.TileSize * 4, game.settings.TileSize * 3))
		#0 = Top 1 = Bottom 2 = Left 3 = Right
		self.facing = 1
		self.currentsprite = [0, 0, game.settings.TileSize, game.settings.TileSize]
		self.spritepos = [0, 0]
		self.visible = 1
		self.ui = 0
		self.layer = 2
		
		
		
		#Positions and Dimensions
		self.pos = p.math.Vector2(x, y)
		self.tilepos = p.math.Vector2(int((self.pos.x + (game.settings.TileSize / 2)) / game.settings.TileSize), int((self.pos.y + (game.settings.TileSize / 2)) / game.settings.TileSize))
		self.rect = p.Rect(self.pos.x, self.pos.y, game.settings.TileSize, game.settings.TileSize) #Global position
		self.hitmask = p.Rect(3 * game.settings.scale, 8 * game.settings.scale, 10 * game.settings.scale, 8 * game.settings.scale)
		self.layer = 1
		self.collision = True 
		#Up, Down, Left, Right
		self.collided = [False, False, False, False]
		
		
		self.image = p.Surface((game.settings.TileSize, game.settings.TileSize), p.SRCALPHA)
		
		#Speed, Sprint, and Stamina
		self.normal_speed = 150.0
		self.speed = self.normal_speed
		self.sprint_multiplyer = 1.7
		self.sprint_speed = int(self.normal_speed * self.sprint_multiplyer)
		self.is_sprinting = False
		
		self.stamina_limit = 10
		self.stamina = self.stamina_limit
		
		self.ave_sta_regen = 0.7
		self.moving_sta_regen = 0.6
		self.stamina_regen = self.ave_sta_regen
		
		#Velocity
		self.moving = False
		self.Vel = p.math.Vector2(0, 0)
		self.VelX = 0
		self.VelY = 0
		
		self.anim_timer = Metronome()
		self.walk_sequence = (1, 0, 2, 0)
		self.walk_index = 0
		
		self.image.blit(self.spritesheet, (0, 0), self.currentsprite)
		
		
	def setcurrent(self, num1, num2, game_):
		self.currentsprite[0] = num1 * game_.settings.TileSize
		self.currentsprite[1] = num2 * game_.settings.TileSize
		self.spritepos = [num1, num2]
		
	def update(self, game):
		
		
		#Movement
		prev_tilepos = self.tilepos
		
		if (game.keys[p.K_w] or game.keys[p.K_s]) and (game.keys[p.K_a] or game.keys[p.K_d]):
			self.speed /= 2 ** 0.5
		
		
		self.Vel = p.math.Vector2(0, 0)
		
		if game.keys[p.K_w] and game.keys[p.K_s]:
			pass
		elif game.keys[p.K_w]:
			self.Vel.y -= 1
			self.facing = 0
		elif game.keys[p.K_s]:
			self.Vel.y += 1
			self.facing = 1
		if game.keys[p.K_a] and game.keys[p.K_d]:
			pass
		elif game.keys[p.K_a]:
			self.Vel.x -= 1
			self.facing = 2
		elif game.keys[p.K_d]:
			self.Vel.x += 1
			self.facing = 3
		
		
		#Speed and Stamina
		
		if self.moving:
			self.stamina_regen = self.ave_sta_regen * self.moving_sta_regen
		else:
			self.stamina_regen = self.ave_sta_regen
		
		if game.keys[p.K_LSHIFT] and self.stamina > 0 and self.moving:
			self.speed = self.sprint_speed
			self.is_sprinting = True
			self.stamina = max(self.stamina - game.dt, 0)
		else:
			self.speed = self.normal_speed
			self.is_sprinting = False
			if not (self.moving and game.keys[p.K_LSHIFT]):
				self.stamina = min(self.stamina + (self.stamina_regen * game.dt), self.stamina_limit)
		
		
		
		#Collision neighbor check
			
		neighbor_tiles = [tile.rect for tile in self.groups()[0].sprites() if \
			(not isinstance(tile, Player)) and \
			not hasattr(tile, "isUiElement") and tile.hitbox == 1 and \
			((self.tilepos.x - 1 <= tile.tilepos.x <= self.tilepos.x + 1) and (self.tilepos.y - 1 <= tile.tilepos.y <= self.tilepos.y + 1))]
		
		
		self.collided = [False, False, False, False]
		
		#Collision X
		
		self.pos.x += self.Vel.x * self.speed * game.dt
		hitrect = self.hitmask.move(self.pos.x, self.pos.y)
		
		for t in neighbor_tiles:
			if hitrect.colliderect(t):
				
				if self.Vel.x > 0: #Left
					hitrect.right = t.left
					self.collided[2] = True
					
				elif self.Vel.x < 0: #Right
					hitrect.left = t.right
					self.collided[3] = True
					
		self.pos.x = float(hitrect.x - self.hitmask.x)
		
		if self.collided[2] or self.collided[3]:
			self.Vel.x = 0
		
		#Collision Y
		
		self.pos.y += self.Vel.y * self.speed * game.dt
		hitrect = self.hitmask.move(self.pos.x, self.pos.y)
		
		for t in neighbor_tiles:
			if hitrect.colliderect(t):
				
				if self.Vel.y > 0: #Top
					hitrect.bottom = t.top
					self.collided[0] = True
					
				elif self.Vel.y < 0: #Bottom
					hitrect.top = t.bottom
					self.collided[1] = True
					
		self.pos.y = float(hitrect.y - self.hitmask.y)
		
		if self.collided[0] or self.collided[1]:
			self.Vel.y = 0
		
		self.moving = True if self.Vel.x != 0 or self.Vel.y != 0 else False
		
		#Sprite
		
		past_spritepos = self.spritepos
		
		match self.facing:
			case 0:
				self.setcurrent(3, self.spritepos[1], game)
			case 1:
				self.setcurrent(0, self.spritepos[1], game)
			case 2:
				self.setcurrent(2, self.spritepos[1], game)
			case 3:
				self.setcurrent(1, self.spritepos[1], game)
		
		
		
		# Timer
		
		if (self.anim_timer.update(game.dt, 60 / self.speed) and self.moving):
			#self.setcurrent(self.spritepos[0],(1 - self.spritepos[1]), game)
			self.setcurrent(self.spritepos[0],self.walk_sequence[self.walk_index], game)
			self.walk_index += 1
			if len(self.walk_sequence)-1 < self.walk_index:
				self.walk_index = 0
			
		elif not self.moving:
			
			self.walk_index = 0
			self.setcurrent(self.spritepos[0], 0, game)
			
		
		self.tilepos = p.math.Vector2(int((self.pos.x + (game.settings.TileSize / 2)) / game.settings.TileSize), int((self.pos.y + (game.settings.TileSize / 2)) / game.settings.TileSize))
		
		self.rect.topleft = (self.pos.x, self.pos.y)
		
		
		if past_spritepos != self.spritepos:
			self.image.fill((0, 0, 0, 0))
			self.image.blit(self.spritesheet, (0, 0), self.currentsprite)
		
		#Dev note: The Bugsquasher
		#Prints everytime player moves a tile.Very useful (Atleast for me) but also deadly. Replace argument with whatever.
		#The triple double quotes are for your safety. Unleash at your own risk.
		
		"""
		if prev_tilepos != self.tilepos:
			print(self.tilepos)
		"""
		
		self.dirty = 1
		
if __name__ == "__main__":
	print("\n\nLol you nitty witty run from the main script\n\n")
