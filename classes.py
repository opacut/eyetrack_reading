import pygame
from pygame import mixer

class AreaOfInterest:
	def __init__(self, top_pos_x, top_pos_y, bot_pos_x, bot_pos_y, name, animation=None, sound=None):
		self.topleft = (top_pos_x, top_pos_y)
		self.bottomright = (bot_pos_x,bot_pos_y)
		self.name = name
		self.animation = animation
		self.sound = sound
		self.started = False

	def start(self):
		#if not self.running:
		if self.animation and not self.animation.running:
			self.animation.run()
			self.animation.running = True
		if self.sound and not self.sound.running:
			self.sound.run()
			self.sound.running = True
		self.started = True
		#self.running = True

	def update(self):
		if self.animation and self.animation.running:
			self.animation.update()
		if self.sound and self.sound.running:
			self.sound.update()

class Hit:
	def __init__(self, area, start_time):
		self.area = area
		self.start_time = start_time


freeChannels = [0,1,2,3,4,5,6,7,8,9]
def get_free_channel():
	return freeChannels.pop(0)

class SoundEffect:
	def __init__(self, volume, track):
		self.volume = volume
		self.track = track
		self.running = False

	def run(self):
		channel_number = get_free_channel()
		mixer.Channel(channel_number).set_volume(self.volume)
		mixer.Channel(channel_number).play(mixer.Sound(self.track))
		self.running = True

	def update(self):
		pass

class Animation:
	def __init__(self, spritesheet, frequency, position, screen):
		self.spritesheet = spritesheet
		self.frequency=frequency
		self.position = position
		self.screen = screen
		self.running = False

	def run(self):
		current_time = pygame.time.get_ticks()
		current_sprite_index = int((current_time/100)%10)
		self.screen.draw_image(self.spritesheet[current_sprite_index], pos=self.position)
	
	def update(self):
		self.run()
