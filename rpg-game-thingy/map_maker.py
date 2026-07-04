import pygame as p

from os import path
from json import loads, load, dump
from math import ceil

from scripts.values import Settings
from scripts.camera import Camera
from scripts.loaders.tilesprites import *

class UI_Bar(p.sprite.DirtySprite):
	def __init__(self, game):
		super().__init__()
		
		self.image = p.Surface((game.settings.windowSize[0], game.settings.TileSize), p.SRCALPHA)
		self.rect = self.image.get_rect()
		self.pos = p.math.Vector2(0, 0)
		self.isUiElement = 1
		
		
	def update(self, game):
		
		self.image.fill((77, 77, 77, 128))
		
		self.dirty = 1

class UI_Button(p.sprite.DirtySprite):
	def __init__(self, game, image, index):
		super().__init__()
		
		self.image = image
		self.rect = self.image.get_rect()
		self.pos = p.math.Vector2(index + game.settings.TileSize, 0)
		self.visible = 1
		self.isUiElement = 1
		
	def update(self, game):
		
		self.dirty = 1



def dumpMap(game):
	
	game.dt = game.clock.tick() / 1000.0
	
	width = 0
	height = 0
	
	
				
	for s in game.tiles:
		if isinstance(s, Tile):
			width = int(max(width, s.tilepos.x))
			height = int(max(height, s.tilepos.y))
	print(width, height)
	width += 1
	height += 1
	
	mapdata = {"Name": game.title,
			"Id": 0,
			"Camera_Lock": game.camlock,
			"Width": width,
			"Height": height,
			"MetaData": {},
			"Map": {}}
	
	#print("Game block queue length:", len(game.block_queue["1"]))
	
	#I KNEW IT THERES A BETTER WAY !!!!!!!!!
	
	for i in game.tiles:
		if isinstance(i, Tile):
			if str(s.layer) not in mapdata["Map"]:
				mapdata["Map"].update({str(s.layer): []})
			mapdata["Map"][str(s.layer)].append([int((i.tilepos.y * width) + i.tilepos.x), i.id])
		
	mapdata["Map"] = {k: v for k, v in sorted(mapdata["Map"].items())}
			
	#Actually serializing da map
	
	with open(path.join(game.dir_path, "data", "map_maked_map.json"), "w") as f:
		dump(mapdata, f)
	
	game.dt = game.clock.tick() / 1000.0
	print(f"Finished map conversion in {float(game.dt)} seconds.")



	
class Tile(p.sprite.DirtySprite):
	def __init__(self, game, pos):
		super().__init__()
		
		self.image = p.Surface((game.settings.TileSize, game.settings.TileSize))
		
		self.pos = p.math.Vector2(pos)
		self.tilepos = p.math.Vector2(pos[0] / game.settings.TileSize, pos[1] / game.settings.TileSize)
		self.rect = p.Rect(*self.pos, game.settings.TileSize, game.settings.TileSize)
		
		image = p.transform.scale(p.image.load(game.blockIds[str(game.selectedId)]["Spritesheet_Location"]).convert_alpha(), (game.settings.TileSize, game.settings.TileSize))
		
		self.image.blit(image, (0, 0), [0, 0, game.settings.TileSize, game.settings.TileSize])
		
		self.id = game.selectedId
		self.layer = 1
		self.visible = 1
		
		
		
	def update(self, game):
		
		
		if game.mouse_press == 3 and self.rect.collidepoint(game.mouse_world_pos):
			self.visible = 0
			self.kill()
			return
		
		if self.rect.colliderect(game.camera.rect):
			self.visible = 1
		else:
			self.visible = 0
		self.dirty = 1
		



