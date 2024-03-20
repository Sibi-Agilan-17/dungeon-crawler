import pygame


class Player:
	def __init__(self, spawn_location: list = (0, 0, 16, 16), **kwargs):

		# game logic variables

		self.regen = 0.2
		self.max_hp = 100
		self.hp = self.max_hp
		self.alive: bool = False
		self.velocity_cap = 2
		self.linear_travel_speed = 1

		# graphic logic variables

		self.air_time: int = 0
		self.run_count: int = 0
		self.facing_right = True
		self.idle_count: int = 0
		self.velocity_vector = pygame.Vector2(0, 0)
		self.hitbox: pygame.Rect = pygame.Rect(*spawn_location)
		self.idle_animation = self.run_animation = []  # will be written later

		for k, v in kwargs.items():
			setattr(self, k, v)

	def move(self, collision_types, movement_data, tile_data):
		self.hitbox.x += movement_data[0]

		for collision in self._collision_test(tile_data):
			if movement_data[0] > 0:
				self.hitbox.right = collision.left
				collision_types['right'] = True

			elif movement_data[0] < 0:
				self.hitbox.left = collision.right
				collision_types['left'] = True

		self.hitbox.y += movement_data[1]

		for collision in self._collision_test(tile_data):
			if movement_data[1] > 0:
				self.hitbox.bottom = collision.top
				collision_types['bottom'] = True

			elif movement_data[1] < 0:
				self.hitbox.top = collision.bottom
				collision_types['top'] = True

		return collision_types

	def _collision_test(self, tiles) -> list:
		return [x for x in tiles if self.hitbox.colliderect(x)]

	def update(self):
		self.alive = self.hp > 0

		self.hp = pygame.math.clamp(self.hp, 0, self.max_hp)
		self.velocity_vector.y = pygame.math.clamp(self.velocity_vector.y, -7.8, 7.8)
		self.velocity_vector.x = pygame.math.clamp(self.velocity_vector.x, 0, self.velocity_cap)

		if self.idle_count + 2 >= len(self.idle_animation):
			self.idle_count = 0

		if self.run_count + 2 >= len(self.run_animation):
			self.run_count = 0

		self.hp += self.regen

	def update_pos(self, x, y):
		self.hitbox.x = x
		self.hitbox.y = y

	def reset(self, coordinates=(0, 0)):
		self.air_time = 0
		self.hp = self.max_hp
		self.facing_right = True
		self.update_pos(*coordinates)
