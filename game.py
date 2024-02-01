import pygame


class GameState:
	"""For running game logic"""

	def __init__(self):
		self.fps = 60
		self.mvt = {k: False for k in ['l', 'r', 'j', 'd']}  # Left, Right, Jump, Dash
		self.controls = {
			'left': {pygame.K_a, pygame.K_LEFT},
			'right': {pygame.K_d, pygame.K_RIGHT},
			'up': {pygame.K_w, pygame.K_UP, pygame.K_SPACE},
		}

		self.dash_allowed = False
		self.end_animation = False
		self.death_animation = False

		self.dashes = 1
		self.level = 1
		self.end_timer = 60 * 60  # no. of seconds * 60
		self.timer = 10 * 60
		self.info = False
		self.debug = False

		self.wait = False
		self.wait_timer = 0
		self.last_death = 0

		self.damage_map = {'lava': 100, 'spikes': 100, 'fall': 5}
		self.lava_blocks = []

	def wait_for(self, time):
		self.wait = True
		self.wait_timer = time

	def update(self):
		self.wait = self.wait_timer == 0
		self.lava_blocks = []
