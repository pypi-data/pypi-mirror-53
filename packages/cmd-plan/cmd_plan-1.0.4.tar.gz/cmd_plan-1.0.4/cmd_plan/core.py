import os


def launch(node_name: str, nodes: dict, already_run_nodes: set = None):
    if already_run_nodes is None:
        already_run_nodes = set()
    if node_name not in nodes:
        raise Exception('Node "%s" does not exist.' % node_name)
    for dependency_node_name in nodes.get(node_name).get('dependencies', []):
        if dependency_node_name in already_run_nodes:
            continue
        launch(dependency_node_name, nodes, already_run_nodes)
        already_run_nodes.add(dependency_node_name)
    os.system(nodes.get(node_name).get('command'))
    already_run_nodes.add(node_name)
