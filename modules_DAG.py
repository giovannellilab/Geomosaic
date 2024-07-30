#!/usr/bin/env python3
#

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import numpy as np
import matplotlib.patheffects as pe


def main():
    with open('src/geomosaic/gmpackages.json', 'r') as f:
        gmpackages = json.load(f)

    G = import_graph(gmpackages["graph"])

    #### CODE DRAW
    ############################################
    ############################################
    ############################################
    
    bfs_preprocessing = nx.bfs_tree(G, "pre_processing")
    bfs_preprocessing.remove_node("assembly")
    bfs_preprocessing.remove_node("binning")

    bfs_assembly = nx.bfs_tree(G, "assembly")
    bfs_assembly.remove_node("binning")

    bfs_binning = nx.bfs_tree(G, "binning")

    pure_preproc_nodes = [x for x in bfs_preprocessing.nodes() if x not in list(bfs_assembly.nodes()) + list(bfs_binning.nodes())]
    pure_assembly_nodes = [x for x in bfs_assembly.nodes() if x not in list(bfs_binning.nodes())]
    pure_binning_nodes = list(bfs_binning.nodes())

    # Computing Layers through the longest shortest path

    bfs_preproc_layers = {
        0: ["pre_processing"]
    }
    for target in pure_preproc_nodes:
        if target == "pre_processing":
            continue
        
        len_lp = len(get_longest_path(G, "pre_processing", target)) - 1
        
        if len_lp not in bfs_preproc_layers:
            bfs_preproc_layers[len_lp] = []

        bfs_preproc_layers[len_lp].append(target)
    
    bfs_assembly_layers = {
        0: ["assembly"]
    }
    for target in pure_assembly_nodes:
        if target == "assembly":
            continue
        
        len_lp = len(get_longest_path(G, "assembly", target)) - 1
        
        if len_lp not in bfs_assembly_layers:
            bfs_assembly_layers[len_lp] = []

        bfs_assembly_layers[len_lp].append(target)


    bfs_binning_layers = {
        0: ["binning"]
    }
    for target in pure_binning_nodes:
        if target == "binning":
            continue

        if target not in ["binning_qa", "binning_derep"]:
            # In this way "mags_retrieval" is in the same layer of "binning_qa"
            len_lp = len(get_longest_path(G, "binning", target)) - 2
        else:
            len_lp = len(get_longest_path(G, "binning", target)) - 1
        
        if len_lp not in bfs_binning_layers:
            bfs_binning_layers[len_lp] = []

        bfs_binning_layers[len_lp].append(target)

    pos = {"pre_processing": np.array([0, 0])}
    y_shift = 15

    preproc_y = pos["pre_processing"][1] + y_shift
    for l, modules_list in bfs_preproc_layers.items():
        if l == 0:
            continue
        
        preproc_x = pos["pre_processing"][0] + 2.6
        
        flag_inserted = False
        for m in modules_list:
            pos[m] = np.array([preproc_x, preproc_y])
            preproc_x += 2.6
            flag_inserted = True
        
        if flag_inserted:
            preproc_y += y_shift
    
    pos["assembly"] = np.array([0, preproc_y])
    assembly_y = pos["assembly"][1] + y_shift
    for l, modules_list in bfs_assembly_layers.items():
        if l == 0:
            continue
        
        assembly_x = pos["assembly"][0]+2.7
        
        flag_inserted = False
        for m in modules_list:
            pos[m] = np.array([assembly_x, assembly_y])
            assembly_x += 2.7
            flag_inserted = True
        
        if flag_inserted:
            assembly_y += y_shift

    pos["binning"] = np.array([0, assembly_y])
    binning_y = pos["binning"][1] + y_shift
    for l, modules_list in bfs_binning_layers.items():
        if l == 0:
            continue
        
        binning_x = pos["binning"][0]+2.8

        flag_inserted = False
        for m in modules_list:
            pos[m] = np.array([binning_x, binning_y])
            binning_x += 2.8
            flag_inserted = True

        if flag_inserted:
            binning_y += y_shift

    ####################################################
    ####################################################
    ####################################################

    assert len(pos) == len(G.nodes())

    new_pos = {}
    max_layer_y = max([j[1] for i, j in pos.items()])+1
    for i, j in pos.items():
        new_pos[i] = np.array([j[0], max_layer_y - j[1]])
    
    pos_labels_attrs = {}
    for node, coords in new_pos.items():
        pos_labels_attrs[node] = (coords[0], coords[1] + 4)

    draw_graph(G, new_pos, pos_labels_attrs)
    draw_white_graph(G, new_pos, pos_labels_attrs)
    draw_workflow_graph(G, new_pos, pos_labels_attrs)


