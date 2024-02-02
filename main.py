import pygame
import random
import sys
import time

from game import GameEngine

engine = GameEngine()
game_state = engine.game_state
gallery = engine.gallery
player = engine.player
layers = engine.map.layers
display = engine.display

layer1_images = gallery.layer1_images
layer2_images = gallery.layer2_images
layer3_images = gallery.layer3_images

death_animation = False

idle_count = 0
run_count = 0
door = pygame.Rect(1000, 1000, 1, 1)

death_images = []
particles = []
direction = [1]

# Game Loop
engine.speaker.background_music.play()
game_state.last_death = time.time()

while engine.RUN:
	engine.speaker.background_music.play()

	engine.display.fill((28, 31, 36))
	collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

	engine.true_scroll[0] += (player.hitbox.x - engine.true_scroll[0] - 165) / 15
	engine.true_scroll[1] += (player.hitbox.y - engine.true_scroll[1] - 236) / 15

	scroll = engine.true_scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

	tiles = []
	spikes = []
	platforms = []

	if game_state.level > 2:
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
						display.blit(gallery.lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
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
						display.blit(gallery.lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
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
						display.blit(gallery.lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
						game_state.lava_blocks.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile != '0' and tile != '5' and tile != '6' and tile != '7' and tile != '8' and tile != '9' and tile != 'l':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))
					x += 1
				y += 1

	for spike in spikes:
		if player.hitbox.colliderect(spike):
			player.hp -= game_state.damage_map['spikes'] // 10

	for lava_block in game_state.lava_blocks:
		if player.hitbox.colliderect(lava_block):
			player.hp -= game_state.damage_map['lava']

	movement = [0, 0]

	if engine.RUN:
		if player.alive:
			if game_state.mvt['l']:
				movement[0] -= player.linear_travel_speed
			if game_state.mvt['r']:
				movement[0] += player.linear_travel_speed

			movement[1] += player.gravity
			player.gravity += 0.2

	collisions = player.move(collision_types, movement, tiles)

	if player.hitbox.colliderect(door):
		engine.speaker.next_level_sound.play()
		player.reset_stats()
		game_state.last_death = time.time()

		game_state.level += 1

		if not game_state.level <= game_state.max_level:
			game_state.level = 1

		y = 0

		for row in layers[game_state.level - 1][0]:
			x = 0
			for tile in row:
				if tile == '7':
					player.respawn[0] = 16 * x
					player.respawn[1] = 16 * y
				x += 1
			y += 1

		player.x = player.respawn[0] - 16
		player.y = player.respawn[1] - 16

		continue

	plat_col = []
	for platform in platforms:
		if player.hitbox.colliderect(platform):
			plat_col.append(platform)

	for tile in plat_col:
		if movement[1] > 0:
			player.hitbox.bottom = tile.top
			collision_types['bottom'] = True

	if not player.alive:
		player.gravity = 0

		player.hitbox.x = player.respawn[0]
		player.hitbox.y = player.respawn[1]
		player.alive = True
		player.reset_stats()
		game_state.last_death = time.time()

		oe = 2

		if len(particles) == 0 and oe == 1:
			for num in range(30):
				particles.append([[(player.hitbox.center[0] - scroll[0]), (player.hitbox.center[1] - scroll[1])], [random.randint(0, 30) / 10 - 1.5, random.randint(0, 10) / 6 - 3], random.randint(3, 5)])

		for particle in particles:
			particle[0][0] += particle[1][0]
			particle[0][1] += particle[1][1] - 0.5
			particle[2] -= 0.05
			particle[1][1] += 0.035
			pygame.draw.circle(display, (255, 0, 50), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

	if player.alive:
		particles.clear()

		pygame.draw.rect(display, "red", (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1] - 8, 32, 4))
		pygame.draw.rect(display, "green", (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1] - 8, 32 * player.hp / player.max_hp, 4))

	if collision_types['bottom']:
		grav = 0
		game_state.mvt['j'] = False

		if player.air_timer > 50:
			player.hp -= game_state.damage_map['fall'] * player.air_timer // 10

		player.air_timer = 0

	else:
		player.air_timer += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if player.alive and engine.RUN:
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

		elif event.type == pygame.KEYUP:
			if event.key in game_state.controls['left']:
				game_state.mvt['l'] = False

			if event.key in game_state.controls['right']:
				game_state.mvt['r'] = False

	if idle_count + 1 >= len(gallery.idle_animation):
		idle_count = 0

	if run_count + 1 >= len(gallery.run_animation):
		run_count = 0

	if player.alive:
		if game_state.mvt['j']:
			engine.speaker.jump_sound.play()

			if game_state.mvt['r']:
				display.blit(gallery.jump_img, (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))

			elif game_state.mvt['l']:
				display.blit(pygame.transform.flip(gallery.jump_img, True, False), (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))

			else:
				if direction[-1] == 1:
					display.blit(gallery.jump_img, (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))
				elif direction[-1] == 2:
					display.blit(pygame.transform.flip(gallery.jump_img, True, False), (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))

		elif not game_state.mvt['l'] and not game_state.mvt['r']:
			if direction[-1] == 1:
				display.blit(gallery.idle_animation[idle_count], (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))
				idle_count += 1

			elif direction[-1] == 2:
				display.blit(pygame.transform.flip(gallery.idle_animation[idle_count], True, False), (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))
				idle_count += 1

		elif game_state.mvt['r']:
			display.blit(gallery.run_animation[run_count], (player.hitbox.x + 1 - scroll[0], player.hitbox.y - scroll[1]))
			run_count += 1

		elif game_state.mvt['l']:
			display.blit(pygame.transform.flip(gallery.run_animation[run_count], True, False), (player.hitbox.x - 1 - scroll[0], player.hitbox.y - scroll[1]))
			run_count += 1

	engine.WIN.blit(pygame.transform.scale(display, engine.WIN_DIMENSIONS), (0, 0))
	pygame.display.update()
	engine.tick()
