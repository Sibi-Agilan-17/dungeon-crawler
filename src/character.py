import json
import pygame.draw

with open('memory/core.json', 'r') as f:
	data = json.load(f)


__all__ = [
	"Object",
	"Character",
	"Player",
]


class Object(object):
	"""
	Properties common to all the objects in the game

	* Affected by gravity
	* Has mass and can be moved
	"""

	def __init__(self, hitbox=None):
		self.hitbox: pygame.Rect = hitbox
		self.gravity = 0

	def tick(self):
		"""All objects get updated every tick"""

		if self.gravity > 5:
			self.gravity = 5

	def update(self, x, y):
		self.hitbox.x = x
		self.hitbox.y = y

	def collision_test(self, tiles):
		colliding_tiles = []

		for tile in tiles:
			if self.hitbox.colliderect(tile):
				colliding_tiles.append(tile)

		return colliding_tiles

	def move(self, collision_types, movement_data, tile_data):
		self.hitbox.x += movement_data[0]

		for collision in self.collision_test(tile_data):
			if movement_data[0] > 0:
				self.hitbox.right = collision.left
				collision_types['right'] = True

			elif movement_data[0] < 0:
				self.hitbox.left = collision.right
				collision_types['left'] = True

		self.hitbox.y += movement_data[1]

		for collision in self.collision_test(tile_data):
			if movement_data[1] > 0:
				self.hitbox.bottom = collision.top
				collision_types['bottom'] = True

			elif movement_data[1] < 0:
				self.hitbox.top = collision.bottom
				collision_types['top'] = True

		return collision_types


class Character(Object):
	"""All characters, whether controlled by a human or by the computer"""

	def __init__(self, hitbox=None):
		super().__init__(hitbox)

		self.max_hp: int = 0
		self.hp: int = self.max_hp

		self.velocity: int = 0
		self.velocity_cap: int = -1
		self.air_time: int = 0

		self.alive: bool = False
		self.is_controlled_by_computer: bool = False

		self.idle_count: int = 0
		self.run_count: int = 0

	def tick(self):
		super(Character, self).tick()

		if self.hp > self.max_hp:
			self.hp = self.max_hp

		if self.velocity > self.velocity_cap:
			self.velocity = self.velocity_cap

		self.alive = self.hp > 0

	def reset_stats(self, coordinates=(0, 0)):
		self.hp = self.max_hp
		self.velocity = 0
		self.air_time = 0
		self.gravity = 0
		self.update(*coordinates)


class Player(Character):
	def __init__(self, **kwargs):
		super(Player, self).__init__()

		self.max_hp = data['player']['max_health']
		self.hp = self.max_hp
		self.linear_travel_speed = data['player']['speed']
		self.velocity_cap = data['player']['speed_cap']
		self.regen = data['player']['regen']
		self.facing_right = True
		self.idle_animation = self.run_animation = []  # will be written later

		for k, v in kwargs.items():
			setattr(self, k, v)

	def tick(self):
		super(Player, self).tick()

		if self.idle_count + 1 >= len(self.idle_animation):
			self.idle_count = 0

		if self.run_count + 1 >= len(self.run_animation):
			self.run_count = 0

		self.hp += self.max_hp * self.regen / 1000


class Enemy(Character):
	def __init__(self, **kwargs):
		super(Enemy, self).__init__()

		self.facing_right = True
		self.is_controlled_by_computer = True

		for k, v in kwargs.items():
			setattr(self, k, v)

	def tick(self):
		super(Enemy, self).tick()
