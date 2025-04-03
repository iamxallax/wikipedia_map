import networkx as nx
from pyvis.network import Network
import os
import sqlite3
from get_data import get_list
import webbrowser
import math

def create_graph(connections:list):
    G = nx.Graph()
    
    # Create the NetworkX graph
    for tup in connections:
        home_name = tup[0]
        branch_name = tup[1]
        if not home_name in G.nodes:
            G.add_node(home_name)
        if not branch_name in G.nodes:
            G.add_node(branch_name)
        G.add_edge(home_name, branch_name)
    
    # Create a Pyvis Network
    net = Network(notebook=True, height='750px', width='100%')
    net.from_nx(G)

    # Calculate degrees and scale node sizes logarithmically
    degrees = dict(G.degree())
    for node in net.nodes:
        degree = degrees[node['id']]
        node['size'] = math.log(degree + 1) * 10  # Adjust multiplier for desired scaling
        node['label'] = ''
        node['title'] = node['id']
    
    # Set options with modified physics settings for spreading nodes
    net.set_options('''
    var options = {
      "configure": {
        "enabled": true,
        "filter": "nodes, physics"
      },
      "interaction": {
        "hover": true
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -2000,
          "centralGravity": 0.3,
          "springLength": 200,
          "springConstant": 0.04,
          "damping": 0.09
        }
      }
    }
    ''')

    # Display the network
    net.show('network.html')

    # Cleanup
    os.remove('links.db')

# Execute the function to create the graph from your data
create_graph(get_list())

# Open the result in a web browser
webbrowser.open('network.html')