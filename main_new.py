from os import path
from json import load

try:
	import pygame as p
except ImportError:
	print("You is NOT download pygame T_T\nDownload it first $$")

import scripts
from scripts.loaders.tilesprites import *
from scripts.loaders.loaders import *
from scripts.helperfunc import Metronome, ewmul
from scripts.player import Player
from scripts.values import Settings
from scripts.camera import Camera
from scripts.helperfunc import collision, Metronome

class Sprites:
	def __init__(self):
		self.staticTile = StaticTile_
class Game:
	def __init__(self):
		
		p.init()
		p.font.init()
		#print(p.font.get_fonts())
		
		self.settings = Settings()
		self.window = p.display.set_mode(self.settings.windowSize)
		
		
		self.clock = p.time.Clock()
		self.dir_path = path.dirname(path.realpath(__file__))
		self.font = p.font.Font("Minecraft.ttf", 20)
		self.player = Player(1 * self.settings.TileSize, 1 * self.settings.TileSize, self)
		self.camera = Camera(self, self.player.pos)
		
		
		with open("data/blocks.json") as j:
			self.blockIds = load(j)
		
		self.dt = self.clock.tick() / 1000.0
		
		self.tileGroup = TileGroup()
		self.uiGroup = TileGroup()
		self.sprite_loader = Sprite_Loader()
		self.maploader = Loader()
		self.sprites = Sprites()
		
		
		print(path.join(self.dir_path, "data", "placeholder_map.json"))
		
		self.map_name = "map_maked_map.json"
		
		self.uiGroup.add(Debug_UI_Visuals(self))
		self.tileGroup.add(self.maploader.Load_Map(path.join(self.dir_path, "data", self.map_name), self))
		self.tileGroup.add(self.player)
		self.tileGroup.sort_sprites()	
		
		
		self.dev_timer = Metronome(1)
		self.fps_limit = 60
		self.dt = self.clock.tick() / 1000.0
		print(self.dt)
		
		self.active = True
		
		#==OH HEY LOOOOK THE MAIN LOOP STARTS HEREEEE==#
		
		
	def run(self):
		while self.active:
			for e in p.event.get():
				if e.type == p.QUIT:
					self.active = False
				if e.type == p.KEYDOWN:
					if e.key == p.K_i:
						self.camera.static[0] = not self.camera.static[0]
					if e.key == p.K_o:
						self.camera.static[1] = not self.camera.static[1]
			
			self.dt = self.clock.tick(self.fps_limit) / 1000.0
			if 1 <= self.dt <= 2:
				self.dt = 0.7
			elif self.dt > 2:
				self.dt = 0.005 
			
			self.window.fill((0xE0, 0xE0, 0xE0))
			
			self.keys = p.key.get_pressed()
			
			if self.keys[p.K_q]:
				self.active = False
			if self.keys[p.K_e]:
				self.player.pos.x = 50
				self.player.pos.y = 50
			
			self.camera.update(self)
			
			self.tileGroup.update(self)
			self.uiGroup.update(self)
			self.tileGroup.draw_all(self)
			self.uiGroup.draw_all(self)
			
			self.camera.draw_all(self)
			
			visible_tiles = len([1 for s in self.tileGroup if s.visible == 1])
			
			if self.dev_timer.update(self.dt):
				#Happens per second
				print(f"Number of pixels in ui_surface: {p.mask.from_surface(self.camera.ui_surface).count()}")
				"""
				print("="*10)
				#BUGLOG: somehow 0
				
				#BUGLOG: somehow normal
				print(f"Visible tiles apparently rn: {visible_tiles}")
				print(f"Last tiles position in the camera: {self.camera.dev_var}")"""
			
			p.display.flip()
		
		p.quit()
	
	
if __name__ == "__main__":
	Game().run()

