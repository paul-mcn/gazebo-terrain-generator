# gazebo-terrain-generator
A terrain generator to create worlds to use in gazebo

## Get started
Assuming you're using ubuntu 20.04 and have python3 installed. Currently I'm using python 3.8.10, earlier version may work, however, they have not been tested.

### Inital install
Steps for when you first clone the project
```
# Create virtual environment for isolated python environment. It allows you install packages locally rather than globally.
python3 -m venv venv

# Activate environment 
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Launch file
python main.py
```

### Subsequent runs
Each time you open the terminal, you will have to run the below code. Otherwise your global pacakges will be used and the file won't launch correctly
```
source venv/bin/activate
python main.py
```

### Deactivate environment
Once you're done with the project, deactivate it by using the `deactivate` cmd in your terminal

# Libraries used
PCG Gazeo

Trimesh

Numpy

Pyglet

Noise

