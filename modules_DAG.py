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
        
        preproc_x = pos["pre_processing"][0] + 0.5
        
        flag_inserted = False
        for m in modules_list:
            if m in assembly_layers_node or m in binning_layers_node:
                continue

            pos[m] = np.array([preproc_x, preproc_y])
            preproc_x += 0.5
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

    # ## ---> ## MANUAL SHIFTING POSITIONS ## <--- ##
    # # Assembly coverage
    # old_assemblycoverage_y = new_pos["assembly_coverage"][1]
    # new_pos["assembly_coverage"] = np.array([new_pos["assembly_readmapping"][0], old_assemblycoverage_y])

    # old_assemblycoverage_label_y = pos_labels_attrs["assembly_coverage"][1]
    # pos_labels_attrs["assembly_coverage"] = np.array([pos_labels_attrs["assembly_readmapping"][0], old_assemblycoverage_label_y])

    # # Gene Coverage
    # old_genecoverage_y = new_pos["gene_coverage"][1]
    # new_pos["gene_coverage"] = np.array([new_pos["assembly_readmapping"][0]+0.3, old_genecoverage_y])

    # old_genecoverage_label_y = pos_labels_attrs["gene_coverage"][1]
    # pos_labels_attrs["gene_coverage"] = np.array([pos_labels_attrs["assembly_readmapping"][0]+0.35, old_genecoverage_label_y])

    # # Domain annotation
    # old_domainannotation_y = new_pos["domain_annotation"][1]
    # new_pos["domain_annotation"] = np.array([new_pos["orf_prediction"][0]+0.2, old_domainannotation_y])

    # old_domainannotation_label_y = pos_labels_attrs["domain_annotation"][1]
    # pos_labels_attrs["domain_annotation"] = np.array([pos_labels_attrs["orf_prediction"][0]+0.2, old_domainannotation_label_y])

    print(new_pos)

    draw_graph(G, new_pos, pos_labels_attrs)
    draw_white_graph(G, new_pos, pos_labels_attrs)
    draw_workflow_graph(G, new_pos, pos_labels_attrs)


def import_graph(edges: list):
    g = nx.DiGraph()
    for source, target in edges:
        g.add_edge(source, target)
    
    return g


def draw_graph(G, new_pos, pos_labels_attrs):
    plt.figure(figsize=(12, 10), dpi=300)
    
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
    plt.figure(figsize=(12, 10), dpi=300)
    nx.draw(G, 
        new_pos, 
        with_labels = False, 
        alpha=0.8,
        edge_color="#515151"
    )

    nodes = nx.draw_networkx_nodes(G, new_pos, node_color=["white" for _ in G.nodes() ])
    nodes.set_edgecolor('gray')

    for lbl, coords in pos_labels_attrs.items():
        plt.text(coords[0], coords[1], lbl, path_effects=[pe.withStroke(linewidth=4, foreground="white")], va="center", ha="center")
        
    plt.savefig('images/modules_DAG_white.png', bbox_inches='tight')
    plt.savefig('images/modules_DAG_white.svg', bbox_inches='tight', format="svg")


def draw_workflow_graph(G, new_pos, pos_labels_attrs):
    plt.figure(figsize=(12, 10), dpi=300)
    choices = [
        "pre_processing",
        "assembly",
        "assembly_readmapping",
        "assembly_tax_annotation",
        "orf_prediction",
        "assembly_func_annotation",
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
        edge_color="#515151"
    )
    
    for lbl, coords in pos_labels_attrs.items():
        plt.text(coords[0], coords[1], lbl, path_effects=[pe.withStroke(linewidth=4, foreground="white")], va="center", ha="center")
        
    stream_module_legend = mpatches.Patch(color=col_accepted, label='Accepted modules')
    analysis_module_legend = mpatches.Patch(color=col_ignored, label='Ignored modules')
    skipped_module_legend = mpatches.Patch(color=col_removed, label='Removed modules due to ignored dependencies')
    plt.legend(handles=[stream_module_legend, analysis_module_legend, skipped_module_legend])
    plt.savefig('images/modules_DAG_workflow.png', bbox_inches='tight')
    plt.savefig('images/modules_DAG_workflow.svg', bbox_inches='tight', format="svg")


if __name__ == "__main__":
    main()
