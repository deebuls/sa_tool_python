import sys
import os.path
sys.path.append(
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import sa_tool
import networkx as nx

if __name__ == '__main__' :
    B = nx.Graph(name=" Tank System")
    B.add_nodes_from(['h', 'h_dot', 'q_i', 'q_o'], bipartite=0, color='r', type='unknown') # Add the node attribute "bipartite"
    B.add_nodes_from(['u', 'y'], bipartite=0, color='r', type='known') # Add the node attribute "bipartite"
    B.add_nodes_from(['c1','c2','c3', 'c4', 'c5', 'c6'], bipartite=1, color='b')
    B.add_edges_from([('u','c2'),('u','c5')])
    B.add_edges_from([('h_dot','c1'),('h_dot','c6') ])
    B.add_edges_from([('h','c6'),('h','c3'),('h','c4') ])
    B.add_edges_from([('h', 'c6')], derivative_casuality=True)
    B.add_edges_from([('q_i','c1'),('q_i','c2')])
    B.add_edges_from([('q_o','c3'),('q_o','c1')])
    B.add_edges_from([('y','c5'),('y','c4')])

    sa1 = sa_tool.SATool(B)
    sa1.visualize_bipartite(with_orientation=True)
    sa1.list_all_analytic_redundancy_relations()
    sa1.list_all_detectable_constratints()
