import networkx as nx
from pyvis.network import Network
import os
import sqlite3
from get_data import get_clean_info
import math
from subprocess import run
import matplotlib.pyplot as plt

def create_graph(connections: list):
    G = nx.Graph()
    
    for tup in connections:
        home_name = tup[0]
        branch_name = tup[1]
        G.add_edge(home_name, branch_name)

    # Precompute the layout using NetworkX with a larger distance
    pos = nx.spring_layout(G, k=1.0, iterations=50, seed=42)  # 'k' increased for more spacing
    
    # Create a Pyvis Network
    net = Network(notebook=True, height='750px', width='100%')
    
    # Calculate degrees and assign positions, sizes, and colors
    degrees = dict(G.degree())
    colormap = plt.cm.viridis
    max_degree = max(degrees.values())
    
    for node in G.nodes:
        x, y = pos[node]
        degree = degrees[node]
        size = math.log(degree + 1) * 10
        normalized_degree = degree / max_degree
        rgba_color = colormap(normalized_degree)
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(rgba_color[0] * 255), 
            int(rgba_color[1] * 255), 
            int(rgba_color[2] * 255)
        )
        net.add_node(node, x=x*1000, y=y*1000, size=size, title=node, color=hex_color, label='')
    
    # Add edges
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])
    
    # Disable physics in Pyvis and set options to ensure static layout
    net.set_options('''
    var options = {
      "configure": {
        "enabled": true,
        "filter": "nodes, physics"
      },
      "interaction": {
        "hover": true
      },
      "nodes": {
        "font": {
          "size": 0
        }
      },
      "physics": {
        "enabled": false,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.3,
          "springLength": 250,
          "springConstant": 0.04,
          "damping": 0.09
        }
      }
    }
    ''')
    
    # Display the network
    net.show('network.html')

    # Open the result in a web browser
    run(['open', 'network.html'])

# Execute the function to create the graph from your data
create_graph(get_clean_info())