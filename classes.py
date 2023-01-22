import pygame
from pygame import mixer


class AreaOfInterest:
	def __init__(self, gc, top_pos_x, top_pos_y, bot_pos_x, bot_pos_y, name, animation=None, sound=None):
		self.gc = gc
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


class SoundEffect:
	def __init__(self, gc, volume, track):
		self.gc = gc
		self.volume = volume
		self.track = track
		self.running = False

	def run(self):
		self.channel_number = self.gc.get_free_channel()
		mixer.Channel(self.channel_number).set_volume(self.volume)
		mixer.Channel(self.channel_number).play(mixer.Sound(self.track))
		self.running = True

	def update(self):
		mixer.Channel(self.channel_number).unpause()

class Animation:
	def __init__(self, gc, spritesheet, frequency, position):
		self.gc = gc
		self.spritesheet = spritesheet
		self.frequency=frequency
		self.position = position
		self.running = False

	def run(self):
		current_time = pygame.time.get_ticks()
		current_sprite_index = int((current_time/100)%10)
		self.gc.screen.draw_image(self.spritesheet[current_sprite_index], pos=self.position)
	
	def update(self):
		self.run()

class GameController:
	def __init__(self, keyboard, display, screen, eyetracker, scene_name):
		mixer.init()
		mixer.set_num_channels(10)
		self.keyboard = keyboard
		self.display = display
		self.screen = screen
		self.eyetracker = eyetracker
		self.freeChannels = [0,1,2,3,4,5,6,7,8,9]
		self.load_scene(name=scene_name)
		self.running = True
		#self.current_scene = None
		self.background_path = None

	
	def process_control(self, key):
		if key[0] != None:
			print(key)
		if key[0] == 'space':
			self.stop_all()
			if self.current_scene == "1":
				self.load_scene(name="2")
			elif self.current_scene == "2":
				self.load_scene(name="1")
		if key[0] == 'escape':
			self.running = False

	def pause_all(self):
		#for i in range(len(self.freeChannels)):
			#mixer.fadeout(i)
			#mixer.stop()
		mixer.pause()
	
	def stop_all(self):
		mixer.stop()

	def load_scene(self, name):
		self.registered_objects = []
		self.registered_objects.append(
			AreaOfInterest(
				gc=self,
				top_pos_x=0, top_pos_y=0,
				bot_pos_x=0, bot_pos_y=0,
				name="None"
			)
		)
		if name=="default":
			self.current_scene = "default"
			self.background_path="media/image/cafeteria.png"
			self.coffee_sprites = []
			self.current_coffee_sprite = 0
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/1.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/2.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/3.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/4.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/5.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/6.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/7.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/8.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/9.png'))
			self.coffee_sprites.append(pygame.image.load('media/anim/coffee_anim/10.png'))
			self.playing_anim = False

            # build default scene
            # register and define all the areas of interest used
            # the values are hard-coded at the moment. Modify according to the display size used.
            # see objects.txt for different resolutions
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1031,top_pos_y=279,
					bot_pos_x=1112,bot_pos_y=463,
					name="Coffee",
					animation=Animation(gc=self,spritesheet=self.coffee_sprites, frequency=8, position=(1100,300))
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1157,top_pos_y=244,
					bot_pos_x=1294,bot_pos_y=378,
					name="Music", 
					sound=SoundEffect(gc=self, volume=0.7, track="media/sounds/City-Life.mp3")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=702,top_pos_y=508,
					bot_pos_x=1012,bot_pos_y=848,
					name="People", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/people.mp3")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=450,top_pos_y=154,
					bot_pos_x=684,bot_pos_y=648,
					name="Street", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/street.mp3")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=793, top_pos_y=225,
					bot_pos_x=857, bot_pos_y=276,
					name="Sign1"
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=773, top_pos_y=368,
					bot_pos_x=819, bot_pos_y=428,
					name="Sign2"
				)
			)
		elif name=="1":
			self.current_scene = "1"
			self.background_path="media/image/img001.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=602,top_pos_y=60,
					bot_pos_x=1291,bot_pos_y=333,
					name="Steps", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/steps.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=593,top_pos_y=367,
					bot_pos_x=1278,bot_pos_y=617,
					name="Interior", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/interior.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=599,top_pos_y=638,
					bot_pos_x=955,bot_pos_y=1000,
					name="Interior2", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/interior.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=967,top_pos_y=633,
					bot_pos_x=1261,bot_pos_y=1002,
					name="Woof", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/woof.wav")
				)
			)
		elif name=="2":
			self.current_scene = "2"
			self.background_path="media/image/img002.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=620,top_pos_y=354,
					bot_pos_x=1305,bot_pos_y=634,
					name="Steps2", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/steps2.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=622,top_pos_y=47,
					bot_pos_x=1299,bot_pos_y=356,
					name="Whine", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/whine.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=896,top_pos_y=638,
					bot_pos_x=1299,bot_pos_y=1007,
					name="Scare", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/scare.mp3")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=999,top_pos_y=366,
					bot_pos_x=1292,bot_pos_y=628,
					name="Howl", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/howl.mp3")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=626,top_pos_y=641,
					bot_pos_x=895,bot_pos_y=1017,
					name="Howl2", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/howl.mp3")
				)
			)
		else:
			raise Exception
		self.background_image = pygame.image.load(self.background_path)

	def get_free_channel(self):
		return self.freeChannels.pop(0)

