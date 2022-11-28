from constants import *

#from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze.eyetracker import EyeTracker
import pygame

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

while keyboard.get_key()[0] == None:
	#pdb.set_trace()
	#disp.blit(background_image, (0,0))
	screen.draw_image(background_image)
	current_time = pygame.time.get_ticks()

	# Check position and print if change
	# old_gazepos_x = gazepos[0]
	# old_gazepos_y = gazepos[1]
	gazepos = eyetracker.sample()
	# if gazepos[0] != old_gazepos_x or gazepos[1] != old_gazepos_y:
	# 	print(gazepos)

	#coffee
	#	[x,y] 1031,279
	#	[x,y] 1112,463
	if (gazepos[0] in range(1031,1112)) and (gazepos[1] in range(279, 463)):
		if last_collision != "Coffee":
			last_collision = "Coffee"
			print("Hit coffee.")
			start_hit = pygame.time.get_ticks()
		else:
			diff = ((current_time-start_hit)%60000)/1000
			print(f"Hitting still. {diff}")
			if diff >= 2:
				print("Playing animation.")
	else:
		if last_collision == "Coffee":
			last_collision = None
			print("Lost contact with Coffee.")
			print("Stopping animation.")

	#music
	# 	[x,y] 1157,244
	# 	[x,y] 1294,378

	#people
	# 	[x,y] 702,508
	# 	[x,y] 1012,848

	#street
	# 	[x,y] 450,154
	# 	[x,y] 684,648

	#sign1
	# 	[x,y] 793,225
	# 	[x,y] 857,276

	#sign2
	# 	[x,y] 773,368
	# 	[x,y] 819,428


	# tl_col = tr_col = ll_col = lr_col = (255,0,0)
	# if (gazepos[0] in range(50,150)) and (gazepos[1] in range(50, 150)):
	# 	tl_col = (0,255,0)
	# elif (gazepos[0] in range(700, 800)) and (gazepos[1] in range(50, 150)):
	# 	tr_col = (0,255,0)
	# elif (gazepos[0] in range(50, 150)) and (gazepos[1] in range(700, 800)):
	# 	ll_col = (0,255,0)
	# elif (gazepos[0] in range(700, 800)) and (gazepos[1] in range(700, 800)):
	# 	lr_col = (0,255,0)

	# screen.draw_text(text="LOOK", colour=tl_col, pos=(100, 100), fontsize=84)
	# screen.draw_text(text="HERE", colour=tr_col, pos=(750, 100), fontsize=84)
	# screen.draw_text(text="OR", colour=ll_col, pos=(100, 750), fontsize=84)
	# screen.draw_text(text="HERE", colour=lr_col, pos=(750, 750), fontsize=84)
	
    # draw crosshair
	screen.draw_circle(colour=FGC, pos=gazepos, r=13, pw=2, fill=False)
	disp.fill(screen)
	disp.show()
	screen.clear()
