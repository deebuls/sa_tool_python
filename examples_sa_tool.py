import sa_tool
import networkx as nx

if __name__ == '__main__' :
    '''
    B = nx.Graph(name="Example 5.17")
    B.add_nodes_from(['x1', 'x2', 'x3', 'x4', 'x5'], bipartite=0, color='r') # Add the node attribute "bipartite"
    B.add_nodes_from(['c1','c2','c3', 'c4', 'c5', 'c6'], bipartite=1, color='b')
    B.add_edges_from([('x1','c1'),('x1','c2'),('x1','c4') ])
    B.add_edges_from([('x2','c2'),('x2','c5')])
    B.add_edges_from([('x3','c2'),('x3','c3')])
    B.add_edges_from([('x4','c3'),('x4','c4'),('x4','c6') ])
    B.add_edges_from([('x5','c5'),('x5','c6')])

    sa1 = sa_tool.SATool(B)
    sa1.visualize_bipartite()
    sa1.calculate_maximum_matching()
    sa1.visualize_bipartite(with_matching=True)
    sa1.calculate_orientation()
    sa1.visualize_bipartite(with_orientation=True)


    B = nx.Graph(name="Example 5.3 Linear System")
    B.add_nodes_from(['x1', 'x2', 'u', 'x1_dot', 'x1_dot'], bipartite=0, color='r') # Add the node attribute "bipartite"
    B.add_nodes_from(['c1','c2','c3', 'c4'], bipartite=1, color='b')
    B.add_edges_from([('u','c4')])
    B.add_edges_from([('x1','c1'),('x1','c4') ])
    B.add_edges_from([('x2','c2'),('x2','c3'),('x2','c4') ])
    B.add_edges_from([('x1_dot','c1'),('x1_dot','c2')])
    B.add_edges_from([('x2_dot','c3'),('x2_dot','c4')])

    sa1 = sa_tool.SATool(B)
    sa1.visualize_bipartite()
    sa1.calculate_maximum_matching()
    sa1.visualize_bipartite(with_matching=True)
    sa1.calculate_orientation()
    sa1.visualize_bipartite(with_orientation=True)

    '''

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
    #sa1.calculate_maximum_matching_max_flow_algorithm()
    #sa1.visualize_bipartite()
    sa1.calculate_maximum_matching()
    #sa1.visualize_bipartite(with_matching=True)
    sa1.calculate_orientation()
    #sa1.visualize_bipartite(with_orientation=True)
    sa1.list_all_analytic_redundancy_relations()


    '''
    B = nx.Graph(name=" Tank System")
    B.add_nodes_from(['h', 'h_dot', 'q_i', 'q_o'], bipartite=0, color='r', type='unknown') # Add the node attribute "bipartite"
    B.add_nodes_from(['c1','c2','c3', 'c4', 'c5', 'c6'], bipartite=1, color='b')
    B.add_edges_from([('h_dot','c1'),('h_dot','c6') ])
    B.add_edges_from([('h','c3'),('h','c4') ])
    B.add_edges_from([('q_i','c1'),('q_i','c2')])
    B.add_edges_from([('q_o','c3'),('q_o','c1')])

    sa1 = sa_tool.SATool(B)
    sa1.visualize_bipartite()
    sa1.calculate_maximum_matching()
    sa1.visualize_bipartite(with_matching=True)
    sa1.calculate_orientation()
    sa1.visualize_bipartite(with_orientation=True)

    ''' 
