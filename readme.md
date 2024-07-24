# Blender Scripts

This is a library I've created to keep track of all of the tools I make while I learn to use blender. My goal is to eventually have a library I can use in my own game creation as well as bring some sort of help to those who happen upon the repo. 

## maze_maker.py
This script can be invoked inside of the MazeMaker.blend file included to create a randomized maze. In order to do this there are a few steps that must be done before running the script to ensure it works.
1. Create a Wall asset that is 1mx1mx.1m (x, y, z)
2. Create a Post object that is 1m tall (other dimensions can be set as needed)
3. Create a grid with 1mx1m cells 
4. Add the Maze Geometry Node to the grid's modifiers
5. Plug the wall and post into the arguments
6. Run the script while the object is selected