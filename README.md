# blender-displacement-scripts

all editable variables are at the top of the scripts and have uppercase names.

open the script in blender as a text file, select your object in the viewport and click "run script".

sci-fi-panelling.py
* randomly selects verts and edge loops, expands and shrinks the selection, and assigns weights to a vertex group. adds a displacement modifier, edge split and smooth shading. works best with 10k+ verts

vertex-weight-mix.py
* combines all vertex groups. weights are divided by number of groups to keep values between 0 and 1

mark-weight-edges-sharp.py
* marks inner and/or outer edges of quantitized vertex weights as sharp

extrude-on-normals-by-vertex-weight.py
* does exactly what the script's called. weights are quantitized before extrusion.
