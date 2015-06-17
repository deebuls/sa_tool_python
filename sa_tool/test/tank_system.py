import sys
import os
import networkx as nx

topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                           os.pardir, os.pardir))
if os.path.exists(os.path.join(topdir, "targetDir", "__init__.py")):
        sys.path.insert(0, topdir)
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 

import sa_tool

if __name__ == '__main__' :
    B = nx.Graph()
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
    #sa1.calculate_maximum_matching_max_flow_algorithm()
    sa1.visualize_bipartite()
    sa1.calculate_maximum_matching()
    sa1.visualize_bipartite(with_matching=True)
    sa1.visualize_bipartite(with_orientation=True)
    
