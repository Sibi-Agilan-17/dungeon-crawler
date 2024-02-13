import json
import pygame

from utils import *
from character import Player


__all__ = [
	'GameEngine',
]

with open('memory/core.json', 'r') as f:
	data = json.load(f)


class GameEngine:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('...')
		pygame.mouse.set_visible(False)

		self.RUN = True
		self.FPS = data['fps']
		self.width, self.height = 700 * 1.5, 500 * 1.5
		self.WIN_DIMENSIONS = [self.width, self.height]
		self.WIN = pygame.display.set_mode(self.WIN_DIMENSIONS)
		self.display = pygame.Surface((self.width // 2, self.height // 2))

		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Comic Sans MS', 16)
		self.igt = None
		self.debug = True

		self.true_scroll = [0, 0]
		self.speaker = Speaker()
		self.gallery = Gallery()
		self.map = Map()

		self.gravitational_vector = pygame.Vector2(0, 0.2)

		self.level = data['level']
		self.max_level = 3
		self.score = 0
		self.damage_map = data['damage_map']
		self.spawn_platform = [0, 0]
		self.lava_blocks = []
		self.controls = {k: {...} for k in ['left', 'right', 'up', 'cheats']}
		self.mvt = {k: False for k in ['l', 'r', 'j']}  # Left, Right, Jump

		if 'wasd' in data['controls']:
			self.controls['left'].add(pygame.K_a)
			self.controls['right'].add(pygame.K_d)
			self.controls['up'].add(pygame.K_w)

		if 'arrow' in data['controls']:
			self.controls['left'].add(pygame.K_LEFT)
			self.controls['right'].add(pygame.K_RIGHT)
			self.controls['up'].add(pygame.K_UP)

		if 'cheats' in data['controls']:
			self.controls['cheats'].add(pygame.K_c)

		self.doors = [pygame.Rect(1000, 1000, 1, 1)]
		self.player = Player(hitbox=pygame.Rect(*self.get_spawn_coordinates(), 16, 22))
		self.player.run_animation = self.gallery.player_run_animation
		self.player.idle_animation = self.gallery.player_idle_animation

	def get_spawn_coordinates(self):
		spawn_location = [0, 0]
		y = 0

		try:
			for row in self.map.layers[self.level - 1][0]:
				x = 0
				for tile in row:
					if tile == '7':
						spawn_location[0] = 16 * x
						spawn_location[1] = 16 * y
					x += 1
				y += 1

		except IndexError:  # next level does not exist
			spawn_location = [1024, 1024]

		return spawn_location

	def tick(self):
		for door in self.doors:
			if self.player.hitbox.colliderect(door):
				self.level += 1
				self.score += 100
				self.speaker.next_level_sound.play()
				self.player.update_position(*self.get_spawn_coordinates())
				self.doors = []

		self.lava_blocks = []
		self.player.tick()
		self.clock.tick(self.FPS)

	def reset_stats(self):
		self.score = 0
		self.level = 1
		self.igt = None
		self.RUN = True
