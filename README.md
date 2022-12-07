# Eyetracking interactions
School project, exploring possibilities of creating interactive content with eye tracking using PyGaze.

# run
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

I had some more problems with the installation, and needed to install `wheel`, `attrdict`, `gtk3-devel` and only then `psychopy`.

Check the forums, as there might have been new updates since I wrote this.

It's developed with the Eyetribe software, and we're borrowing the driver (with slight adjustments) from the PyTribe project by esdalmaijer, https://github.com/esdalmaijer/PyTribe

WINDOWS
This was way more tricky than it should have been. Do yourself a favor and use pyenv :)
to install pyenv, I use https://chocolatey.org/install
then install python 3.9 or lower (I'm using 3.6.8 at the moment), like here https://realpython.com/intro-to-pyenv/#using-pyenv-to-install-python
and that should theoretically do it. Contact me if something doesn't work, and we can throw our hands in the air in confusion together.
