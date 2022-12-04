import pygame
from constants import *

#from pygaze import libtime

from pygame import mixer
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.libscreen import Display 
from pygaze.libscreen import Screen

from classes import Animation
from classes import AreaOfInterest
from classes import Hit
from classes import SoundEffect

# set up objects
keyboard = Keyboard()
disp = Display()
screen = Screen()
blankscreen = Screen()
eyetracker = EyeTracker(disp)

eyetracker.calibrate()

background_image = pygame.image.load('cafeteria.png')

gazepos = [0,0]
last_collision = None
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
old_diff = 0
playing = False
playing_music = False
playing_people = False
playing_street = False

# music
mixer.init()
mixer.set_num_channels(10)

# load spritesheeet for the coffee animation
coffee_sprites = []
current_coffee_sprite = 0
coffee_sprites.append(pygame.image.load('anim/coffee_anim/1.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/2.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/3.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/4.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/5.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/6.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/7.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/8.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/9.png'))
coffee_sprites.append(pygame.image.load('anim/coffee_anim/10.png'))
playing_anim = False

# register and define all the areas of interest used
registered_objects = []
registered_objects.append(
	AreaOfInterest(
		top_pos_x=0, top_pos_y=0,
		bot_pos_x=0, bot_pos_y=0,
		name="None"
	)
)
registered_objects.append(
	AreaOfInterest(
		top_pos_x=1031,top_pos_y=279,
		bot_pos_x=1112,bot_pos_y=463,
		name="Coffee",
		animation=Animation(spritesheet=coffee_sprites, frequency=8, position=(1100,300), screen=screen)
	)
)
registered_objects.append(
	AreaOfInterest(
		top_pos_x=1157,top_pos_y=244,
		bot_pos_x=1294,bot_pos_y=378,
		name="Music", 
		sound=SoundEffect(volume=0.7, track="sounds/City-Life.mp3")
	)
)
registered_objects.append(
	AreaOfInterest(
		top_pos_x=702,top_pos_y=508,
		bot_pos_x=1012,bot_pos_y=848,
		name="People", 
		sound=SoundEffect(volume=0.5, track="sounds/people.mp3")
	)
)
registered_objects.append(
	AreaOfInterest(
		top_pos_x=450,top_pos_y=154,
		bot_pos_x=684,bot_pos_y=648,
		name="Street", 
		sound=SoundEffect(volume=0.5, track="sounds/street.mp3")
	)
)
registered_objects.append(
	AreaOfInterest(
		top_pos_x=793, top_pos_y=225,
		bot_pos_x=857, bot_pos_y=276,
		name="Sign1"
	)
)
registered_objects.append(
	AreaOfInterest(
		top_pos_x=773, top_pos_y=368,
		bot_pos_x=819, bot_pos_y=428,
		name="Sign2"
	)
)

current_hit = Hit(area=registered_objects[0], start_time=0)

while keyboard.get_key()[0] == None:
	screen.draw_image(background_image)
	current_time = pygame.time.get_ticks()

	### DEBUG: Check position and print if change
	### old_gazepos_x = gazepos[0]
	### old_gazepos_y = gazepos[1]
	gazepos = eyetracker.sample()
	### if gazepos[0] != old_gazepos_x or gazepos[1] != old_gazepos_y:
	### 	print(gazepos)

	for obj in registered_objects:
		if (gazepos[0] in range(obj.topleft[0], obj.bottomright[0])) and (gazepos[1] in range(obj.topleft[1], obj.bottomright[1])):
			if current_hit.area.name != obj.name:
				### DEBUG: print(f"Hit {obj.name}")
				current_hit = Hit(area=obj, start_time=current_time)
				break
			elif not obj.started:
				diff = int(((current_time-current_hit.start_time)%60000)/1000)
				if old_diff < diff:
					### DEBUG: print(f"Hitting still. {diff} seconds.")
					if diff >= 1:
						### DEBUG: print(f"Playing animation for {obj.name}")
						obj.start()
				old_diff = diff
				break
			else:
				obj.update()
				break
	else:
		if current_hit.area.name != "None":
			### DEBUG: print(f"Lost contact with {current_hit.area.name}.")
			current_hit = Hit(area=registered_objects[0], start_time=0)
			### DEBUG: in case we decide to stop the animations
			### print("Stopping animation.")
			### mixer.Channel(0).pause()
			### mixer.Channel(1).pause()
			### mixer.Channel(2).pause()
			### playing_people = False
			### playing_street = False
			### playing_anim = False

    # draw crosshair
	screen.draw_circle(colour=FGC, pos=gazepos, r=13, pw=2, fill=False)
	disp.fill(screen)
	disp.show()
	screen.clear()
