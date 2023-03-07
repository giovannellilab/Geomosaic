#!/usr/bin/env python3
#

import networkx as nx
import json
from networkx.classes import DiGraph
import yaml
from parse_sample_table import parse_sample_table
from argparse import ArgumentParser
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout



def main():
    args = parse_args()

    folder_raw_reads = args.directory
    working_dir = args.working_dir
    sample_table = args.sample_table

    samples_list, wdir_geomosaic = parse_sample_table(folder_raw_reads, working_dir, sample_table)

    modules_folder = "modules"
    # with open('gmpackages_dummy.json', 'r') as f:
    with open('gmpackages.json', 'r') as f:
        gmpackages = json.load(f)

    G = import_graph(gmpackages["graph"])
    collected_modules = gmpackages["modules"]

    mstart = "m1"
    user_choices, dependencies, modified_G = build_pipeline_modules(G, collected_modules, mstart=mstart)

    # print(user_choices)
    config_filename = "config.yaml"
    config = {}
    config["SAMPLES"] = samples_list[:1]
    config["WDIR"] = wdir_geomosaic

    for _, pckg_info in user_choices.items():
        if "previous" in pckg_info:
            config[f"PRE_{pckg_info['package'].upper()}"] = pckg_info['previous']

    with open(config_filename, 'w') as fd_config:
        yaml.dump(config, fd_config)

    with open("Snakefile", "wt") as fd:
        fd.write(f"configfile: {str(repr(config_filename))}\n")

        # Rule ALL
        fd.write("\nrule all:\n\tinput:\n\t\t")
        for m in sorted(user_choices.keys()):
            package = user_choices[m]["package"]
            snakefile_target = f"{modules_folder}/{m}/{package}/Snakefile_target"

            with open(snakefile_target) as file:
                target = yaml.load(file, Loader=yaml.FullLoader)
            
            input_target = target[f"rule all_{package}"]["input"]
            print(input_target)
            fd.write(f"{input_target}\n\t\t")
                    
        # Rule for each package
        for i, v in user_choices.items():
            with open(f"{modules_folder}/{i}/{v['package']}/Snakefile") as sf:
                fd.write(sf.read())


def build_pipeline_modules(graph: DiGraph, collected_modules: dict, mstart: str="m1"):
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
    queue = deque(list(nx.bfs_tree(G, source=mstart).nodes()))

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
    
    dependencies = list(nx.dfs_edges(G, source=mstart))

    for module_source, module_target in dependencies:
        user_choices[module_target]["previous"] = user_choices[module_source]["package"]

    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, arrows=True)
    plt.show()

    return user_choices, dependencies, G


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


def parse_args():
    parser = ArgumentParser(description="Script to parse user samples table")
    parser.add_argument("-d", "--directory", required=True, type=str, help="Path to the directory containing raw reads (fastq.gz files)")
    parser.add_argument("-w", "--working_dir", required=True, type=str, help="Path to the working directory for geomosaic")
    parser.add_argument("-s", "--sample_table", required=True, type=str, help="Path to the user sample table")
    return parser.parse_args()


if __name__ == "__main__":
    main()
