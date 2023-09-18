from pcg_gazebo.parsers.sdf import create_sdf_element


def create_model_sdf_elements(mesh_uri, color=[0, 0.5, 0, 1]):
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
        {"tag": "sdf", "children": ["model"]},
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
