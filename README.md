# Eyetracking interactions
School project, exploring possibilities of creating interactive content with eye tracking using PyGaze.

# Install
`python scene.py`

You will need to have [PyGaze](http://www.pygaze.org/installation/) installed.

This code is developed on Fedora 36. 

Unfortunately, to install all the dependencies of PyGaze, you need at most Python 3.9.15 - I had to downgrade.  
To do that, I installed a parallel installation of python3.9 with  
`sudo dnf install python3.9`  
and then use it to create a virtual environment:
`python3.9 -m venv .venv`  
`source .venv/bin/activate`  
Confirm with `python --version` that you have the correct interpreter set up and you can start the pygaze installation, as per the instructions above.

I had some more problems with the installation, and needed to install `wheel`, `attrdict`, `gtk3-devel`, `gcc-c++` and only then `psychopy`.

Check the forums, as there might have been new updates since I wrote this.

It's developed with the Eyetribe software, and we're borrowing the driver (with slight adjustments) from the PyTribe project by esdalmaijer, https://github.com/esdalmaijer/PyTribe

WINDOWS
This was way more tricky than it should have been. Do yourself a favor and use pyenv :)
to install pyenv, I use https://chocolatey.org/install
then install python 3.9 or lower (I'm using 3.6.8 at the moment), like here https://realpython.com/intro-to-pyenv/#using-pyenv-to-install-python
and that should theoretically do it. Contact me if something doesn't work, and we can throw our hands in the air in confusion together.

# Running a scenario
You can run this in dummy mode, i.e. operated by mouse, or you can use the Eyetribe eyetracker. 
The code is not tested on anything else, but I'm hoping it should be adaptable.
To switch from dummy to eyetribe, change the value of `DUMMYMODE` in `constants.py` to `False`.

Right now we don't have a build mechanism working, so to run, do
`python scene.py`

The mechanism to input a new scenario is a bit complex at the moment and requires touching the code. 
In the future, I plan to make the app take .json files that would describe the scene.
To describe a new scenario, you will be altering the classes.GameController.load_scene() method.

To add a new scenario, add the scenario name into the list of available scenarios, like so

![scenario setup](/docs/scenarios.png)

A scenario is composed of a series of scenes, or "slides" that you cycle through by pressing space.
A scene is defined by several things:
- a name
- path to the background image
- a list of registered objects

This list of registered objects is the main thing you have to define. Every such object is an AreaOfInterest object.
You need to know and have a couple things in order to define this properly. An AreaOfInterest is a rectangular area that, when entered, will initiate an interaction.
You need the x and y of the top left point of the rectangle, and the x and y of the bottom right point. 
There is a mechanism here to find that out. Uncomment the code in these lines:  
![debug position](/docs/debug_position.png)
And you'll be able to see the position of the cursor when running the app. 

Next, give each interaction a name.
And a SoundEffect. You can also see in the cafeteria scenario a way of adding animations, but it's a bit clunky at the moment.

Lastly, you should define how your scenario cycles through the scenes in the `classes.GameController.next_scene()` method.

After that, you're ready to switch to <your_scenario> in `scene.py`, in gc initialization:
`gc = GameController(keyboard=keyboard, display=disp, screen=screen, eyetracker=eyetracker, scenario_name=<your_scenario>)`

# Further work
These are some additions I plan to work on on this project in the future. Feel free to open up a PR and help with any of these.
- dynamic scenario creation from a .json file
- start the program by offering user a choice from the scenarios available
- package everything neatly as a python package
- generate an executable
- 'editor' mode where a user can upload images and create AoIs and scenarios without touching the code
