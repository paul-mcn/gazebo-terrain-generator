from pcg_gazebo.parsers.sdf import create_sdf_element


def create_geometry_sdf(mesh_uri, scale, submesh_name=False):
    mesh = create_sdf_element("mesh")
    geometry = create_sdf_element("geometry")
    mesh.uri = mesh_uri  # type: ignore
    mesh.scale = scale  # type: ignore
    if submesh_name:
        submesh = create_sdf_element("submesh")
        submesh.name = submesh_name  # type: ignore
        mesh.children["submesh"] = submesh  # type: ignore
    geometry.mesh = mesh  # type: ignore
    return geometry


def create_tree_sdf(
    mesh_uri, script_uris, model_name, model_pose, material_names, scale
):
    collision = create_sdf_element("collision")
    link = create_sdf_element("link")
    model = create_sdf_element("model")
    link.children["visual"] = []
    for material_name in material_names:
        uri = create_sdf_element("uri")
        uri2 = create_sdf_element("uri")
        geometry = create_sdf_element("geometry")
        script = create_sdf_element("script")
        material = create_sdf_element("material")
        visual = create_sdf_element("visual")
        submesh_name = material_name.split("/")[-1]
        geometry = create_geometry_sdf(mesh_uri, scale, submesh_name)
        material.reset()  # type: ignore
        script.name = material_name  # type: ignore
        uri.value = script_uris[0]  # type: ignore
        uri2.value = script_uris[1]  # type: ignore
        script.children["uri"] = [uri, uri2]  # type: ignore
        material.children["script"] = script  # type: ignore
        visual.children["geometry"] = geometry  # type: ignore
        visual.children["material"] = material  # type: ignore
        visual.name = submesh_name  # type: ignore
        link.children["visual"].append(visual)  # type: ignore

    geometry = create_geometry_sdf(mesh_uri, scale)
    collision.children["geometry"] = geometry  # type: ignore
    link.children["collision"] = collision  # type: ignore
    model.children["link"] = link  # type: ignore
    model.name = model_name  # type: ignore
    model.pose = model_pose  # type: ignore
    model.static = True  # type: ignore
    return model


def create_ground_sdf(mesh_uri, model_name, model_pose, material_name, scale):
    uri = create_sdf_element("uri")
    uri2 = create_sdf_element("uri")
    script = create_sdf_element("script")
    material = create_sdf_element("material")
    visual = create_sdf_element("visual")
    collision = create_sdf_element("collision")
    link = create_sdf_element("link")
    model = create_sdf_element("model")
    geometry = create_geometry_sdf(mesh_uri, scale)
    material.reset()  
    script.name = material_name  # type: ignore
    # for objects that dont have custom materials, just use the gazebo default materials
    uri.value = "file://media/materials/scripts/gazebo.material"  # type: ignore
    script.children["uri"] = uri  # type: ignore
    material.lighting = True 
    # material.ambient = [0, 0, 0, 0]
    # material.diffuse = [1, 1, 1, 1]
    # material.specular = [0, 0, 0, 0]
    # material.emissive = [0, 0, 0, 0]
    material.children["script"] = script  # type: ignore
    visual.children["geometry"] = geometry  # type: ignore
    visual.children["material"] = material  # type: ignore
    visual.cast_shadows = True
    visual.name = "visual"  # type: ignore
    collision.children["geometry"] = geometry  # type: ignore
    link.children["collision"] = collision  # type: ignore
    link.children["visual"] = visual  # type: ignore
    model.children["link"] = link  # type: ignore
    model.name = model_name  # type: ignore
    model.pose = model_pose  # type: ignore
    model.static = True  # type: ignore
    return model


def create_rock_sdf(
    mesh_uri, script_uris, model_name, model_pose, material_name, scale
):
    uri = create_sdf_element("uri")
    uri2 = create_sdf_element("uri")
    script = create_sdf_element("script")
    material = create_sdf_element("material")
    visual = create_sdf_element("visual")
    collision = create_sdf_element("collision")
    link = create_sdf_element("link")
    model = create_sdf_element("model")
    geometry = create_geometry_sdf(mesh_uri, scale)
    material.reset(with_optional_elements=True)  # type: ignore
    script.name = material_name  # type: ignore
    # for objects that dont have custom materials, just use the gazebo default materials
    if script_uris and len(script_uris) >= 2:
        uri.value = script_uris[0]  # type: ignore
        uri2.value = script_uris[1]  # type: ignore
        script.children["uri"] = [uri, uri2]  # type: ignore
    material.children["script"] = script  # type: ignore
    visual.children["geometry"] = geometry  # type: ignore
    visual.children["material"] = material  # type: ignore
    visual.cast_shadows = True
    visual.name = "rock"  # type: ignore
    collision.children["geometry"] = geometry  # type: ignore
    link.children["collision"] = collision  # type: ignore
    link.children["visual"] = visual  # type: ignore
    model.children["link"] = link  # type: ignore
    model.name = model_name  # type: ignore
    model.pose = model_pose  # type: ignore
    model.static = True  # type: ignore
    return model


