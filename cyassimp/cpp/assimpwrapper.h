#pragma once

#include <string>
#include <vector>
#include <assimp/Importer.hpp>
const std::string NO_TEXTURE_PATH = "NO_TEXTURE_PATH";

// forward declarations
struct aiScene;
struct aiMesh;
struct aiMaterial;
class AssimpMesh;
class AssimpScene;
class AssimpImporter;


// *************** IMPORTER ************ //
class AssimpImporter{
    Assimp::Importer importer;
    AssimpScene* p_scene;

    public:
    AssimpImporter(std::string path);
    ~AssimpImporter();
    AssimpScene* get_scene();
};


// *************** SCENE *************** //
class AssimpScene{
    const aiScene* p_scene;

    public:
    std::vector<AssimpMesh*> meshes;
    AssimpScene(const aiScene* scene);
    ~AssimpScene();
    unsigned int n_meshes();
    std::string texture_path();
};


// *************** MESH *************** //
class AssimpMesh{
    aiMesh* p_mesh;
    AssimpScene* scene;

    public:
    AssimpMesh(aiMesh* mesh, AssimpScene* scene);
    unsigned int n_points();
    unsigned int n_faces();
    unsigned int n_tcoord_sets();
    unsigned int n_colour_sets();
    bool has_points();
    bool has_lines();
    bool has_triangles();
    bool has_polygons();
    bool is_trimesh();
    bool is_pointcloud();
    void points(double* points);
    void trilist(unsigned int* trilist);
    void tcoords(int index, double* tcoords);
    void colour_per_vertex(int index, double* colour_per_vertex);
    void tcoords_with_alpha(int index, double* tcoords);
};


// *************** HELPER ROUTINES *************** //
unsigned int tcoords_mask(aiMesh* mesh, bool* has_tcoords);
unsigned int colour_sets_mask(aiMesh* mesh, bool* has_colour_sets);
std::string diffuse_texture_path_on_material(aiMaterial* mat);
