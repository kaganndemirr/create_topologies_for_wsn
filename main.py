import random
import string
import pathlib
import os

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

alphabet = list(string.ascii_uppercase)

topology_number = 10

dir_path = os.path.dirname(os.path.realpath(__file__))

xml_output_location = os.path.join(dir_path, "topologies")

if not os.path.isdir(xml_output_location):
    pathlib.Path(xml_output_location).mkdir(parents=True, exist_ok=True)

for graphs in range(topology_number):

    node_names_for_xml = []
    edges_for_xml = []

    branch_number = random.randint(2, 10)
    depth = random.randint(2, 10)

    G = nx.Graph()

    G.add_node("R")
    node_names_for_xml.append('\t\t<node id="ES_R" />\n')

    for i in range(branch_number):
        node_name = alphabet[i % len(alphabet)] + str(i)
        node_names_for_xml.append('\t\t <node id="ES_' + str(node_name) + '" />\n')
        G.add_node(node_name)
        G.add_edge("R", node_name)
        edges_for_xml.append('\t\t <edge source="ES_R' + '" target="ES_' + str(node_name) + '" />\n')

    z = 0
    j = 0
    for i in range(2, depth + 1):
        how_many_node_for_dept = random.randint(2, 10)
        assign_nodes_to_list = []
        temp_how_many_node_for_dept = how_many_node_for_dept
        while temp_how_many_node_for_dept > 0:
            how_many_node_for_branch = random.randint(1, temp_how_many_node_for_dept)
            assign_nodes_to_list.append(how_many_node_for_branch)
            temp_how_many_node_for_dept = temp_how_many_node_for_dept - how_many_node_for_branch
        for k in assign_nodes_to_list:
            for t in range(k):
                node_name = alphabet[(z + branch_number) % len(alphabet)] + str(z + branch_number)
                G.add_node(node_name)
                node_names_for_xml.append('\t\t <node id="ES_' + str(node_name) + '" />\n')
                index = j % len(alphabet)
                parent_node_name = alphabet[index] + str(j)
                node_names_for_xml.append('\t\t <node id="ES_' + str(parent_node_name) + '" />\n')
                G.add_edge(parent_node_name, node_name)
                edges_for_xml.append('\t\t <edge source="ES_' + str(parent_node_name) + '" target="ES_' + str(node_name) + '" />\n')
                z += 1
            j += 1

    with open(os.path.join(xml_output_location, "DAG_" + str(graphs + 1) + ".xml"), "w") as graph_file:
        graph_file.write('<graphml >\n')
        graph_file.write('\t<graph id="G" edgedefault="undirected">\n')

        for nodes in node_names_for_xml:
            graph_file.write(nodes)
    
        for edges in edges_for_xml:
            graph_file.write(edges)

        graph_file.write('\t</graph >\n')
        graph_file.write('</graphml >\n')

    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True)
    plt.savefig("DAG_" + str(graphs + 1) + ".png")
    plt.clf()

