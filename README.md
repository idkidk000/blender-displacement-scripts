# blender displacement scripts
* all editable variables are at the top of the scripts and have uppercase names.
* open the script in blender as a text file, select your object in the viewport and click "run script".

### sci-fi-panelling.py
* subdivides the mesh if it has fewer than SUBDIV_MIN_VERTS.
* randomly selects verts and edge loops, recursively expands and shrinks the selection, and assigns weights to a vertex group. 
* adds a displacement modifier, edge split and smooth shading. 
* works best on high poly meshes where all faces are similar sized quads.

### vertex-weight-mix.py
* creates a vertex group using combined weights from all all other groups.

### mark-weight-edges-sharp.py
* marks inner and/or outer edges of quantitized vertex weights as sharp.

### extrude-on-normals-by-vertex-weight.py
* does exactly what the script's called. 
* weights are quantitized before extrusion.

# q&a
*what can i do with these scripts?*
* https://github.com/johnakki/blender-displacement-scripts/blob/master/example.JPG
* https://github.com/johnakki/blender-displacement-scripts/blob/master/example2.JPG
* https://youtu.be/6LW3J4h2jVM

*why is your python code so terrible?*
* you must have at least 50,000 iq to understand my highly optimized algorithms.

*how should i spend my life savings?*
* https://www.blender.org/foundation/donation-payment/
* https://my.fsf.org/donate
