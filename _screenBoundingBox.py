#based on https://olestourko.github.io/2018/02/03/generating-convnet-training-data-with-blender-1.html

def object_bounds_2d(scene, obj, cam):
    """
    Returns camera space bounding box of the mesh object.

    Gets the camera frame bounding box, which by default is returned without any transformations applied.
    Create a new mesh object based on mesh_object and undo any transformations so that it is in the same space as the
    camera frame. Find the min/max vertex coordinates of the mesh visible in the frame, or None if the mesh is not in view.
    """
    verts = []
    mat = obj.matrix_world
    temp_verts = [vert.co for vert in obj.data.vertices]

    for i in range(len(temp_verts)):
        vco = obj.matrix_world @ temp_verts[i]
        origin = cam.matrix_world.translation
        direction = (vco - origin).normalized()
        visObject = scene.ray_cast(bpy.context.view_layer.depsgraph, origin, direction)
        if(visObject[4] == obj):
            verts.append(vco)

    coords_2d = [world_to_camera_view(scene, cam, coord) for coord in verts]

    verts_2d =[]
    for (x, y, distance_to_lens), vert_co in zip(coords_2d,verts):
        verts_2d.append(tuple((x, y)))

    if len(verts_2d) == 0:
        print("!Object not visible in the scene; {}".format(str(obj.name)))
        return None

    max_y = np.clip(max(verts_2d, key = lambda i : i[1])[1], 0.0, 1.0)
    max_x = np.clip(max(verts_2d, key = lambda i : i[0])[0], 0.0, 1.0)
    min_y = np.clip(min(verts_2d, key = lambda i : i[1])[1], 0.0, 1.0)
    min_x = np.clip(min(verts_2d, key = lambda i : i[0])[0], 0.0, 1.0)

    verts_2d.clear()

    return (min_x, max_x, min_y, max_y)
    
if __name__ == '__main__':
    scene = bpy.data.scenes['Scene']
    camera_obj = bpy.data.objects['Camera']
    obj = bpy.data.objects['Object']
    object_bounds_2d(scene, obj, camera):
