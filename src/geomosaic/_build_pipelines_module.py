import networkx as nx
from networkx.classes import DiGraph
from collections import deque
import networkx as nx
import subprocess
from geomosaic._utils import GEOMOSAIC_ERROR
from geomosaic._validator import validator_hmms_folder, validator_completeness_contamination_integer


def build_pipeline_modules(graph: DiGraph, collected_modules: dict, order: list, additional_input: dict, mstart: str="pre_processing", unit=False):
    G = graph.copy()
    assert mstart in G.nodes()

    dfs_collection = {}
    for m in G.nodes():
        dfs_collection[m] = list(nx.dfs_preorder_nodes(G, source=m))
    
    # Cleaning the Graph, based on the starting point
    for n in graph.nodes():
        if n not in dfs_collection[mstart]:
            G.remove_node(n)

    # Obtaining all descendants of the working graphs
    modules_descendants = {}
    for m in G.nodes():
        modules_descendants[m] = list(nx.descendants(G, m))

    user_choices = {}
    
    if unit:
        raw_queue = [mstart]
    else:
        raw_queue = list(nx.bfs_tree(G, source=mstart).nodes())

    # Defining order
    queue = deque([elem for elem in order if elem in raw_queue])

    while queue:
        status = False
        my_module = queue[0]

        module_descr = collected_modules[my_module]["description"]
        module_choices = {}
        module_choices[0] = {"display": "-- Ignore this module (and all successors) --", "package": ""}
        for indice, raw_package in enumerate(collected_modules[my_module]["choices"].items(), start=1):
            pckg_display, pckg_name = raw_package
            module_choices[indice] = {"display": pckg_display, "package": pckg_name}

        prompt_display = f"\n{module_descr}\n" + "\n".join([f"{integer}) {pck_info['display']}" for integer, pck_info in module_choices.items()])
        while not status:
            print(prompt_display)
            
            raw_input = input()

            status, obj = check_user_input(raw_input, list(module_choices.keys()))
            if not status:
                print(obj)
        
        parse_input = obj
        if parse_input == 0:
            G.remove_node(my_module)
            G.remove_nodes_from(modules_descendants[my_module])
            for desc in modules_descendants[my_module]:
                if desc in queue:
                    queue.remove(desc)
            
            queue.popleft()
            continue
        
        user_choices[my_module] = module_choices[parse_input]["package"]
        queue.popleft()
    
    dependencies = list(G.edges())
    order_writing = list(nx.bfs_tree(G, source=mstart).nodes())

    return user_choices, dependencies, G, order_writing


def ask_additional_parameters(additional_input, order_writing):
    additional_parameters = {}

    for module in order_writing:
        if module in additional_input:
            for adt_param, adt_param_tokens in additional_input[module].items():
                input_adt_param = get_user_path(adt_param_tokens["description"])

                if adt_param == "hmm_folder" and not validator_hmms_folder(input_adt_param):
                    print("GeoMosaic Error - Exit Code 1")
                    exit(1)
                
                if adt_param == "completness_threshold" and not validator_completeness_contamination_integer(input_adt_param):
                    print("GeoMosaic Error - Exit Code 1 - completeness")
                    exit(1)

                if adt_param == "contamination_threshold" and not validator_completeness_contamination_integer(input_adt_param):
                    print("GeoMosaic Error - Exit Code 1")
                    exit(1)
                
                # INSERT PARAM FOR CONFIG FILE
                if adt_param_tokens["type"] in ["integer"]:
                    additional_parameters[adt_param] = int(input_adt_param)
                else:
                    additional_parameters[adt_param] = input_adt_param
    
    return additional_parameters


def get_user_path(description):
    try:
        raw_path = subprocess.check_output(f'read -e -p "{description}: \n" var; echo $var', shell=True, executable='/bin/bash')
        path = raw_path.rstrip().decode('utf-8')
        return path
    except Exception as e:
        print(description)
        input_adt_param=input()
        return input_adt_param



def import_graph(edges: list) -> DiGraph:
    g = nx.DiGraph()
    for source, target in edges:
        g.add_edge(source, target)
    
    return g


def check_user_input(input, list_ints):
    false_payload = (False, "Wrong input")

    try:
        user_input = int(input)

        if user_input not in list_ints:
            return false_payload
    except:
        return false_payload
    
    return True, user_input
