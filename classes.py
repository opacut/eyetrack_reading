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
		if mixer.Channel(self.channel_number).get_busy():
			mixer.Channel(self.channel_number).unpause()
		else:
			mixer.Channel(self.channel_number).play(mixer.Sound(self.track))

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
			if self.current_scene == "8":
				self.load_scene(name="1")
			else:
				new_scene_number = int(self.current_scene)+1
				self.load_scene(name=str(new_scene_number))
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
		mixer.init()
		self.freeChannels = [0,1,2,3,4,5,6,7,8,9]
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
			self.background_path="media/image/komix/1.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=286,top_pos_y=67,
					bot_pos_x=546,bot_pos_y=366,
					name="1 cinely", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/1 cinely.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=564,top_pos_y=76,
					bot_pos_x=747,bot_pos_y=403,
					name="2 sklouznuti", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/2 sklouznuti.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=294,top_pos_y=471,
					bot_pos_x=498,bot_pos_y=727,
					name="3 odchod", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/3 odchod.ogg")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=636,top_pos_y=469,
					bot_pos_x=919,bot_pos_y=688,
					name="4 rany", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/4 rany.ogg")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1366,top_pos_y=409,
					bot_pos_x=1623,bot_pos_y=581,
					name="5 zahada", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/5 zahada.ogg")
				)
			)
		elif name=="2":
			self.current_scene = "2"
			self.background_path="media/image/komix/2.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=351,top_pos_y=500,
					bot_pos_x=798,bot_pos_y=831,
					name="6 zdeseni", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/6 zdeseni.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1219,top_pos_y=684,
					bot_pos_x=1575,bot_pos_y=949,
					name="7 premysleni", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/7 premysleni.mp3")
				)
			)
		elif name=="3":
			self.current_scene = "3"
			self.background_path="media/image/komix/3.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=508,top_pos_y=155,
					bot_pos_x=638,bot_pos_y=297,
					name="8 zamykani", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/8 zamykani.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=824,top_pos_y=175,
					bot_pos_x=1580,bot_pos_y=586,
					name="9 chuze v desti", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/9 chuze v desti.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=845,top_pos_y=670,
					bot_pos_x=1591,bot_pos_y=968,
					name="10 splouch", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/10 splouch.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1001,top_pos_y=219,
					bot_pos_x=1418,bot_pos_y=330,
					name="extra splouch", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/10 splouch.wav")
				)
			)
		elif name=="4":
			self.current_scene = "4"
			self.background_path="media/image/komix/4.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1005,top_pos_y=222,
					bot_pos_x=1371,bot_pos_y=410,
					name="11 praskani ohne", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/11 praskani ohne.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=340,top_pos_y=406,
					bot_pos_x=1045,bot_pos_y=958,
					name="12 odezva", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/12 odezva.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1058,top_pos_y=604,
					bot_pos_x=1567,bot_pos_y=982,
					name="13 padlovani", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/13 padlovani.wav")
				)
			)
		elif name=="5":
			self.current_scene = "5"
			self.background_path="media/image/komix/5.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=763,top_pos_y=343,
					bot_pos_x=1156,bot_pos_y=456,
					name="14 splouch", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/14 splouch.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=342,top_pos_y=478,
					bot_pos_x=723,bot_pos_y=730,
					name="15 leknuti", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/15 leknuti.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=348,top_pos_y=748,
					bot_pos_x=980,bot_pos_y=948,
					name="16 jizda na lodi", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/16 jizda na lodi.wav")
				)
			)
		elif name=="6":
			self.current_scene = "6"
			self.background_path="media/image/komix/6.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=939,top_pos_y=111,
					bot_pos_x=1547,bot_pos_y=447,
					name="17 ozvena", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/17 ozvena.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=354,top_pos_y=452,
					bot_pos_x=1553,bot_pos_y=752,
					name="18 zmizeni", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/18 zmizeni.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=373,top_pos_y=764,
					bot_pos_x=1217,bot_pos_y=935,
					name="19 beh", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/19 beh.flac")
				)
			)
		elif name=="7":
			self.current_scene = "7"
			self.background_path="media/image/komix/7.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=379,top_pos_y=112,
					bot_pos_x=1526,bot_pos_y=371,
					name="21 aaaaa", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/21 aaaaa.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=772,top_pos_y=624,
					bot_pos_x=1052,bot_pos_y=956,
					name="22 hop", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/22 hop.wav")
				)
			)
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=1147,top_pos_y=624,
					bot_pos_x=1469,bot_pos_y=951,
					name="23 uf", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/23 uf.wav")
				)
			)
		elif name=="8":
			self.current_scene = "8"
			self.background_path="media/image/komix/8.jpg"
			self.registered_objects.append(
				AreaOfInterest(
					gc=self,
					top_pos_x=455,top_pos_y=369,
					bot_pos_x=1469,bot_pos_y=951,
					name="24 rozlouceni", 
					sound=SoundEffect(gc=self, volume=0.5, track="media/sounds/komix_sounds/24 rozlouceni.wav")
				)
			)
		else:
			raise Exception
		self.background_image = pygame.image.load(self.background_path)

	def get_free_channel(self):
		return self.freeChannels.pop(0)

