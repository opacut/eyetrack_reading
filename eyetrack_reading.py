from constants import *

#from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze.eyetracker import EyeTracker

# set up objects
keyboard = Keyboard()
disp = Display()
screen = Screen()
blankscreen = Screen()
eyetracker = EyeTracker(disp)

eyetracker.calibrate()
while keyboard.get_key()[0] == None:
	gazepos = eyetracker.sample()

	tl_col = tr_col = ll_col = lr_col = (255,0,0)
	if (gazepos[0] in range(50,150)) and (gazepos[1] in range(50, 150)):
		tl_col = (0,255,0)
	elif (gazepos[0] in range(700, 800)) and (gazepos[1] in range(50, 150)):
		tr_col = (0,255,0)
	elif (gazepos[0] in range(50, 150)) and (gazepos[1] in range(700, 800)):
		ll_col = (0,255,0)
	elif (gazepos[0] in range(700, 800)) and (gazepos[1] in range(700, 800)):
		lr_col = (0,255,0)

	screen.draw_text(text="LOOK", colour=tl_col, pos=(100, 100), fontsize=84)
	screen.draw_text(text="HERE", colour=tr_col, pos=(750, 100), fontsize=84)
	screen.draw_text(text="OR", colour=ll_col, pos=(100, 750), fontsize=84)
	screen.draw_text(text="HERE", colour=lr_col, pos=(750, 750), fontsize=84)
	
    # draw crosshair
	screen.draw_circle(colour=FGC, pos=gazepos, r=13, pw=2, fill=False)
	disp.fill(screen)
	disp.show()
	screen.clear()