def import_graph(edges: list):
    g = nx.DiGraph()
    for source, target in edges:
        g.add_edge(source, target)
    
    return g


def draw_graph(G, new_pos, pos_labels_attrs):
    plt.figure(figsize=(14, 13), dpi=300)
    
    nx.draw(G, 
        new_pos, 
        with_labels = False, 
        node_color=["#6699ff" if i in ["pre_processing", "assembly", "binning"] else "#82E0AA" for i in G.nodes() ], 
        alpha=0.8,
        # node_size = [len(v) * the_base_size for v in G.nodes()],
        edge_color="#999999"
    )

    for lbl, coords in pos_labels_attrs.items():
        plt.text(coords[0], coords[1], lbl, 
                 path_effects=[pe.withStroke(linewidth=4, foreground="white")], 
                 va="center", ha="center", weight='bold')

    stream_module_legend = mpatches.Patch(color='#6699ff', label='Main stream modules')
    analysis_module_legend = mpatches.Patch(color='#82E0AA', label='Analysis stream modules')
    plt.legend(handles=[stream_module_legend, analysis_module_legend])
    plt.savefig('images/modules_DAG.png', bbox_inches='tight')
    plt.savefig('images/modules_DAG.svg', bbox_inches='tight', format="svg")


def draw_white_graph(G, new_pos, pos_labels_attrs):
    plt.figure(figsize=(14, 13), dpi=300)
    nx.draw(G, 
        new_pos, 
        with_labels = False, 
        alpha=0.8,
        edge_color="#999999"
    )

    nodes = nx.draw_networkx_nodes(G, new_pos, node_color=["white" for _ in G.nodes() ])
    nodes.set_edgecolor('gray')

    for lbl, coords in pos_labels_attrs.items():
        plt.text(coords[0], coords[1], lbl, 
                 path_effects=[pe.withStroke(linewidth=4, foreground="white")], 
                 va="center", ha="center", weight='bold')
        
    plt.savefig('images/modules_DAG_white.png', bbox_inches='tight')
    plt.savefig('images/modules_DAG_white.svg', bbox_inches='tight', format="svg")


def draw_workflow_graph(G, new_pos, pos_labels_attrs):
    plt.figure(figsize=(14, 13), dpi=300)
    choices = [
        "pre_processing",
        "assembly",
        "assembly_func_annotation",
        "assembly_readmapping",
        "assembly_tax_annotation",
        "orf_prediction",
        "assembly_orf_annotation",
        "binning",
        "binning_derep",
        "binning_qa",
        "mags_retrieval",
        "mags_metabolism_annotation",
        "mags_tax_annotation",
        "mags_coverage",
    ]

    nc = []
    skipped = ["assembly_hmm_annotation", "mags_hmm_annotation", 
               "mags_domain_annotation", "mags_func_annotation"]

    col_accepted = "#26CA94"
    col_ignored = "#F45F53"
    col_removed = "#B1B8BD"

    for i in G.nodes():
        if i in choices and i not in skipped :
            nc.append(col_accepted)
        elif i in skipped:
            nc.append(col_removed)
        else:
            nc.append(col_ignored)

    nx.draw(G, 
        new_pos, 
        with_labels = False, 
        node_color=nc, 
        alpha=0.8,
        # node_size = [len(v) * the_base_size for v in G.nodes()],
        edge_color="#999999"
    )
    
    for lbl, coords in pos_labels_attrs.items():
        plt.text(coords[0], coords[1], lbl, 
                 path_effects=[pe.withStroke(linewidth=4, foreground="white")], 
                 va="center", ha="center", weight='bold')
        
    stream_module_legend = mpatches.Patch(color=col_accepted, label='Accepted modules')
    analysis_module_legend = mpatches.Patch(color=col_ignored, label='Ignored modules')
    skipped_module_legend = mpatches.Patch(color=col_removed, label='Removed modules due to ignored dependencies')
    plt.legend(handles=[stream_module_legend, analysis_module_legend, skipped_module_legend])
    plt.savefig('images/modules_DAG_workflow.png', bbox_inches='tight')
    plt.savefig('images/modules_DAG_workflow.svg', bbox_inches='tight', format="svg")


def get_longest_path(G, source, target):
    longest_path = max(nx.all_simple_paths(G, source, target), key=lambda x: len(x))
    return longest_path


if __name__ == "__main__":
    main()
