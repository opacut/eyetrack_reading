import pygame
from constants import *

from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
import pdb
from pygaze.libscreen import Display 
from pygaze.libscreen import Screen
from pygaze.liblog import Logfile

#from PyGazeAnalyser.pygazeanalyser.edfreader import read_edf
#from PyGazeAnalyser.pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, draw_scanpath, draw_raw

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

# output
#log = Logfile()
#log.write(["starttime","endtime","duration","endx","endy"])

gazepos = [0,0]
last_collision = None
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
old_diff = 0


gc = GameController(keyboard=keyboard, display=disp, screen=screen, eyetracker=eyetracker, scenario_name="cafeteria")

current_hit = Hit(area=gc.registered_objects[0], start_time=0)

#eyetracker.start_recording()
#eyetracker.log("TRIALSTART")
#eyetracker.log(f"IMAGENAME {images[trialnr]}")
#eyetracker.status_msg(f"trial {trialnr+1}/{nrtrials}")
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
			gc.stop_all()

    # draw crosshair
	screen.draw_circle(colour=FGC, pos=gazepos, r=13, pw=2, fill=False)
	disp.fill(screen)
	disp.show()
	screen.clear()

#eyetracker.log("TRIALEND")

#eyetracker.stop_recording()

#screen.clear()
#screen.draw_text(text="Transferring the data file...")
#disp.fill(screen)
#disp.show()

#eyetracker.close()
#log.close()

#edfdata = read_edf(f"{LOGFILE}.txt", start="TRIALSTART", stop="TRIALEND", missing=0.0, debug=False)

#screen.clear()
#screen.draw_text(text="This is the end.")
#disp.fill(screen)
#disp.show()

#keyboard.get_key(keylist=None, timeout=None, flush=True)
#disp.close()