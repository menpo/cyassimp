This is a small C++ wrapper around the Assimp Library.

It contains:

1. `AssimpImporter` - instantiated with a path to a file that Assimp
understands. Disables features of Assimp that we don't need (importing
materials, calculating norms etc). Has one method, `get_scene()`, which 
returns an...

2. `AssimpScene` - a wrapper for `aiScene`. Builds a vector of `AssimpMesh` 
pointers at `this.meshes`. Also looks for the likely place for Assimp to
find basic texture maps (`aiTextureType_DIFFUSE`) and has a method
to grab this path. Although Assimp is capable of dealing with multiple
textures this remains unexplored, and for now, the first texture path found
is kept here.

3. `AssimpMesh` - a wrapper for `aiMesh`. Methods for checking state 
(`is_trimesh()` and for copying the mesh data
(points, trilist, tcoords) into simple C arrays.

These are the only classes that the Cython wrapper (`../cyassimp.pyx`) has to
interface with, meaning we don't have to worry about wrapping the internal
details of Assimp.
