import pygame
from constants import *

from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.libscreen import Display 
from pygaze.libscreen import Screen

from classes import Hit
from classes import GameController
from PyTribe.pytribe import *


# set up objects
keyboard = Keyboard()
disp = Display()
screen = Screen()
blankscreen = Screen()
eyetracker = EyeTracker(disp)
# Eyetribe
#eyetracker = EyeTribe()
eyetracker.calibrate()

gazepos = [0,0]
last_collision = None
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
old_diff = 0
playing = False
playing_music = False
playing_people = False
playing_street = False


gc = GameController(keyboard=keyboard, display=disp, screen=screen, eyetracker=eyetracker, scene_name="1")

current_hit = Hit(area=gc.registered_objects[0], start_time=0)

eyetracker.start_recording()
while gc.running:
	gc.process_control(keyboard.get_key())
	screen.draw_image(gc.background_image)
	current_time = pygame.time.get_ticks()

	### DEBUG: Check position and print if change
	### old_gazepos_x = gazepos[0]
	### old_gazepos_y = gazepos[1]
	gazepos = eyetracker.sample()
	### if gazepos[0] != old_gazepos_x or gazepos[1] != old_gazepos_y:
	### 	print(gazepos)

	for obj in gc.registered_objects:
		if (int(gazepos[0]) in range(obj.topleft[0], obj.bottomright[0])) and (int(gazepos[1]) in range(obj.topleft[1], obj.bottomright[1])):
			if current_hit.area.name != obj.name:
				### DEBUG: print(f"Hit {obj.name}")
				current_hit = Hit(area=obj, start_time=current_time)
				break
			elif not obj.started:
				diff = ((current_time-current_hit.start_time)%60000)/1000
				if old_diff < diff:
					### DEBUG: print(f"Hitting still. {diff} seconds.")
					if diff >= 0.5:
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
			current_hit = Hit(area=gc.registered_objects[0], start_time=0)
			### DEBUG: in case we decide to stop the animations
			### print("Stopping animation.")
			gc.pause_all()
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

eyetracker.stop_recording()
eyetracker.close()