def create_grass_sdf(mesh_uri, model_name, model_pose, material_name, scale):
    uri = create_sdf_element("uri")
    script = create_sdf_element("script")
    material = create_sdf_element("material")
    visual = create_sdf_element("visual")
    link = create_sdf_element("link")
    model = create_sdf_element("model")
    geometry = create_geometry_sdf(mesh_uri, scale)
    material.reset(with_optional_elements=True)  # type: ignore
    script.name = material_name  # type: ignore
    # for objects that dont have custom materials, just use the gazebo default materials
    uri.value = "file://media/materials/scripts/gazebo.material"
    script.children["uri"] = uri  # type: ignore
    material.children["script"] = script  # type: ignore
    visual.children["geometry"] = geometry  # type: ignore
    material.lighting = True
    material.ambient = [0, 1, 0, 1]
    visual.children["material"] = material  # type: ignore
    visual.name = "grass"  # type: ignore
    link.children["visual"] = visual  # type: ignore
    model.children["link"] = link  # type: ignore
    model.name = model_name  # type: ignore
    model.pose = model_pose  # type: ignore
    model.static = True  # type: ignore
    return model


def create_ground_mesh_sdf_elements(mesh_uri, color=[0, 0.5, 0, 1]):
    # list should be in order from child to parent
    sdf_elements = [
        {"tag": "mesh", "opts": {"uri": mesh_uri}},
        {"tag": "geometry", "children": ["mesh"]},
        {"tag": "collision", "children": ["geometry"]},
        {"tag": "material", "opts": {"ambient": color}},
        {"tag": "visual", "children": ["geometry", "material"]},
        {"tag": "link", "children": ["collision", "visual"]},
        {
            "tag": "model",
            "children": ["link"],
            "opts": {
                "name": "ground_mesh1",
                "pose": [0, 0, 0, 0, 0, 0],
                "static": True,
            },
        },
        {"tag": "world", "children": ["model"]},
        {"tag": "sdf", "children": ["world"]},
    ]
    return sdf_elements


def set_element_options(sdf_el, opts: dict):
    """
    Sets the xml tag's options. e.g. name, pose
    """
    for opt, val in opts.items():
        setattr(sdf_el, opt, val)


def set_element_children(sdf_el, children, cache):
    for child in children:
        child_el = cache.get(child)
        # for some reason mesh needs to be set as a direct attribute of geometry,
        # e.g. geometry.mesh = mesh, and not geometry.children.mesh = mesh
        # otherwise, an <empty> and <mesh> will be created as children of the <geometry> element, and throw an error
        if sdf_el.xml_element_name == "geometry":
            setattr(sdf_el, child, child_el)
        else:
            sdf_el.children[child] = child_el


def create_and_set_sdf_element(element, cache: dict):
    # get a reference to the element's tag
    tag = element.get("tag")

    # create the sdf element
    sdf_el = create_sdf_element(tag)
    if sdf_el is None:
        return print("Woops, something went wrong when trying to create sdf element")

    # Save element in flat object for fast lookup
    cache[tag] = sdf_el

    # use element options
    opts = element.get("opts")
    if opts:
        set_element_options(sdf_el, opts)

    # Create child elements
    children = element.get("children")
    if children:
        set_element_children(sdf_el, children, cache)


def create_sdf_tree(sdf_elements):
    element_cache = {}
    # Create the sdf elements dynamically.
    # NOTE: child elements must be set before parent elements in the sdf_elements array
    for element in sdf_elements:
        create_and_set_sdf_element(element, element_cache)

    # get the root of the sdf tree
    el = sdf_elements[-1].get("tag")
    root_element = element_cache[el]
    return root_element
