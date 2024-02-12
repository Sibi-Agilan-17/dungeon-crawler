import datetime
import math

import pygame
import sys

from game import GameEngine

engine = GameEngine()
gallery = engine.gallery
player = engine.player
layers = engine.map.layers
display = engine.display

layer1_images = gallery.layer1_images
layer2_images = gallery.layer2_images
layer3_images = gallery.layer3_images

WRITE_DATA = pygame.USEREVENT + 1
pygame.time.set_timer(WRITE_DATA, 1000)  # write data every second
freeze_time = False
final_time = None

while True:
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

	if not engine.level <= engine.max_level:
		freeze_time = True
		final_time = datetime.datetime.now()
		engine.level = 1

	for layer in layers[engine.level - 1]:
		y = 0

		if layer == layers[engine.level - 1][0]:
			for row in layer:
				x = 0
				for tile in row:
					if tile == '1':
						display.blit(layer1_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '2':
						display.blit(layer1_images[1], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '3':
						display.blit(layer1_images[2], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '4':
						display.blit(layer1_images[3], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '5':
						display.blit(layer1_images[4], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '6':
						display.blit(layer1_images[5], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == '7':
						display.blit(layer1_images[0], (16 * x - scroll[0], 16 * y - scroll[1]))
					elif tile == 'l':
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

					if tile not in '056789':
						tiles.append(pygame.Rect(16 * x, 16 * y, 16, 16))
					x += 1
				y += 1

	for spike in spikes:
		if player.hitbox.colliderect(spike):
			player.hp -= engine.damage_map['spikes'] // 10
			engine.score -= (engine.damage_map['spikes'] // 10) * 0.1

	for lava_block in engine.lava_blocks:
		if player.hitbox.colliderect(lava_block):
			player.hp -= engine.damage_map['lava']
			engine.score -= (engine.damage_map['lava'] // 10) * 0.1

	if engine.RUN:
		if player.alive:
			if engine.mvt['l'] or engine.mvt['r']:
				player.velocity_vector.x += player.linear_travel_speed / 2.1414

				if engine.mvt['l']:
					movement[0] -= player.velocity_vector.x
				else:
					movement[0] += player.velocity_vector.x

			movement[1] += player.velocity_vector.y
			player.velocity_vector.y += engine.gravitational_vector.y

	collisions = player.move(collision_types, movement, tiles)

	if player.alive:
		pygame.draw.rect(display, "red", (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1] - 8, 32, 4))
		pygame.draw.rect(display, "green", (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1] - 8, 32 * player.hp / player.max_hp, 4))

		if engine.debug:
			display.blit(engine.font.render(f"Score: {engine.score}", False, (211, 211, 211)), (0, 0))

			if engine.igt:
				time_now = final_time if freeze_time else datetime.datetime.now()
				igt = time_now - engine.igt

				color = (255, 215, 0) if (freeze_time and not engine.controls['cheats']) else(211, 211, 211)
				display.blit(engine.font.render("IGT:  " + str(igt)[2:11], False, color), (0, 24))

	else:
		engine.reset_stats()
		player.reset_stats(coordinates=engine.get_spawn_coordinates())

	if collision_types['bottom']:
		engine.mvt['j'] = False

		if player.air_time > 1:
			engine.speaker.jump_sound.play()

			if player.air_time > 64:
				fall_damage = pygame.math.clamp(engine.damage_map['fall'] * player.velocity_vector.magnitude(), 0, player.max_hp)

				player.hp -= fall_damage
				engine.score -= fall_damage

		player.air_time = 0

	else:
		player.air_time += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if not engine.igt:
				engine.igt = datetime.datetime.now()

			if player.alive and engine.RUN:
				if event.key in engine.controls['left']:
					engine.mvt['l'] = True
					player.facing_right = False

				elif event.key in engine.controls['right']:
					engine.mvt['r'] = True
					player.facing_right = True

				elif event.key in engine.controls['up']:
					if player.air_time < 6:
						engine.mvt['j'] = True
						player.velocity_vector.y -= player.linear_travel_speed * 2

				elif event.key in engine.controls['cheats']:
					if player.hp > player.max_hp * 0.95:
						engine.damage_map = {k: 0 for k, _ in engine.damage_map.items()}
					else:
						player.hp = player.max_hp

				elif event.key == pygame.K_r:
					engine.RUN = False
					engine.reset_stats()
					player.reset_stats(coordinates=engine.get_spawn_coordinates())

				elif event.key == pygame.K_q:
					sys.exit(-1)

				elif event.key == pygame.K_z:
					engine.debug = not engine.debug

		elif event.type == pygame.KEYUP:
			if event.key in engine.controls['left']:
				player.velocity_vector.x = 0
				engine.mvt['l'] = False

			if event.key in engine.controls['right']:
				player.velocity_vector.x = 0
				engine.mvt['r'] = False

		elif event.type == WRITE_DATA:
			# todo: implement save states
			...

	if player.alive:
		if engine.mvt['j']:
			if player.facing_right:
				display.blit(gallery.player_jump_img, (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))

			else:
				display.blit(pygame.transform.flip(gallery.player_jump_img, True, False), (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))

		elif not engine.mvt['l'] and not engine.mvt['r']:
			if player.facing_right:
				display.blit(player.idle_animation[player.idle_count], (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))
				player.idle_count += 1

			else:
				display.blit(pygame.transform.flip(player.idle_animation[player.idle_count], True, False), (player.hitbox.x - scroll[0], player.hitbox.y - scroll[1]))
				player.idle_count += 1

		elif player.facing_right:
			display.blit(player.run_animation[player.run_count], (player.hitbox.x + 1 - scroll[0], player.hitbox.y - scroll[1]))
			player.run_count += 1

		else:
			display.blit(pygame.transform.flip(player.run_animation[player.run_count], True, False), (player.hitbox.x - 1 - scroll[0], player.hitbox.y - scroll[1]))
			player.run_count += 1

		engine.WIN.blit(pygame.transform.scale(display, engine.WIN_DIMENSIONS), (0, 0))
		pygame.display.update()

	engine.score = int(pygame.math.clamp(engine.score, 0, math.inf))
	engine.tick()
