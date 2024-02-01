"""
Survival game made by R. Sibi Agilan of class 10-C for Chip Challenge 2023-24
"""

import os
import pygame
import random
import sys
import time

from game import GameState
from player import Player

cnt = 0

pygame.init()

width, height = 700 * 1.5, 500 * 1.5
WIN = pygame.display.set_mode((width, height))
display = pygame.Surface((width // 2, height // 2))
game_state = GameState()

dash_allow = False
end = False

s = e = time.time()

death_animation = False

idle_count = 0
run_count = 0
dash_count = 0
dashes = 1
door = pygame.Rect(1000, 1000, 1, 1)

idle_images = []
run_images = []
layer1_images = []
layer2_images = []
layer3_images = []
death_images = []
particles = []
alive = []

direction = [1]

true_scroll = [0, 0]

black = (0, 0, 0)
white = (255, 255, 255)
gray = (55, 55, 55)

pygame.display.set_caption('Chip Challenge 2023-24 Project')
pygame.mouse.set_visible(False)
pygame.mixer.set_num_channels(4)


def load_image(img_name):
	return pygame.image.load(img_name).convert_alpha()


for i in range(1, 6):
	idle_img = load_image(os.path.join('assets', 'images', 'idle_animation', 'Idle ' + str(i) + '.png'))
	idle_images.append(idle_img)

for i in range(1, 8):
	run_img = load_image(os.path.join('assets', 'images', 'run_animation', 'Run ' + str(i) + '.png'))
	run_images.append(run_img)

for i in range(1, 7):
	sprite_img = load_image(os.path.join('assets', 'images', 'tiles', 'layer1_tiles', 'Sprite_' + str(i) + '.png'))
	layer1_images.append(sprite_img)

for i in range(7, 16):
	sprite_img = load_image(os.path.join('assets', 'images', 'tiles', 'layer2_tiles', 'Sprite_' + str(i) + '.png'))
	layer2_images.append(sprite_img)

for i in range(16, 25):
	sprite_img = load_image(os.path.join('assets', 'images', 'tiles', 'layer3_tiles', 'Sprite_' + str(i) + '.png'))
	layer3_images.append(sprite_img)

jump_img = load_image(os.path.join('assets', 'images', 'jump_animation', 'Jump.png'))
lava_img = load_image(os.path.join('assets', 'images', 'texture', 'lava (2).png'))


def load_map(path):
	file = open('assets/level_data/' + path + '.txt', 'r')
	data = file.read()
	file.close()
	data = data.split('\n')
	game_map = []

	for line in data:
		game_map.append(list(line))

	return game_map


layers = []
levels = []

layers.append([load_map('level1_layer1'), load_map('level1_layer2'), load_map('level1_layer3')])
layers.append([load_map('level2_layer1'), load_map('level2_layer2'), load_map('level2_layer3')])
layers.append([load_map('level3_layer1'), load_map('level3_layer2'), load_map('level3_layer3')])

y = 0
spawn_platform = [0, 0]

for row in layers[game_state.level - 1][0]:
	x = 0
	for tile in row:
		if tile == '7':
			spawn_platform[0] = 16 * x
			spawn_platform[1] = 16 * y
		x += 1
	y += 1

player_rectangle = pygame.Rect(spawn_platform[0], spawn_platform[1], 16, 22)
player = Player(rect=player_rectangle)
alive.append(player)


def clip(surf, x_coordinate, y_coordinate, x_size, y_size):
	handle_surf = surf.copy()
	clip_r = pygame.Rect(x_coordinate, y_coordinate, x_size, y_size)
	handle_surf.set_clip(clip_r)
	image = surf.subsurface(handle_surf.get_clip())
	return image.copy()


class Sound:
	def __init__(self, path, channel=0, volume=1.0):
		self.path = path
		self.paused = False
		self.volume = volume
		self.channel = pygame.mixer.Channel(channel)
		self.channel.set_volume(volume)
		self.sound = pygame.mixer.Sound(path)

	def play(self):
		if self.paused:
			return self.channel.unpause()

		self.channel.play(self.sound)

	def pause(self):
		self.paused = True
		self.channel.pause()

	def is_playing(self) -> bool:
		return self.channel.get_busy()


class Font:
	def __init__(self, path):
		self.spacing = 1
		self.character_order = [
			'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
			'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
			'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', '\'', '!', '?', '0', '1', '2',
			'3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';'
		]
		self.characters = {}
		font_img = load_image(path).convert()
		current_char_width = 0
		character_count = 0

		for wid in range(font_img.get_width()):
			c = font_img.get_at((wid, 0))
			if c[0] == 127:
				char_img = clip(font_img, wid - current_char_width, 0, current_char_width, font_img.get_height())
				self.characters[self.character_order[character_count]] = char_img.copy()
				character_count += 1
				current_char_width = 0
			else:
				current_char_width += 1
		self.space_width = self.characters['A'].get_width()

	def render(self, surf, text, loc):
		x_offset = 0
		for char in text:
			if char != ' ':
				surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
				x_offset += self.characters[char].get_width() + self.spacing
			else:
				x_offset += self.space_width + self.spacing


my_big_font = Font('assets/large_font.png')
next_level_sound = Sound('./assets/sounds/next_level.mp3', channel=3)
background_music = Sound('./assets/sounds/background_music.mp3', channel=1, volume=0.65)
jump_sound = Sound('./assets/sounds/jump.mp3')


def animate(frames, frame_duration):
	animation = []
	for u in range(len(frames)):
		for v in range(frame_duration):
			animation.append(frames[u])
	return animation


idle_animation = animate(idle_images, 12)
run_animation = animate(run_images, 6)


def collision_test(rect, lis):  # lis = tiles
	colliding_tiles = []

	for tile_ in lis:
		if rect.colliderect(tile_):
			colliding_tiles.append(tile_)

	return colliding_tiles


def move(rect, movement_data, tile_data):  # movement = [5,2]
	rect.x += movement_data[0]

	for collision in collision_test(rect, tile_data):
		if movement_data[0] > 0:
			rect.right = collision.left
			collision_types['right'] = True
		elif movement_data[0] < 0:
			rect.left = collision.right
			collision_types['left'] = True

	rect.y += movement_data[1]

	for collision in collision_test(rect, tile_data):
		if movement_data[1] > 0:
			rect.bottom = collision.top
			collision_types['bottom'] = True
		elif movement_data[1] < 0:
			rect.top = collision.bottom
			collision_types['top'] = True

	return rect, collision_types


# Game Loop
clock = pygame.time.Clock()
run = True
background_music.play()
game_state.last_death = time.time()

while run:
	s = time.time()

	if not background_music.is_playing():
		background_music.play()

	display.fill((28, 31, 36))
	mx, my = pygame.mouse.get_pos()
	collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

	true_scroll[0] += (player_rectangle.x - true_scroll[0] - 165) / 15
	true_scroll[1] += (player_rectangle.y - true_scroll[1] - 236) / 15

	scroll = true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

	tiles = []
	spikes = []
	platforms = []

	if end or game_state.info:
		end_text = 'Congratulations! You have won!'

		if end:
			display.fill(black)
			game_state.end_timer -= 1

			if game_state.end_timer <= 3600:
				my_big_font.render(display, end_text, (225 / 2, 235 / 2))
				y = 0

				for row in layers[game_state.level - 1][0]:
					x = 0
					for tile in row:
						if tile == '7':
							player.respawn[0] = 16 * x
							player.respawn[1] = 16 * y
						x += 1
					y += 1

			if game_state.end_timer == 0:
				game_state.end_timer = 3600
				end = False
				game_state.level = 1
				direction.append(1)

		if game_state.info:
			display.fill(black)
			game_state.timer -= 1

			if game_state.timer <= 3600:
				my_big_font.render(display, "Jump and press X for a secret move", (225 / 2, 235 / 2))
				y = 0

				for row in layers[game_state.level - 1][0]:
					x = 0
					for tile in row:
						if tile == '7':
							player.respawn[0] = 16 * x
							player.respawn[1] = 16 * y
						x += 1
					y += 1

			if game_state.timer == 0:
				game_state.timer = 600
				game_state.info = False
				game_state.level = 3

	if game_state.level > 3:
		end = True
		game_state.end_timer = 60 * 60
		game_state.level = 1
		player.reset_stats()

	for layer in layers[game_state.level - 1]:
		y = 0

		if layer == layers[game_state.level - 1][0]:
			for row in layer:
				x = 0
				for tile in row:
					if tile == '1':
						display.blit(layer1_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '2':
						display.blit(layer1_images[1], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '3':
						display.blit(layer1_images[2], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '4':
						display.blit(layer1_images[3], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '5':
						display.blit(layer1_images[4], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '6':
						display.blit(layer1_images[5], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '7':
						display.blit(layer1_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))
						player.respawn[0] = 16 * x
						player.respawn[1] = 16 * y
					if tile == 'l':
						display.blit(lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
						game_state.lava_blocks.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile != '0' and tile != '1' and tile != '2' and tile != '7' and tile != 'l':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))

					x += 1
				y += 1

		if layer == layers[game_state.level - 1][1]:
			for row in layer:
				x = 0
				for tile in row:
					if tile == '1':
						display.blit(layer2_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '2':
						display.blit(layer2_images[1], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '3':
						display.blit(layer2_images[2], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '4':
						display.blit(layer2_images[3], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '5':
						display.blit(layer2_images[4], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '6':
						display.blit(layer2_images[5], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '7':
						display.blit(layer2_images[6], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '8':
						display.blit(layer2_images[7], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '9':
						display.blit(layer2_images[8], (16 * x - scroll[0], 16 * y - scroll[1]))
						door = pygame.Rect(16 * x, 16 * y, 16, 32)
					if tile == 'l':
						display.blit(lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
						game_state.lava_blocks.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile != '0' and tile != '9' and tile != 'l':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))
					x += 1
				y += 1

		if layer == layers[game_state.level - 1][2]:
			for row in layer:
				x = 0
				for tile in row:
					if tile == '1':
						display.blit(layer3_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '2':
						display.blit(layer3_images[1], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '3':
						display.blit(layer3_images[2], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '4':
						display.blit(layer3_images[3], (16 * x - scroll[0], 16 * y - scroll[1]))
					if tile == '5':
						display.blit(layer3_images[4], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x, 16 * y + 6, 16, 10))
					if tile == '6':
						display.blit(layer3_images[5], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x, 16 * y, 10, 16))
					if tile == '7':
						display.blit(layer3_images[6], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x, 16 * y - 6, 16, 10))
					if tile == '8':
						display.blit(layer3_images[7], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x + 6, 16 * y, 10, 16))
					if tile == '9':
						display.blit(layer3_images[8], (16 * x - scroll[0], 16 * y - scroll[1]))
						platforms.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile == 'l':
						display.blit(lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
						game_state.lava_blocks.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile != '0' and tile != '5' and tile != '6' and tile != '7' and tile != '8' and tile != '9' and tile != 'l':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))
					x += 1
				y += 1

	for spike in spikes:
		if player_rectangle.colliderect(spike):
			player.hp -= game_state.damage_map['spikes'] // 10

	for lava_block in game_state.lava_blocks:
		if player_rectangle.colliderect(lava_block):
			player.hp -= game_state.damage_map['lava']

	movement = [0, 0]

	if not end:
		if player.alive:
			if game_state.mvt['l']:
				movement[0] -= player.linear_travel_speed
			if game_state.mvt['r']:
				movement[0] += player.linear_travel_speed
			if not game_state.mvt['d']:
				movement[1] += player.gravity
				player.gravity += 0.2

	if dash_count + 1 >= 5:
		game_state.mvt['d'] = False
		dash_count = 0
		player.gravity = 0

	if game_state.mvt['d'] and player.alive:
		if direction[-1] == 1:
			movement[0] += dash_count * 7
			dash_count += 0.5
		elif direction[-1] == 2:
			movement[0] -= dash_count * 7
			dash_count += 0.5

	player_, collisions = move(player_rectangle, movement, tiles)

	if player_.colliderect(door):
		next_level_sound.play()
		player.reset_stats()
		game_state.wait_for(60)
		game_state.last_death = time.time()

		game_state.level += 1

		y = 0

		for row in layers[game_state.level - 1][0]:
			x = 0
			for tile in row:
				if tile == '7':
					player.respawn[0] = 16 * x
					player.respawn[1] = 16 * y
				x += 1
			y += 1

		player_.x = player.respawn[0] - 16
		player_.y = player.respawn[1] - 16

		if game_state.level == 3:
			game_state.info = True

		if game_state.level == 4:
			end = True

		continue

	plat_col = []
	for platform in platforms:
		if player_rectangle.colliderect(platform):
			plat_col.append(platform)

	for tile in plat_col:
		if movement[1] > 0:
			player_rectangle.bottom = tile.top
			collision_types['bottom'] = True

	if not (player.alive or game_state.wait):
		dash_count = 0
		player.gravity = 0
		game_state.mvt['d'] = False

		if not game_state.wait:
			player_rectangle.x = player.respawn[0]
			player_rectangle.y = player.respawn[1]
			player.alive = True
			player.reset_stats()
			game_state.last_death = time.time()

			if not game_state.debug:
				game_state.level = 1

		oe = 2

		if len(particles) == 0 and oe == 1:
			for num in range(30):
				particles.append([[(player_.center[0] - scroll[0]), (player_.center[1] - scroll[1])], [random.randint(0, 30) / 10 - 1.5, random.randint(0, 10) / 6 - 3], random.randint(3, 5)])

		for particle in particles:
			particle[0][0] += particle[1][0]
			particle[0][1] += particle[1][1] - 0.5
			particle[2] -= 0.05
			particle[1][1] += 0.035
			pygame.draw.circle(display, (255, 0, 50), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

	if player.alive:
		particles.clear()

		pygame.draw.rect(display, "red", (player_.x - scroll[0], player_.y - scroll[1] - 8, 32, 4))
		pygame.draw.rect(display, "green", (player_.x - scroll[0], player_.y - scroll[1] - 8, 32 * player.hp / player.max_hp, 4))

	if collision_types['bottom']:
		grav = 0
		dashes = 1
		game_state.mvt['j'] = False

		if player.air_timer > 50:
			player.hp -= game_state.damage_map['fall'] * player.air_timer // 10

		player.air_timer = 0

	else:
		player.air_timer += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if player.alive and (not end):
				if not game_state.mvt['d']:
					if event.key in game_state.controls['left']:
						game_state.mvt['l'] = True
						direction.append(2)

					elif event.key in game_state.controls['right']:
						game_state.mvt['r'] = True
						direction.append(1)

					elif event.key in game_state.controls['up']:
						if player.air_timer < 6:
							game_state.mvt['j'] = True
							player.gravity = -4.0

					elif event.key == pygame.K_q:
						sys.exit(-1)

					elif event.key == pygame.K_z:
						game_state.debug = not game_state.debug

				if (event.key == pygame.K_x or event.key == pygame.K_l) and game_state.mvt['j'] and dash_allow and not (not player.alive or end):
					if dashes > 0:
						player.hp -= player.max_hp * 0.25
						game_state.mvt['d'] = True
						dashes = 0

		elif event.type == pygame.KEYUP:
			if event.key in (pygame.K_a, pygame.K_LEFT):
				game_state.mvt['l'] = False

			if event.key in (pygame.K_d, pygame.K_RIGHT):
				game_state.mvt['r'] = False

	if idle_count + 1 >= len(idle_animation):
		idle_count = 0

	if run_count + 1 >= len(run_animation):
		run_count = 0

	if player.alive:
		if game_state.mvt['d']:
			if direction[-1] == 1:
				display.blit(jump_img, (player_.x - scroll[0], player_.y - scroll[1]))
			elif direction[-1] == 2:
				display.blit(pygame.transform.flip(jump_img, True, False), (player_.x - scroll[0], player_.y - scroll[1]))

		elif game_state.mvt['j']:
			jump_sound.play()

			if game_state.mvt['r']:
				display.blit(jump_img, (player_.x - scroll[0], player_.y - scroll[1]))

			elif game_state.mvt['l']:
				display.blit(pygame.transform.flip(jump_img, True, False), (player_.x - scroll[0], player_.y - scroll[1]))

			else:
				if direction[-1] == 1:
					display.blit(jump_img, (player_.x - scroll[0], player_.y - scroll[1]))
				elif direction[-1] == 2:
					display.blit(pygame.transform.flip(jump_img, True, False), (player_.x - scroll[0], player_.y - scroll[1]))

		elif not game_state.mvt['l'] and not game_state.mvt['r']:
			if direction[-1] == 1:
				display.blit(idle_animation[idle_count], (player_.x - scroll[0], player_.y - scroll[1]))
				idle_count += 1

			elif direction[-1] == 2:
				display.blit(pygame.transform.flip(idle_animation[idle_count], True, False), (player_.x - scroll[0], player_.y - scroll[1]))
				idle_count += 1

		elif game_state.mvt['r']:
			display.blit(run_animation[run_count], (player_.x + 1 - scroll[0], player_.y - scroll[1]))
			run_count += 1

		elif game_state.mvt['l']:
			display.blit(pygame.transform.flip(run_animation[run_count], True, False), (player_.x - 1 - scroll[0], player_.y - scroll[1]))
			run_count += 1

	if game_state.wait:
		game_state.wait_timer -= 1

	WIN.blit(pygame.transform.scale(display, (width, height)), (0, 0))
	pygame.display.update()
	clock.tick(game_state.fps)

	player.hp += player.max_hp / 1000

	if game_state.debug:
		dash_allow = True
		e = time.time()
		cnt = (cnt + e - s) * 0.5
		player.hp += player.max_hp / 1000
		print(f"FPS: {1 / (e - s)} | IGT: {e - game_state.last_death} | AVG FPS: {1 / cnt}")

	for x in alive:
		x.update()

	game_state.update()
