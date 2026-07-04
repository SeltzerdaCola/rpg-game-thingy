def collision(a, b):
	return (a[0] < b[0] + b[2]) and (a[0] + a[2] > b[0]) and (a[1] < b[1] + b[3]) and (a[1] + a[3] > b[1])
ewmul = lambda a, b: [a * b for a, b in zip(a, b)] 

class Metronome():
	def __init__(self, tick = 1):
		self.active = True
		self.timer = 0
		self.tick = tick
		self.is_ticked = False
	def update(self, delta, tick = 0):
		if self.active:
			self.timer += delta
			if tick > 0:
				self.tick = tick
			if self.timer >= self.tick:
				self.is_ticked = True
				self.timer = 0
				return True
			return False