class MapMaker:
	def __init__(self, tileclass):
		
		p.init()
		
		self.settings = Settings()
		self.camera = Camera(self, p.math.Vector2(0, 0), True)
		self.window = p.display.set_mode(self.settings.windowSize)
		self.tiles = TileGroup()
		self.dir_path = path.dirname(path.realpath(__file__))
		
		
		self.tiles.sort_add(UI_Bar(self))
		
		self.mouse_pos = (0, 0)
		self.mouse_press = 0
		
		self.clock = p.time.Clock()
		self.dt = self.clock.tick() / 1000.0
		
		#Actual stuff inclusive to map maker
		self.map_name = "map_maked_map.json"
		
		self.selectedId = 1
		self.max_width = 20
		self.max_height = 20
		self.save = False
		self.file = "placeholder_map.json"
		self.title = "Placeholder_Map"
		self.camlock = [False, False]
		
		self.block_queue = {}
		
		with open("data/blocks.json") as j:
			self.blockIds = loads(j.read())
		
		with open(path.join("data", self.map_name)) as m:
			self.existing_mapdata = loads(m.read())
		
		"""
		for b in self.blockIds:
			if b != "0":
				self.tiles.sort_add(
		"""
		
		#Read existing blocks
		for l in self.existing_mapdata["Map"]:
			for t in self.existing_mapdata["Map"][l]:
				self.selectedId = int(t[1])
				pos = ((t[0] % self.existing_mapdata["Width"]) * self.settings.TileSize, (t[0] // self.existing_mapdata["Width"]) * self.settings.TileSize)
				self.tiles.sort_add(tileclass(self, pos))
					
		self.has_errored = False
		self.delete_pos = (-1, -1)
		
		self.window.fill((0xFF, 0xFF, 0xFF))
		self.active = True
	def run(self):
		
		while self.active:
			events = p.event.get()
			for e in events:
				if e.type == p.QUIT:
					self.active = False
				elif e.type == p.MOUSEMOTION:
					self.mouse_pos = e.pos
					self.mouse_press = 1 if e.buttons[0] else 2 if e.buttons[1] else 3 if e.buttons[2] else self.mouse_press
				elif e.type == p.MOUSEBUTTONDOWN:
					self.mouse_press = e.button
				elif e.type == p.KEYDOWN:
					
					if e.key == p.K_s and (e.mod & p.KMOD_CTRL):
						print("Actually saving...\n")
						dumpMap(self)
						self.save = True
					elif e.key == p.K_1:
						self.selectedId = 1
					elif e.key == p.K_2:
						self.selectedId = 2
					elif e.key == p.K_3:
						self.selectedId = 3

		
		
			self.window.fill((0xFF, 0xFF, 0xFF))
			self.dt = self.clock.tick() / 1000.0
			self.keys = p.key.get_pressed()
			self.mouse_world_pos = (self.mouse_pos[0] + self.camera.pos.x, self.mouse_pos[1] + self.camera.pos.y)
			
			self.camera.update(self)
			
			
			cam_speed = 200
			
			if self.keys[p.K_w]:
				self.camera.pos.y -= cam_speed * self.dt
			elif self.keys[p.K_s]:
				self.camera.pos.y += cam_speed * self.dt
			if self.keys[p.K_a]:
				self.camera.pos.x -= cam_speed * self.dt
			elif self.keys[p.K_d]:
				self.camera.pos.x += cam_speed * self.dt
			
			if self.mouse_press == 1:
				
				
				overlayed = False
				mouse_tile_pos = (self.mouse_world_pos[0] - (self.mouse_world_pos[0] % self.settings.TileSize), self.mouse_world_pos[1] - (self.mouse_world_pos[1] % self.settings.TileSize))
				#Make a new tile
				for sprite in self.tiles.sprites():
					
					if sprite.visible == 1 and not hasattr(sprite, "isUiElement") and (mouse_tile_pos[0] / self.settings.TileSize) == sprite.tilepos.x and (mouse_tile_pos[1] / self.settings.TileSize) == sprite.tilepos.y:
						overlayed = True
						break
				
				if (mouse_tile_pos[0] / self.settings.TileSize) + 1 > self.max_width or (mouse_tile_pos[1] / self.settings.TileSize) + 1 > self.max_height:
					print("Error: given coordinates surpass map size. Please change the map size and try again.")
				elif (not overlayed) and (self.mouse_world_pos[0] >= 0) and (self.mouse_world_pos[1] >= 0):
					self.tiles.sort_add(Tile(self, mouse_tile_pos))
					
				elif overlayed:
					pass
				else:
					if not self.has_errored:
						print("Error: given coordinates exceed world limits.")
						self.has_errored = True
				
			else:
				self.has_errored = False
				
			
			self.tiles.update(self)
			self.tiles.draw_all(self)
			
			self.mouse_press = 0
			self.save = False
			
			p.display.flip()
		
		p.quit()


if __name__ == "__main__":
	MapMaker(Tile).run()
