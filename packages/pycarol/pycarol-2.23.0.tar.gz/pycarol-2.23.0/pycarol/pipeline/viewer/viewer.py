from ..utils import get_reverse_dag, breadth_first_search


def nodes_layout(
        dag:dict,
        align_on_leafs=True,
        mode='force-directed',
        **layout_params
) -> dict:
    """
    Returns layout with x,y coordinates to plot DAG. Available modes are:
      'levels-directed': x positions correspond to the level of the node in DAG.
      'force-directed': computed using fruchterman_reingold_layout method of
      networkx library.
      'kamada-kawai': computed using networkx library
    If align on_leafs is set to true, DAG is first reversed, so that the
    output of the pipeline is on the right and inputs on the left in
    'levels-directed' mode.
    Args:
        dag: dict encoding a DAG structure
        align_on_leafs: layout boolean parameter
        mode: string defining layout mode

    Returns:
        layout: a dict whose keys are DAG nodes an values are (x,y) of each
        node.

    """
    layout_x = {}
    if align_on_leafs:
        dag = get_reverse_dag(dag)
    for i, nodes in enumerate(breadth_first_search(dag)):
        for j, node in enumerate(nodes):
            # overwrite previous levels and keep only last one
            layout_x[node] = i

    levels = sorted(v for v in layout_x.values())
    layout = {}
    for l in levels:
        y = 0
        for node, x in layout_x.items():
            if x == l:
                layout[node] = (x, y)
                y += 1

    if mode == "force-directed":
        import networkx as nx
        graph = nx.DiGraph()
        graph_edges = [(k, vi) for k, v in dag.items() for vi in v]
        graph.add_edges_from(graph_edges)
        default_layout = layout.copy()
        from pycarol.pipeline.utils import find_root_in_dag, find_leaf_in_dag
        root_nodes = find_root_in_dag(dag)
        leaf_nodes = find_leaf_in_dag(dag)
        fixed_nodes = root_nodes + leaf_nodes
        layout = nx.fruchterman_reingold_layout(
            graph,
            pos=default_layout,  # we use levels layout as default position
            fixed=fixed_nodes,
            **layout_params
        )
    elif mode == "kamada-kawai":
        import networkx as nx
        graph = nx.DiGraph()
        graph_edges = [(k, vi) for k, v in dag.items() for vi in v]
        graph.add_edges_from(graph_edges)
        layout = nx.kamada_kawai_layout(
            graph,
            **layout_params
        )

    return layout


def edges_layout(dag:dict, layout:dict) -> list:
    """
    Given a dag network and the positions of each one of its nodes,
    this function creates the positions of the edges.
    Args:
        dag: dict encoding a DAG
        layout: dict containing nodes x,y positions

    Returns:
        edges: list of positions, each one in format ( (x0,y0), (x1,y1) )
    """

    edges = []
    for source_node in layout:
        for target_node in dag[source_node]:
            edges.append((layout[source_node],layout[target_node]),)
    return edges

def get_task_id(t):
    return t.task_id

def get_task_family(t):
    # returns task namespace
        if '.' in t.task_id:
            return t.task_id.split('.')[-2]
        else:
            return ""

def get_task_name(t):
    return t.task_id.split('.')[-1].split('_')[0] # name of the task class

def get_complete(t):
    # return t.complete()
    # make it dummy, because efficient get_complete needs pipeline object
    return False


def get_target_hash_version(t):
    try:
        metadata = t.load_metadata()
    except:
        return ""
    return metadata.get('hash_version',"")

def get_task_hash_version(t):
    try:
        h = t.hash_version()
    except:
        h = ""
    return h
def get_task_version(t):
    try:
        h = t.version
    except:
        h = ""
    return h

def get_target_version(t):
    try:
        metadata = t.load_metadata()
    except:
        return ""
    return metadata.get('version',"")

#TODO: implement dash viewer
def make_nodes_data_source(nodes_layout) -> dict:
    """
    Creates a bokeh compatible data source encoding nodes plotting
    properties. Returns this data source in bokeh compatible dict format
    Args:
        nodes_layout: dict containing nodes as keys and its positions as
        values. In this function nodes are luigi tasks.

    Returns:
        data_source: bokeh compatible dict containing the columns: x, y,
        task_id, task_family, task_name, complete, tasklog, hash_version

    """

    data = dict(
        x=[],
        y=[],
        task_id=[],
        task_family=[],
        task_name=[],
        complete=[],
        target_version=[],
        task_version=[],
    )
    for k,(x,y) in nodes_layout.items():
        data['x'].append(x)
        data['y'].append(y)
        data['task_id'].append(get_task_id(k))
        data['task_family'].append(get_task_family(k))
        data['task_name'].append(get_task_name(k))
        data['complete'].append(get_complete(k))
        data['target_version'].append(get_target_version(k))
        data['task_version'].append(get_task_version(k))

    
    v_gen = (v for v in data.values())
    first_v = next(v_gen)
    for v in v_gen:
        if len(first_v) != len(v):
            raise ValueError("all items in data should have the same length")

    return data

def make_edges_data_source(edges_layout) -> dict:
    """
    Creates a bokeh segment glyph compatible data source encoding edges plotting
    properties. Returns this data source in bokeh compatible dict format
    Args:
        edges_layout: list containing edges coordinates.

    Returns:
        data_source: bokeh segment glyph compatible dict containing the
        columns: x0, y0, x1, y1

    """

    data = dict(
        x0=[],
        y0=[],
        x1=[],
        y1=[]
    )
    for ((x0,y0,),(x1,y1)) in edges_layout:
        data['x0'].append(x0)
        data['y0'].append(y0)
        data['x1'].append(x1)
        data['y1'].append(y1)

    return data

