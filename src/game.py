import json
import pygame

from utils import Gallery, Speaker, Map, MemoryManager
from character import Player


with open('memory/core.json', 'r') as f:
	data = json.load(f)


class GameEngine:
	def __init__(self):
		self.RUN = True
		self.FPS = data['fps']
		self.width, self.height = 700 * 1.5, 500 * 1.5
		self.WIN_DIMENSIONS = [self.width, self.height]

		pygame.init()

		self.WIN = pygame.display.set_mode(self.WIN_DIMENSIONS)
		self.display = pygame.Surface((self.width // 2, self.height // 2))
		pygame.display.set_caption('....')
		pygame.mouse.set_visible(False)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Comic Sans MS', 16)
		self.igt = None

		self.true_scroll = [0, 0]
		self.speaker = Speaker()
		self.gallery = Gallery()
		self.map = Map()
		self.memory = MemoryManager()

		self.level = data['level']
		self.max_level = 2
		self.damage_map = data['damage_map']
		self.lava_blocks = []
		self.controls = {
				'left': {...},
				'right': {...},
				'up': {...},
			}
		self.mvt = {k: False for k in ['l', 'r', 'j']}  # Left, Right, Jump

		if 'wasd' in data['controls']:
			self.controls['left'].add(pygame.K_a)
			self.controls['right'].add(pygame.K_d)
			self.controls['up'].add(pygame.K_w)

		if 'arrow' in data['controls']:
			self.controls['left'].add(pygame.K_LEFT)
			self.controls['right'].add(pygame.K_RIGHT)
			self.controls['up'].add(pygame.K_UP)

		y = 0
		self.spawn_platform = [0, 0]

		for row in self.map.layers[self.level - 1][0]:
			x = 0
			for tile in row:
				if tile == '7':
					self.spawn_platform[0] = 16 * x
					self.spawn_platform[1] = 16 * y
				x += 1
			y += 1

		player_hitbox = pygame.Rect(self.spawn_platform[0], self.spawn_platform[1], 16, 22)
		self.player = Player(hitbox=player_hitbox)

		self.player.run_animation = self.gallery.player_run_animation
		self.player.idle_animation = self.gallery.player_idle_animation

	def tick(self):
		self.lava_blocks = []

		self.player.tick()
		self.clock.tick(self.FPS)
