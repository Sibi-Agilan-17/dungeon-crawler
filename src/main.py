import datetime
import logging
import sys

import pygame

import game

final_time = None
freeze_time = False

engine = game.GameEngine()
gallery = engine.gallery
player = engine.player
layers = engine.map.layers
display = engine.display

layer1_images = gallery.layer1_images
layer2_images = gallery.layer2_images
layer3_images = gallery.layer3_images

engine.speaker.background_music.play(loops=-1)

logging.info("Starting game")

while True:
	collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

	engine.display.fill((28, 31, 36))

	engine.scroll[0] += (player.hitbox.x - engine.scroll[0] - 165) / 15
	engine.scroll[1] += (player.hitbox.y - engine.scroll[1] - 236) / 15

	scroll = engine.scroll.copy()
	scroll[0] = int(scroll[0])
	scroll[1] = int(scroll[1])

	lava = []
	tiles = []
	spikes = []
	movement = [0, 0]

	if not engine.level <= 3:
		logging.info("Freezing time")

		freeze_time = True
		final_time = datetime.datetime.now()
		engine.level = -1

	for layer in layers[engine.level - 1]:
		y = 0

		if layer == layers[engine.level - 1][0]:
			for row in layer:
				x = 0
				for tile in row:
					if 0 < int(tile):
						if int(tile) < 7:
							display.blit(layer1_images[int(tile) - 1], (16 * x - scroll[0], 16 * y - scroll[1]))
						else:
							display.blit(layer1_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))

					if tile not in '0127':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))

					x += 1
				y += 1

		if layer == layers[engine.level - 1][1]:
			for row in layer:
				x = 0
				for tile in row:
					if tile == '1':
						display.blit(layer2_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '2':
						display.blit(layer2_images[1], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '3':
						display.blit(layer2_images[2], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '4':
						display.blit(layer2_images[3], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '5':
						display.blit(layer2_images[4], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '6':
						display.blit(layer2_images[5], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '7':
						display.blit(layer2_images[6], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '8':
						display.blit(layer2_images[7], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '9':
						display.blit(layer2_images[8], (16 * x - scroll[0], 16 * y - scroll[1]))
						engine.doors.append(pygame.Rect(16 * x, 16 * y, 16, 32))
					elif tile == 'l':
						display.blit(gallery.lava_img, (16 * x - scroll[0], 16 * y - scroll[1]))
						lava.append(pygame.Rect(16 * x, 16 * y, 16, 4))

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
					elif tile == '2':
						display.blit(layer3_images[1], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '3':
						display.blit(layer3_images[2], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '4':
						display.blit(layer3_images[3], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '5':
						display.blit(layer3_images[4], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x, 16 * y + 6, 16, 10))
					elif tile == '6':
						display.blit(layer3_images[5], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x, 16 * y, 10, 16))
					elif tile == '7':
						display.blit(layer3_images[6], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x, 16 * y - 6, 16, 10))
					elif tile == '8':
						display.blit(layer3_images[7], (16 * x - scroll[0], 16 * y - scroll[1]))
						spikes.append(pygame.Rect(16 * x + 6, 16 * y, 10, 16))

					if tile not in '05678':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))
					x += 1
				y += 1

	for spike in spikes:
		if player.hitbox.colliderect(spike):
			damage = engine.damage_map['spikes']

			logging.info(f"Spike damage: {damage}")
			player.hp -= damage

	for lava_block in lava:
		if player.hitbox.colliderect(lava_block):
			damage = engine.damage_map['lava']

			logging.info(f"Lava damage: {damage}")
			player.hp -= damage

	collisions = player.move(collision_types, engine.calc_movement(), tiles)

	if player.alive:
		if engine.debug and engine.igt :
			time_str = "IGT:  " + str((final_time if freeze_time else datetime.datetime.now()) - engine.igt)[2:11]
			display.blit(engine.font.render(time_str, False, engine.font_color), (400, 0))

	if engine.RUN and collision_types['bottom']:
		engine.mvt['j'] = False

		if player.air_time > 1:
			engine.speaker.jump_sound.play()

			if player.air_time > 64:
				fall_damage = engine.damage_map['fall'] * player.velocity_vector.magnitude_squared()

				logging.info(f"Fall damage: {fall_damage}")
				player.hp -= fall_damage

		player.air_time = 0

	else:
		player.air_time += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				sys.exit(-1)

			elif event.key == pygame.K_r:
				final_time = None
				freeze_time = False

				engine = game.GameEngine()
				player = engine.player
				display = engine.display

			elif event.key == pygame.K_z:
				engine.debug = not engine.debug

			if player.alive and engine.RUN:
				if event.key in engine.controls['left']:
					engine.mvt['l'] = True
					player.facing_right = False

					if not engine.igt:
						engine.igt = datetime.datetime.now()

				elif event.key in engine.controls['right']:
					engine.mvt['r'] = True
					player.facing_right = True

					if not engine.igt:
						engine.igt = datetime.datetime.now()

				elif event.key in engine.controls['up']:
					if player.air_time < 6:
						engine.mvt['j'] = True
						player.velocity_vector.y = -4.0

					if not engine.igt:
						engine.igt = datetime.datetime.now()

		elif event.type == pygame.KEYUP:
			if event.key in engine.controls['left']:
				player.velocity_vector.x = 0
				engine.mvt['l'] = False

			if event.key in engine.controls['right']:
				player.velocity_vector.x = 0
				engine.mvt['r'] = False

	if player.alive and engine.RUN:
		default_scroll = (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1])

		if engine.mvt['j']:
			if player.facing_right:
				display.blit(gallery.player_jump_img, default_scroll)
			else:
				display.blit(pygame.transform.flip(gallery.player_jump_img, True, False), default_scroll)

		elif not engine.mvt['l'] and not engine.mvt['r']:
			player.idle_count += 1

			if player.facing_right:
				display.blit(player.idle_animation[player.idle_count], default_scroll)
			else:
				display.blit(pygame.transform.flip(player.idle_animation[player.idle_count], True, False),
							 default_scroll)

		elif player.facing_right:
			display.blit(player.run_animation[player.run_count], (default_scroll[0] + 1, default_scroll[1]))
			player.run_count += 1

		else:
			display.blit(pygame.transform.flip(player.run_animation[player.run_count], True, False),
						 (default_scroll[0] - 1, default_scroll[1]))
			player.run_count += 1

	engine.pre_update()
	engine.WIN.blit(pygame.transform.scale(display, engine.WIN_DIMENSIONS), (0, 0))
	pygame.display.flip()
	engine.update()
