# gazebo-terrain-generator
A terrain generator to create worlds to use in gazebo

## Get started
Assuming you're using ubuntu 20.04 and have python3 installed. Currently I'm using python 3.8.10, earlier version may work, however, they have not been tested.

### Inital install
Steps for when you first clone the project
```
# Clone the project from git
git clone https://github.com/paul-mcn/gazebo-terrain-generator.git

# cd into the root project dir
cd gazebo-terrain-generator

# Create an isolated python environment. It allows you install packages locally rather than globally.
python3 -m venv venv

# Activate environment 
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### To run the world
To generate terrain and run it inside gazebo, you must first run the python file, then launch the gazebo world.
You can do this by running:
```
# Generate terrain
python main.py

# Launch Gazebo. This is done in the root of the project dir, however, it can be done anywhere.
# Just make sure you adjust the path arg.
gazebo ./worlds/generated_world.world
```


### Subsequent runs
Each time you open a new terminal, you will have to run the below code in the root project dir. 
Otherwise your global pacakges will be used and the file won't launch correctly
```
# ❌ will fail
python main.py

# ✅ will work
source venv/bin/activate
python main.py
```

### Deactivate environment
Once you're done with the project, deactivate it by using the `deactivate` cmd in your terminal

## Export paths
As of yet, custom paths are not support. 
It is important to note that the `generated_world.world` file sources the `ground_mesh` using `model://ground_mesh`.
Thus, if you wish to choose a different dir, make sure to add it to the `GAZEBO_MODEL_PATH`.

Worlds export to `gazebo-terrain-generator/worlds` under the name `generated_world.world` by default
Models export to `$HOME/.gazebo/models` under the name `ground_mesh` by default. Additionally, it contains the following files:
- model.config
- model.sdf
- model.obj


## Libraries used
PCG Gazeo - https://boschresearch.github.io/pcg_gazebo_pkgs/

Trimesh - https://trimsh.org/trimesh.html

Numpy - https://numpy.org/doc/stable/

Pyglet - https://pyglet.readthedocs.io/en/pyglet-1.5-maintenance/ note: 1.5 is used, not 2+

Noise - somewhere in the abyss

