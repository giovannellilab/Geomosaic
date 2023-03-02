#!/usr/bin/env python3
#

import networkx as nx
import json
from networkx.classes import DiGraph
import yaml
from parse_sample_table import main as parse_sample_table



def main():
    samples_list, wdir_geomosaic = parse_sample_table()

    modules_folder = "modules"
    with open('gmpackages.json', 'r') as f:
        gmpackages = json.load(f)

    g = import_graph(gmpackages["graph"])

    print("\nChoose your workflow...")
    user_choices, deps = user_input_order(g, gmpackages["modules"])
    for s, t in deps:
        user_choices[t]["previous"] = user_choices[s]["package"]

    print(user_choices)

    # print(user_choices)
    config_filename = "config.yaml"
    config = {}
    config["SAMPLES"] = samples_list[:1]
    config["WDIR"] = wdir_geomosaic

    for i, v in user_choices.items():
        if "previous" in v:
            config[f"PRE_{v['package'].upper()}"] = v['previous']

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


def user_input_order(G: DiGraph, modules: dict):
    dfs = list(nx.dfs_preorder_nodes(G, source="m1"))
    dependencies = list(nx.dfs_edges(G, source="m1"))
    user_choices = {}
    for n in dfs:
        status = False
        choices = {idx: {"name": v[0], "package": v[1]} for idx, v in enumerate(list(modules[n]["choices"].items()), start=1)}
        prompt = [f"{k}) {v['name']}" for k, v in choices.items()]
        while not status:
            print(modules[n]["description"])
            print("\n".join(prompt))

            raw_input = input()

            status, obj = check_user_input(raw_input, list(choices.keys()))
            if not status:
                print(obj)
        
        print("============================\n")
        parse_input = obj
        user_choices[n] = {"package": choices[parse_input]["package"]}
    
    return user_choices, dependencies


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




if __name__ == "__main__":
    main()
