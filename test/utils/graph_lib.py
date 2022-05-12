#!/usr/bin/env python3
######################################################
# File: graph_lib.py
# Author: Bart Gajderowicz
# Date: May 6, 2022
# Description:
#   Helper functions for graphing netowrkx graphs
######################################################

import re, colorsys, random, os
from pyvis import network as pvnet

dir_path = os.path.dirname(os.path.realpath(__file__))
report_path = dir_path + '/../../report/'


def plot_g_pyviz(G, filename='out.html', dir=report_path, height='95%', width='100%', notebook=False, subtitle=None):
    _ = os.makedirs(dir) if not os.path.exists(dir) else None
    g = G.copy()  # some attributes added to nodes
    title = filename.split('.')[0].replace('_', ' ').upper()
    if subtitle:
        title = f"<h1>{title}: <i>{subtitle}</i></h1>"
    net = pvnet.Network(notebook=notebook, directed=True, height=height, width=width, heading=title)
    opts = '''
        var options = {
          "physics": {
            "enabled": true
          },
            "minVelocity": 0.05,
            "timestep": 0.22,
            "forceAtlas2Based": {
              "gravitationalConstant": -100,
              "centralGravity": 0.11,
              "springLength": 100,
              "springConstant": 0.09,
              "avoidOverlap": 1
            },
          "barnesHut":{
             "gravitationalConstant": 100,
              "avoidOverlap": 1
          },
          "solver":"barnesHut"
        }
    '''

    net.set_options(opts)
    # uncomment this to play with layout
    # pvnet.stabilize(2000)
    # net.show_buttons(filter_=['physics'])
    net.from_nx(g)
    net.save_graph(dir + '/' + filename)
    # return net.show(dir + '/' + filename)
