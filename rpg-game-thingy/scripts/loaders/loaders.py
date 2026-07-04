import pygame as p
from json import load
from os import path

class Loader:
	def __init__(self):
		pass
	def Load_Map(self, Loc, game):
		print("Starting map generation...\n")
		with open(Loc) as j:
			mapdata = load(j)
		
		surfaces = []
		
		for i in tuple(mapdata["Map"].keys()):
			for t in mapdata["Map"][i]:
				
				loaded_sprite = game.sprite_loader.load_sprite(game.blockIds[str(t[1])]["Sprite_Type"] , map_ = mapdata , blockdata = game.blockIds[str(t[1])] , blockid = t[1] , tilepos = (t[0] % mapdata["Width"], t[0] // mapdata["Width"]), layer = i, game_ = game)
				
				surfaces.append(loaded_sprite)
			
		game.camera.map_boundaries = (mapdata["Width"] * game.settings.TileSize, mapdata["Height"] * game.settings.TileSize)
		
		return surfaces
class Sprite_Loader:
	def __init__(self):
		
		self.stloaders = {
			"1": self.st_solid,
			"2": self.st_flexible,
			"3": self.st_terrain
			}
	def load_sprite(self, spritetypeid, **kwargs):
		
		if spritetypeid != 0:
			return self.stloaders[str(spritetypeid)](kwargs)
		
		
	def st_solid(self, k):
		
		
		raw_image = p.transform.scale(p.image.load(path.join(k["game_"].dir_path, k["blockdata"]["Spritesheet_Location"])).convert_alpha(), k["game_"].settings.TileArea)
		
		tile_surface = p.Surface(raw_image.get_size())
		
		tile_surface.blit(raw_image, (0, 0), (*k["blockdata"]["Spritesheet_Pos"], k["game_"].settings.TileSize, k["game_"].settings.TileSize))
		
		
		return k["game_"].sprites.staticTile(tile_surface, k["blockdata"], k["tilepos"], k["layer"], k["game_"])
		
	def st_flexible(self, k):
		pass
	def st_terrain(self, k):
		
		"""
		bitmask_mapwidth = 4
		bitmask_map = ((3, 3), (3, 2), (2, 3), (2, 2), \
						(0, 3), (0, 2), (1, 3), (1, 2), \
						(3, 0), (3, 1), (2, 0), (2, 1), \
						(0, 0), (0, 1), (1, 0), (1, 1))
		
		#Get neighbors
		width = k["map_"]["Width"]
		unpack = lambda n: (n % width, n // width)
		pack_pos = k["tilepos"][1] * width + k["tilepos"][0]
		bitmask = 0
		tilemap = k["map_"][k["layer"]]
		
		tiles = tuple(t[0] for t in filter(lambda i: i[1] == k["blockid"], tilemap) if True)
		neighbors = (pack_pos - width, pack_pos - 1, pack_pos + 1, pack_pos + width)
		
		#Orthodoxal neighbor checking
		
		mask_bool = (int(neighbors[0] in tiles), int(neighbors[1] in tiles), int(neighbors[2] in tiles), int(neighbors[3] in tiles))
		bitmask += (1 * mask_bool[0]) + (2 * mask_bool[1]) + (4 * mask_bool[2]) + (8 * mask_bool[3])
		
		raw_image = p.transform.scale( p.image.load( path.join( k["game_"].dir_path, k["blockdata"]["Spritesheet_Location"]) ).convert_alpha(), k["game_"].settings.TileMultiply(5, 4))
		sub_image = raw_image.subsurface( *k["game"].settings.TileMultiply(*bitmask_map[bitmask], *k["game"].settings.TileArea)
		
		tile_surface = p.Surface(k["game_"].settings.TileArea)
		
		#Diagonal neighbor checking
		in_corner_pos = (k["game"].settings.TileMultiply(4, 0))
		
		if mask_bool[0] and mask_bool[1]: # Top left
			#TODO: Get the inward corner pieces at 0, 0
			
			in_corner = subsurface(*in_corner_pos, *k["game"].settings.TileArea)
			
		if mask_bool[0] and mask_bool[2]: # Top right
			#TODO: Get the inward corner pieces at 1, 0
			
			pixel_pos = k["game_"].settings.PixelProduct(8, 0)
			in_corner = subsurface(in_corner_pos[0] + pixel_pos[0], in_corner_pos[1] + pixel_pos[1], *k["game"].settings.TileArea)
			
		if mask_bool[1] and mask_bool[3]: # Bottom left
			#TODO: Get the inward corner pieces at 0, 1
			
		if mask_bool[2] and mask_bool[3]: # Bottom right
			#TODO: Get the inward corner pieces at 1, 1
		
		"""
		
		
