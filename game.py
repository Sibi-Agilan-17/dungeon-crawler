import pygame

from utils import Gallery, Speaker, Map
from character import Player


class GameEngine:
	def __init__(self):
		self.RUN = True
		self.FPS = 60
		self.width, self.height = 700 * 1.5, 500 * 1.5
		self.WIN_DIMENSIONS = [self.width, self.height]

		pygame.init()

		self.WIN = pygame.display.set_mode(self.WIN_DIMENSIONS)
		self.display = pygame.Surface((self.width // 2, self.height // 2))
		pygame.display.set_caption('Lorem Ipsum')
		pygame.mouse.set_visible(False)
		self.clock = pygame.time.Clock()

		self.true_scroll = [0, 0]
		self.game_state = GameState()
		self.speaker = Speaker()
		self.gallery = Gallery()
		self.map = Map()

		y = 0
		self.spawn_platform = [0, 0]

		for row in self.map.layers[self.game_state.level - 1][0]:
			x = 0
			for tile in row:
				if tile == '7':
					self.spawn_platform[0] = 16 * x
					self.spawn_platform[1] = 16 * y
				x += 1
			y += 1

		player_hitbox = pygame.Rect(self.spawn_platform[0], self.spawn_platform[1], 16, 22)
		self.player = Player(hitbox=player_hitbox)

	def tick(self):
		self.player.tick()
		self.game_state.tick()
		self.clock.tick(self.game_state.fps)


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

		self.last_death = 0

		self.damage_map = {'lava': 100, 'spikes': 100, 'fall': 5}
		self.lava_blocks = []

	def tick(self):
		self.lava_blocks = []
