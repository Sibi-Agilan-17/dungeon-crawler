import os
import pygame


__all__ = [
	"Speaker",
	"Gallery",
	"Map"
]


class Sound:
	def __init__(self, path, channel, volume=1.0):
		self.path = path
		self.volume = volume
		self.channel = channel
		self.channel.set_volume(volume)
		self.sound = pygame.mixer.Sound(path)

	def play(self, *args, **kwargs):
		self.channel.play(self.sound, *args, **kwargs)

	def is_playing(self) -> bool:
		return self.channel.get_busy()


class Speaker:
	def __init__(self, volume):
		self.num_channels = 4

		pygame.mixer.init()
		pygame.mixer.set_reserved(4)
		pygame.mixer.set_num_channels(self.num_channels)

		vol = volume['effects']
		volume = volume['background_music']

		self.channels = [pygame.mixer.Channel(x) for x in range(self.num_channels)]
		self.background_music = Sound('./assets/sounds/background music.mp3', channel=self.channels[1], volume=volume)
		self.jump_sound = Sound('./assets/sounds/jump.mp3', channel=self.channels[2], volume=vol)
		self.next_level_sound = Sound('./assets/sounds/next level.mp3', channel=self.channels[3], volume=vol)


def _load_image(img_name):
	return pygame.image.load(img_name).convert_alpha()


class Gallery:
	def __init__(self):
		self.player_idle_images = []
		self.player_run_images = []
		self.layer1_images = []
		self.layer2_images = []
		self.layer3_images = []

		for i in range(1, 6):
			idle_img = _load_image(os.path.join('assets', 'images', 'idle_animation', 'Idle ' + str(i) + '.png'))
			self.player_idle_images.append(idle_img)

		for i in range(1, 8):
			run_img = _load_image(os.path.join('assets', 'images', 'run_animation', 'Run ' + str(i) + '.png'))
			self.player_run_images.append(run_img)

		for i in range(1, 7):
			sprite_img = _load_image(os.path.join('assets', 'images', 'tiles', 'layer1_tiles', 'Sprite_' + str(i) + '.png'))
			self.layer1_images.append(sprite_img)

		for i in range(7, 16):
			sprite_img = _load_image(os.path.join('assets', 'images', 'tiles', 'layer2_tiles', 'Sprite_' + str(i) + '.png'))
			self.layer2_images.append(sprite_img)

		for i in range(16, 24):
			sprite_img = _load_image(os.path.join('assets', 'images', 'tiles', 'layer3_tiles', 'Sprite_' + str(i) + '.png'))
			self.layer3_images.append(sprite_img)

		self.player_jump_img = _load_image(os.path.join('assets', 'images', 'jump_animation', 'Jump.png'))
		self.lava_img = _load_image(os.path.join('assets', 'images', 'texture', 'lava.png'))

		self.player_idle_animation = self._animate(self.player_idle_images, 12)
		self.player_run_animation = self._animate(self.player_run_images, 6)

	@staticmethod
	def _animate(frames, frame_duration):
		animation = []
		for u in range(len(frames)):
			for v in range(frame_duration):
				animation.append(frames[u])
		return animation


def _load_map(path):
	file = open('./assets/level_data/' + path + '.txt', 'r')
	data = file.read()
	file.close()
	data = data.split('\n')
	game_map = []

	for line in data:
		game_map.append(list(line))

	return game_map


class Map:
	def __init__(self):
		self.layers = []

		self.layers.append([_load_map('level1_layer1'), _load_map('level1_layer2'), _load_map('level1_layer3')])
		self.layers.append([_load_map('level2_layer1'), _load_map('level2_layer2'), _load_map('level2_layer3')])
		self.layers.append([_load_map('level3_layer1'), _load_map('level3_layer2'), _load_map('level3_layer3')])
