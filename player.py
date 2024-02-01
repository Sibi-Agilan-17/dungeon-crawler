import pygame.draw


class Character:
	def __init__(self):
		self.max_hp = 0
		self.position = []
		self.linear_travel_speed = 0
		self.rect: pygame.Rect

	def update(self, *args, **kwargs):
		"""To be subclassed by child classes"""
		...


class Player(Character):
	def __init__(self, **kwargs):
		super(Player, self).__init__()

		self.hp = 100
		self.max_hp = 100
		self.alive = True
		self.linear_travel_speed = 2
		self.air_timer = 0
		self.gravity = 0
		self.respawn = [0, 0]

		for k, v in kwargs.items():
			setattr(self, k, v)

	def update(self):
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

	def update(self):
		self.alive = self.hp > 0
		self.hp = self.max_hp if self.hp > self.max_hp else self.hp

	def reset_stats(self):
		self.hp = self.max_hp
		self.air_timer = 0
		self.gravity = 0
