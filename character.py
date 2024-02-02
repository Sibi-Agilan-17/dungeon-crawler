import json
import pygame.draw

with open('memory/settings.json', 'r') as f:
	data = json.load(f)


class Character:
	def __init__(self, hitbox=None):
		self.max_hp = 0
		self.position = []
		self.linear_travel_speed = 0
		self.hitbox: pygame.Rect = hitbox

	def collision_test(self, lis):  # lis = tiles
		colliding_tiles = []

		for tile_ in lis:
			if self.hitbox.colliderect(tile_):
				colliding_tiles.append(tile_)

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

	def tick(self, *args, **kwargs):
		"""To be subclassed by child classes"""
		...


class Player(Character):
	def __init__(self, **kwargs):
		super(Player, self).__init__()

		self.max_hp = data['player']['max_health']
		self.hp = self.max_hp
		self.alive = True
		self.linear_travel_speed = data['player']['speed']
		self.regen = data['player']['regen']
		self.air_timer = 0
		self.gravity = 0
		self.respawn = [0, 0]

		for k, v in kwargs.items():
			setattr(self, k, v)

	def tick(self):
		self.hp += self.max_hp * self.regen / 1000

		self.alive = self.hp > 0
		self.hp = self.max_hp if self.hp > self.max_hp else self.hp

		if self.gravity > 5:
			self.gravity = 5

	def reset_stats(self):
		self.hp = self.max_hp
		self.air_timer = 0
		self.gravity = 0


class Enemy(Character):
	def __init__(self, **kwargs):
		super(Enemy, self).__init__()

		self.hp = 25
		self.max_hp = 25
		self.alive = True
		self.linear_travel_speed = 1.5
		self.air_timer = 0
		self.gravity = 0
		self.respawn = [32, 0]

		for k, v in kwargs.items():
			setattr(self, k, v)

	def tick(self):
		self.alive = self.hp > 0
		self.hp = self.max_hp if self.hp > self.max_hp else self.hp

	def reset_stats(self):
		self.hp = self.max_hp
		self.air_timer = 0
		self.gravity = 0
