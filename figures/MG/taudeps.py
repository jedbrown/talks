#!/usr/bin/env python2

import networkx as nx
import matplotlib.pyplot as plt

def visit(G,uc,level,part,tauc):
    u1 = add_node(G, '$u_{%d,%d}$' % (level,part))
    G.add_edge(uc,u1)
    tau1 = visit_taumg(G,u1,level,part)
    G.add_edge(tau1,tauc)
def visit_taumg(G,uc,level,part):
    if level < 3:
        name = '$\\tau_%d^{%d,%d}$' % (level+1,level,part)
        if level == 0:
            name = '$\\tau_1^0$'
        tauc = add_node(G, name)
        for i in range(3):
            ct = visit(G,uc,level+1,10*part+i,tauc)
        return tauc
    else:
        return uc

def add_node(G,name):
    G.add_node(name)
    return name

def shift(pos, node, dx, dy):
    loc = pos[node]
    pos[node] = (loc[0] + dx, loc[1] + dy)

def main():
    G = nx.DiGraph()
    coarse_u = add_node(G, '$u_0$')
    coarse_tau = visit_taumg(G,coarse_u,0,0)

    pos = nx.graphviz_layout(G)
    othernodes = [n for n in G.nodes() if n not in [coarse_u, coarse_tau]]
    shift(pos, coarse_u, -20, 30)
    shift(pos, coarse_tau, 15, -30)

    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    nx.draw_networkx_nodes(G, pos, nodelist=othernodes, node_color='#aaddbb')
    nx.draw_networkx_nodes(G, pos, nodelist=[coarse_u], node_color='#5566dd')
    nx.draw_networkx_nodes(G, pos, nodelist=[coarse_tau], node_color='#dd5566')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, size=24)
    plt.savefig('taudeps.pdf')
    # run pdfcrop

if __name__ == '__main__':
    main()
