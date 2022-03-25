# A N-Body simulation using pygame and numpy

Press G key for toggling galaxy spawning. Change the requried properties in *config.py* file. 
See the event handler method for different methods. The barnes hut algorithm is significantly slower in 
python, don't whether i implemented it correctly, may be you can give me a hand in this.

Use right click for dragging and scroll for zooming 
and left click for spawninga and velocity vector for the particles. 


## Keys and functions

Keyboad
- 0-9     : selects particles mass multiplied by 100s
- a       : particle mass by 10000
- b       : particle mass by 100000
- c       : particle mass by 10000000000
- f       : enable barnes hut algorithm
- g       : toggle galaxy spawn
- s       : show quads in barnes hut
- r       : removes all particles
- o       : set center to 0,0
- p       : pause
- left    : slows time 
- right   : speeds time 

Mouse 
- left    : spawns
- right   : drag the space
- middle  : zoom 
