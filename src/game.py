import pygame

from character import Player
from utils import *


def _load_map(path):
	with open('./assets/level_data/' + path + '.txt', 'r') as file:
		data = file.read()
		return [line.rstrip("0") or "0" for line in data.split('\n')]


level_data = [
			[_load_map('level1_layer1'), _load_map('level1_layer2'), _load_map('level1_layer3')],
			[_load_map('level2_layer1'), _load_map('level2_layer2'), _load_map('level2_layer3')],
			[_load_map('level3_layer1'), _load_map('level3_layer2'), _load_map('level3_layer3')],
		]


class GameEngine:
	def __init__(self):
		self.RUN = True
		self.FPS = 60
		self.width, self.height = 700 * 1.5, 500 * 1.5
		self.WIN_DIMENSIONS = [self.width, self.height]
		self.WIN = pygame.display.set_mode(self.WIN_DIMENSIONS)
		self.d = pygame.Surface((self.width // 2, self.height // 2))

		self.clock = pygame.time.Clock()

		self.level_data = level_data
		self.gallery = Gallery()

		self.gravitational_vector = pygame.Vector2(0, 0.19)

		self.level = 1
		self.scroll = [0, 0]
		self.controls = {}
		self.spawn_platform = [0, 0]
		self.damage_map = {"lava": 50, "spikes": 2.5, "fall": 0.75}
		self.mvt = {k: False for k in ['l', 'r', 'j']}  # Left, Right, Jump

		self.doors = [pygame.Rect(1000, 1000, 1, 1)]
		self.player = Player(spawn_location=[*self.get_spawn_coordinates(), 16, 22])
		self.player.run_animation = self.gallery.player_run_animation
		self.player.idle_animation = self.gallery.player_idle_animation
		self.speaker = speaker

		self.reset()

	def pre_update(self) -> None:
		self._check_whether_level_up()

		self._draw_health_bar()
		self._draw_player_movement()

	def _draw_health_bar(self):
		loc = (self.player.hitbox.x - self.scroll[0], self.player.hitbox.y - self.scroll[1] - 8)

		pygame.draw.rect(self.d, "red", (*loc, 32, 4))
		pygame.draw.rect(self.d, "green", (*loc, 32 * self.player.hp / self.player.max_hp, 4))

	def _check_whether_level_up(self):
		for door in self.doors:
			if self.player.hitbox.colliderect(door):

				self.level += 1
				speaker.next_level_sound.play()
				self.player.update_pos(*self.get_spawn_coordinates())
				self.doors = []

	@staticmethod
	def _flip_img(img):
		return pygame.transform.flip(img, True, False)

	def _draw_player_movement(self):
		# default scroll
		scrl = (self.player.hitbox.x - self.scroll[0], self.player.hitbox.y - self.scroll[1])

		if self.mvt['j']:
			if self.player.facing_right:
				self.d.blit(self.gallery.player_jump_img, scrl)
			else:
				self.d.blit(self._flip_img(self.gallery.player_jump_img), scrl)

		elif not self.mvt['l'] and not self.mvt['r']:
			self.player.idle_count += 1

			if self.player.facing_right:
				self.d.blit(self.player.idle_animation[self.player.idle_count], scrl)
			else:
				self.d.blit(self._flip_img(self.player.idle_animation[self.player.idle_count]), scrl)

		else:
			self.player.run_count += 1

			if self.player.facing_right:
				self.d.blit(self.player.run_animation[self.player.run_count], (scrl[0] + 1, scrl[1]))
			else:
				self.d.blit(self._flip_img(self.player.run_animation[self.player.run_count]), (scrl[0] - 1, scrl[1]))

	def calc_movement(self):
		movement = [0, 0]

		if self.player.alive:
			if self.mvt['l'] or self.mvt['r']:
				self.player.velocity_vector.x += self.player.linear_travel_speed / 2

				if self.mvt['l']:
					movement[0] -= self.player.velocity_vector.x
				else:
					movement[0] += self.player.velocity_vector.x

			movement[1] += self.player.velocity_vector.y
			self.player.velocity_vector.y += self.gravitational_vector.y

		else:
			self.reset()

		return movement

	def get_spawn_coordinates(self):
		spawn_location = [0, 0]
		y = 0

		try:
			for row in self.level_data[self.level - 1][0]:
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

	def update(self):
		if self.level > 3:
			self.level = 1

		pygame.display.flip()

		self.player.update()
		self.clock.tick(self.FPS)

	def reset(self):
		self.scroll = [0, 0]

		self.level = 1
		self.mvt = {k: False for k in ['l', 'r', 'j']}  # Left, Right, Jump
		self.player.reset(self.get_spawn_coordinates())

		self.controls['left'] = (pygame.K_a, pygame.K_LEFT)
		self.controls['right'] = (pygame.K_d, pygame.K_RIGHT)
		self.controls['up'] = (pygame.K_w, pygame.K_UP)

		self.RUN = True
