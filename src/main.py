import datetime

import pygame
import sys
import time

from game import GameEngine

engine = GameEngine()
gallery = engine.gallery
player = engine.player
layers = engine.map.layers
display = engine.display
memory = engine.memory

layer1_images = gallery.layer1_images
layer2_images = gallery.layer2_images
layer3_images = gallery.layer3_images

invisible = False
idle_count = 0
run_count = 0
door = pygame.Rect(1000, 1000, 1, 1)

direction = [1]
visible = pygame.USEREVENT + 1
WRITE_DATA = pygame.USEREVENT + 2

engine.speaker.background_music.play()
pygame.time.set_timer(WRITE_DATA, 1000)

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
	movement = [0, 0]

	for layer in layers[engine.level - 1]:
		y = 0

		if layer == layers[engine.level - 1][0]:
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
						engine.lava_blocks.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile not in '0127l':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))

					x += 1
				y += 1

		if layer == layers[engine.level - 1][1]:
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
						engine.lava_blocks.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile not in '09l':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))
					x += 1
				y += 1

		if layer == layers[engine.level - 1][2]:
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
					if tile == 'l':
						display.blit(gallery.lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
						engine.lava_blocks.append(pygame.Rect(16 * x, 16 * y, 16, 4))
					if tile not in '056789l':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))
					x += 1
				y += 1

	for spike in spikes:
		if player.hitbox.colliderect(spike):
			player.hp -= engine.damage_map['spikes'] // 10

	for lava_block in engine.lava_blocks:
		if player.hitbox.colliderect(lava_block):
			player.hp -= engine.damage_map['lava']

	if engine.RUN:
		if player.alive:
			if engine.mvt['l'] or engine.mvt['r']:
				player.velocity += player.linear_travel_speed / 2.1414

				if engine.mvt['l']:
					movement[0] -= player.velocity
				else:
					movement[0] += player.velocity

			movement[1] += player.gravity
			player.gravity += 0.2

	collisions = player.move(collision_types, movement, tiles)

	if player.hitbox.colliderect(door):
		engine.speaker.next_level_sound.play()
		player.reset_stats()

		engine.level += 1
		memory.data['score'] += 100

		if not engine.level <= engine.max_level:
			engine.level = 1

		y = 0

		for row in layers[engine.level - 1][0]:
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

	if player.alive:
		pygame.draw.rect(display, "red", (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1] - 8, 32, 4))
		pygame.draw.rect(display, "green", (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1] - 8, 32 * player.hp / player.max_hp, 4))
		display.blit(engine.font.render(f"Score: {memory.data['score']}", False, (211, 211, 211)), (0, 0))

		time_since_last_death = int(time.time()) - memory.data['last-death']

		days = time_since_last_death // 86400
		hours = time_since_last_death // 3600 % 24
		minutes = time_since_last_death // 60 % 60
		seconds = time_since_last_death % 60

		st = ""

		if not days > 1:
			if not hours > 1:
				if not minutes > 1:
					if not seconds > 1:
						st = "Now"
					else:
						st = f"{seconds} seconds ago"
				else:
					st = f"{minutes} minutes ago"
			else:
				st = f"{hours} hours ago"
		else:
			st = f"{days} days ago"

			if days > 365:
				st = "Never ;)"

		display.blit(engine.font.render("Last death: " + st, False, (211, 211, 211)), (0, 24))

	else:
		player.gravity = 0
		invisible = True
		pygame.time.set_timer(visible, 500)
		memory.data['last-death'] = int(time.time())

		player.hitbox.x = player.respawn[0]
		player.hitbox.y = player.respawn[1]
		player.alive = True
		player.reset_stats()

	if collision_types['bottom']:
		engine.mvt['j'] = False

		if player.air_time > 1:
			engine.speaker.jump_sound.play()

			if player.air_time > 50:
				player.hp -= engine.damage_map['fall'] * player.air_time // 10

		player.air_time = 0

	else:
		player.air_time += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if player.alive and engine.RUN:
				if event.key in engine.controls['left']:
					engine.mvt['l'] = True
					player.facing_right = False
					direction.append(2)

				elif event.key in engine.controls['right']:
					engine.mvt['r'] = True
					player.facing_right = True
					direction.append(1)

				elif event.key in engine.controls['up']:
					if player.air_time < 6:
						engine.mvt['j'] = True
						player.gravity = -4.0

				elif event.key == pygame.K_q:
					sys.exit(-1)

		elif event.type == pygame.KEYUP:
			if event.key in engine.controls['left']:
				player.velocity = 0
				engine.mvt['l'] = False

			if event.key in engine.controls['right']:
				player.velocity = 0
				engine.mvt['r'] = False

		elif event.type == visible:
			invisible = False

		elif event.type == WRITE_DATA:
			memory.write_data()

	if idle_count + 1 >= len(player.idle_animation):
		idle_count = 0

	if run_count + 1 >= len(player.run_animation):
		run_count = 0

	if player.alive and not invisible:
		if engine.mvt['j']:
			if player.facing_right:
				display.blit(gallery.jump_img, (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))

			else:
				display.blit(pygame.transform.flip(gallery.jump_img, True, False), (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))

		elif not engine.mvt['l'] and not engine.mvt['r']:
			if player.facing_right:
				display.blit(player.idle_animation[idle_count], (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))
				idle_count += 1

			else:
				display.blit(pygame.transform.flip(player.idle_animation[idle_count], True, False), (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))
				idle_count += 1

		elif player.facing_right:
			display.blit(player.run_animation[run_count], (player.hitbox.x + 1 - scroll[0], player.hitbox.y - scroll[1]))
			run_count += 1

		else:
			display.blit(pygame.transform.flip(player.run_animation[run_count], True, False), (player.hitbox.x - 1 - scroll[0], player.hitbox.y - scroll[1]))
			run_count += 1

		engine.WIN.blit(pygame.transform.scale(display, engine.WIN_DIMENSIONS), (0, 0))
		pygame.display.update()

	engine.tick()
