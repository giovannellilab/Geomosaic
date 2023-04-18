import networkx as nx
import json
from networkx.classes import DiGraph
import yaml
from geomosaic.parse_sample_table import parse_sample_table
from argparse import ArgumentParser
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import os
import subprocess


def get_user_choices(folder_raw_reads, geomosaic_dir, sample_table, pipeline):
    samples_list, wdir_geomosaic = parse_sample_table(folder_raw_reads, geomosaic_dir, sample_table)

    modules_folder = os.path.join(os.path.dirname(__file__), 'modules')    
    gmpackages_path = os.path.join(os.path.dirname(__file__), 'gmpackages.json')

    with open(gmpackages_path, 'rt') as f:
        gmpackages = json.load(f)

    G = import_graph(gmpackages["graph"])
    collected_modules = gmpackages["modules"]
    order = gmpackages["order"]
    additional_input = gmpackages["additional_input"]

    if pipeline:
        # TODO: Adding additional parameters to default pipeline
        with open(os.path.join(os.path.dirname(__file__), 'pipeline.json')) as default_pipeline:
            pipe = json.load(default_pipeline)
            user_choices = pipe["user_choices"]
            order_writing = pipe["order_writing"]
    else:
        mstart = "pre_processing"
        user_choices, dependencies, modified_G, order_writing = build_pipeline_modules(
            graph=G,
            collected_modules=collected_modules, 
            order=order, 
            additional_input=additional_input,
            mstart=mstart
        )
    
    additional_parameters = ask_additional_parameters(additional_input, order_writing)

    # with open("pipeline.json", "wt") as default_pipeline:
    #     json.dump({"user_choices": user_choices, "order_writing": order_writing}, default_pipeline)
    
    config_filename = os.path.join(geomosaic_dir, "config.yaml")
    snakefile_filename = os.path.join(geomosaic_dir, "Snakefile.smk")

    config = {}
    config["SAMPLES"] = samples_list
    config["WDIR"] = os.path.abspath(wdir_geomosaic)

    for ap, ap_input in additional_parameters.items():
        config[ap] = ap_input

    for module_name, pckg_info in user_choices.items():
        config[module_name] = pckg_info['package']

    with open(config_filename, 'w') as fd_config:
        yaml.dump(config, fd_config)

    with open(snakefile_filename, "wt") as fd:
        fd.write(f"configfile: {str(repr(os.path.abspath(config_filename)))}\n")

        # Rule ALL
        fd.write("\nrule all:\n\tinput:\n\t\t")
        for m in order_writing:
            package = user_choices[m]["package"]
            snakefile_target = os.path.join(modules_folder, m, package, "Snakefile_target.smk")

            with open(snakefile_target) as file:
                target = yaml.load(file, Loader=yaml.FullLoader)
            
            input_target = target[f"rule all_{package}"]["input"]
            fd.write(f"{input_target}\n\t\t")
                    
        # Rule for each package
        for i in order_writing:
            v = user_choices[i]
            with open(os.path.join(modules_folder, i, v['package'], "Snakefile.smk")) as sf:
                fd.write(sf.read())
    
    # Draw DAG
    dag_image = os.path.join(geomosaic_dir, "dag.pdf")
    subprocess.check_call(f"snakemake -s {snakefile_filename} --dag | dot -Tpdf > {dag_image}", shell=True)


def build_pipeline_modules(graph: DiGraph, collected_modules: dict, order: list, additional_input: dict, mstart: str="m1"):
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
                queue.remove(desc)
            
            queue.popleft()
            continue
        
        user_choices[my_module] = {"package": module_choices[parse_input]["package"]}
        queue.popleft()
    
    dependencies = list(G.edges())

    # pos = graphviz_layout(G, prog="dot")
    # nx.draw(G, pos, with_labels=True, arrows=True)
    # plt.show()
    order_writing = list(nx.bfs_tree(G, source=mstart).nodes())

    return user_choices, dependencies, G, order_writing


def ask_additional_parameters(additional_input, order_writing):
    additional_parameters = {}

    for module in order_writing:
        if module in additional_input:
            for adt_param, adt_param_desc in additional_input[module].items():
                input_adt_param = get_user_path(adt_param_desc)
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



def import_graph(edges: dict) -> DiGraph:
    g = nx.DiGraph()
    for s, targets in edges.items():
        for t in targets:
            g.add_edge(s, t)
    
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
