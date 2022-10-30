# eyetrack_reading
School project, exploring interaction possibilities of reading text with eye tracking using PyGaze.

# run
`python eyetrack_reading.py`

You will need to have [PyGaze](http://www.pygaze.org/installation/) installed.
It's developed on Fedora 36. Unfortunately you need at most Python 3.9.15 - I had to downgrade.
To do that, I installed a parallel installation of python3.9 with 
`sudo dnf install python3.9`
and then use it to create a virtual environment:
`python3.9 -m venv .venv`
`source .venv/bin/activate`
Confirm with `python --version` that you have the correct interpreter set up and you can start the pygaze installation, as per the instructions above.

I had some more problems with the installation, and needed to install `wheel`, `attrdict`, `gtk3-devel` and only then `psychopy`.

Check the forums, as there might have been new updates since I wrote this.
