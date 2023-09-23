#!/usr/bin/env python3
#

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.patches as mpatches
import json
import numpy as np


def main():
    with open('src/geomosaic/gmpackages.json', 'r') as f:
        gmpackages = json.load(f)

    G = import_graph(gmpackages["graph"])

    pos = {"pre_processing": np.array([0, 0])}

    bfs_preprocessing = nx.bfs_tree(G, "pre_processing")
    bfs_preprocessing.remove_node("assembly")
    bfs_preprocessing.remove_node("binning")
    bfs_preproc_layers = dict(enumerate(nx.bfs_layers(bfs_preprocessing, "pre_processing")))

    preproc_layers_node = []
    for i in bfs_preproc_layers.values():
        preproc_layers_node += i

    bfs_assembly = nx.bfs_tree(G, "assembly")
    bfs_assembly.remove_node("binning")
    bfs_assembly_layers = dict(enumerate(nx.bfs_layers(bfs_assembly, "assembly")))

    assembly_layers_node = []
    for i in bfs_assembly_layers.values():
        assembly_layers_node += i

    bfs_binning = nx.bfs_tree(G, "binning")
    bfs_binning_layers = dict(enumerate(nx.bfs_layers(bfs_binning, "binning")))

    binning_layers_node = []
    for i in bfs_binning_layers.values():
        binning_layers_node += i

    y_shift = 15

    preproc_y = pos["pre_processing"][1] + y_shift
    for l, modules_list in bfs_preproc_layers.items():
        if l == 0:
            continue
        
        preproc_x = pos["pre_processing"][0] + 0.4
        
        flag_inserted = False
        for m in modules_list:
            if m in assembly_layers_node or m in binning_layers_node:
                continue

            pos[m] = np.array([preproc_x, preproc_y])
            preproc_x += 0.4
            flag_inserted = True
        
        if flag_inserted:
            preproc_y += y_shift
    
    pos["assembly"] = np.array([0, preproc_y])

    assembly_y = pos["assembly"][1] + y_shift
    for l, modules_list in bfs_assembly_layers.items():
        if l == 0:
            continue
        
        assembly_x = pos["assembly"][0]+0.5
        
        flag_inserted = False
        for m in modules_list:
            if m in binning_layers_node:
                continue

            pos[m] = np.array([assembly_x, assembly_y])
            assembly_x += 0.5
            flag_inserted = True
        
        if flag_inserted:
            assembly_y += y_shift

    pos["binning"] = np.array([0, assembly_y])

    binning_y = pos["binning"][1] + y_shift
    for l, modules_list in bfs_binning_layers.items():
        if l == 0:
            continue
        
        binning_x = pos["binning"][0]+0.6
        
        flag_inserted = False
        for m in modules_list:
            pos[m] = np.array([binning_x, binning_y])
            binning_x += 0.6
            flag_inserted = True
        
        if flag_inserted:
            binning_y += y_shift

    assert len(pos) == len(G.nodes())

    new_pos = {}
    max_layer_y = max([j[1] for i, j in pos.items()])+1
    for i, j in pos.items():
        new_pos[i] = np.array([j[0], max_layer_y - j[1]])
    
    pos_labels_attrs = {}
    for node, coords in new_pos.items():
        pos_labels_attrs[node] = (coords[0], coords[1] + 4)


    # MANUAL SHIFTING POSITIONS
    old_genecoverage_y = new_pos["gene_coverage"][1]
    new_pos["gene_coverage"] = np.array([new_pos["assembly_qc_readmapping"][0], old_genecoverage_y])

    old_genecoverage_label_y = pos_labels_attrs["gene_coverage"][1]
    pos_labels_attrs["gene_coverage"] = np.array([pos_labels_attrs["assembly_qc_readmapping"][0], old_genecoverage_label_y])

    print(new_pos)

    plt.figure(figsize=(12, 10), dpi=300)
    
    nx.draw(G, 
        new_pos, 
        with_labels = False, 
        node_color=["#6699ff" if i in ["pre_processing", "assembly", "binning"] else "#82E0AA" for i in G.nodes() ], 
        alpha=0.8,
        # node_size = [len(v) * the_base_size for v in G.nodes()],
        edge_color="#515151"
    )
    
    nx.draw_networkx_labels(G, pos_labels_attrs)
    stream_module_legend = mpatches.Patch(color='#6699ff', label='Main stream modules')
    analysis_module_legend = mpatches.Patch(color='#82E0AA', label='Analysis stream modules')
    plt.legend(handles=[stream_module_legend, analysis_module_legend])
    plt.savefig('images/modules_DAG.png', bbox_inches='tight')
    plt.savefig('images/modules_DAG.svg', bbox_inches='tight')


def import_graph(edges: list):
    g = nx.DiGraph()
    for source, target in edges:
        g.add_edge(source, target)
    
    return g


if __name__ == "__main__":
    main()
