# Embedded file name: /data/dataDeebul/3Sem_MAS/fdd/fault_structure_analysis_tool/networkx/sa_tool/sa_tool.py
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import pulp
import string
from collections import defaultdict

class SATool:
    """"
    Class for doing structural analysis using graphs.
    The class takes the graph produced by networkx and
    provides manipulation on the data
    """

    def __init__(self, graph):
        if False == nx.is_bipartite(graph):
            print '[ERROR]Not a bipartite graph provided.'
            sys.exit()
        self.G = graph
        self.D = graph.to_directed()
        self.variables, self.constraints = nx.bipartite.sets(self.G)
        Y = list(self.variables)
        if self.G.node[Y[0]]['bipartite'] == 1:
            X = self.constraints
            self.constraints = self.variables
            self.variables = X
        try:
            known = []
            unknown = []
            for n in self.variables:
                if self.G.node[n]['type'] == 'known':
                    known.append(n)
                elif self.G.node[n]['type'] == 'unknown':
                    unknown.append(n)
                else:
                    print "[ERROR] Please specify for each node type as 'known' or 'unknown'"
                    sys.exit()

            self.known = set(known)
            self.unknown = set(unknown)
        except KeyError:
            print "[ERROR] Please specify for each node type as 'known' or 'unknown'"
            sys.exit()

        # Creating Reduced Graph
        self.R = self.G.copy()

        # Removing known varaibles
        self.R.remove_nodes_from(self.known)

        # Removing nodes(constraints) with no edges
        solitary=[ n for n,d in self.R.degree().items() if d==0 ]
        self.reduced_constraints = self.constraints - set(solitary)
        self.R.remove_nodes_from(solitary)

        # Removing edges which cannot be matched . provided by user 
        for x, y in self.G.edges():
            if 'derivative_casuality' in self.G[x][y]:
                self.R.remove_edge(x, y)

    def calculate_matching_ranking_constraints(self):
        """
        Calculating the maximum matching based in the ranking.
        Ranking is take as the degree of the nodes(constraints)
        The algorithm is based on the Ranking algorithm from book
        "Fault Diagnosis and Fault-tolerant Control " Chapter 5.
        
        "The idea is to start with constraint with smallest number of edges
        with variables and to propagate step by step by matching constraint 
        and unmatched variable step "
        
        Pre requisitive:
            All the unkown variables are considered as unmatched variables
            Reduced Graph is used.
        Algorithm :
            1. Find the degree of all the nodes(constraints) -> Degree is the number of edges the nodes have.
            2. Loop on the nodes starting from node with smallest degree
            3. For each node(constraint) -> Find the neighbors(variables)
            4. for each neighbor -> check if the neighbor(variable) is in the matched variable list
                if present then 
                    add the (constraint-variable) pair to the matching list
                    remove the variable from the unmatched constraint list
                    break since the constraint is matched
        
        Output :
            Maximum matching
        
        Assumptions :
            
        """
        unmatched_variables = self.unknown.copy()
        unmatched_constraints = self.reduced_constraints.copy()
        max_matching = []
        degree_of_constraints = self.R.degree(self.reduced_constraints)
        ddict = defaultdict(list)
        for k, v in degree_of_constraints.items():
            ddict[v].append(k)

        for deg in ddict:
            for constraint in ddict[deg]:
                variables = self.R.neighbors(constraint)
                for variable in variables:
                    if variable in unmatched_variables:
                        max_matching.append((constraint, variable))
                        unmatched_variables.remove(variable)
                        unmatched_constraints.remove(constraint)
                        break

        self.max_match_dict = dict(max_matching)
        self.max_match_list = max_matching
        self.unmatched_constraints = unmatched_constraints 
        print 'Max Matching : ', max_matching

    def calculate_maximum_matching(self):
        try:
            self.max_match_dict = nx.algorithms.bipartite.maximum_matching(self.R)
            self.max_match_list = list(self.max_match_dict.items())
            print self.max_match_list
        except:
            print 'Networkx Development version required for calculationg maximum matching'
            print 'Please read Installation instructions '
            exit()

    def calculate_orientation(self):
        """
        bipartite =1 means the node is a constraint node
        constructing the orientation graph .
        Orientation :
            For matched constraints :
                from non-matched variable to constraint
                from constraint to matched variable
            for non matched constraints :
                from all varaibles to constraints
                
        Algo :
            The max matching list contains edge in both direction 
            i.e. from constraint to variables and variables to constraints
            loop on the matching list
            check if the edge startd from a constraint node
            if yes 
                add the edge to the orientation list
                find connected nodes of the constraint node
                add edge from connected node to the constraint node
        """
        self.calculate_matching_ranking_constraints()
        self.orientation_graph = []
        for e in self.max_match_list:
            if self.D.node[e[0]]['bipartite'] == 1:
                self.orientation_graph.append(e)
                for s in self.D.successors(e[0]):
                    if s != e[1]:
                        self.orientation_graph.append((s, e[0]))

        for constraint in self.unmatched_constraints:
            for variable in self.D.successors(constraint):
                self.orientation_graph.append((variable, constraint))

    def test_for_obseravable_monitorable(self):
        '''
        Blamke Pg : 163
        "As all constraints are ranked, the system is fully obserable and monitorable."
        Steps for finding monitorability :
            1 Ranking of constratints
                Algo 5.3 Pg 142
            2 Based on result coment on the monitorability 
        '''

    def list_all_analytic_redundancy_relations(self):
        '''
        Blanke Pg : 162
        "Redundancy relations are composed of alternated chains, which start 
        with known variables and which end with non-matched constratints whose
        output is ZERO"

        Steps :
            1 Start with the oriented graph 
            2 Find path from Known variable to non matched contratins

        TODO:
        Open question : 
        1. There are 2 known variable ? so from which to take the path
        2. There are 2 constraints ? I think we have to consider all the constraint
        3. There are multiple path ? so which path
        '''
        print "Known Variables :",self.known
        print "Unmatched contratins :",self.unmatched_constraints

        self.residuals = []

        for v in self.known:
            for c in self.unmatched_constraints:
                paths =  nx.all_simple_paths(self.D, v, c )
                for path in paths:
                    self.residuals.append(list(path))
    
        for path in self.residuals:
            print "RESIDUAL PATH : ", path

    def list_all_detectable_constratints(self):
        '''
        Blanke Pg 164
        Defn : Structural Detectablitiy
            A violation of constraint c is structurally detectable if and only
            if it has a non-zero Boolean signature in some residual r

        Steps:
            1 Find all the analytic redundant relations
            2 Create a matrix of relation to constraints. constraint flag set 
            to true if constraint flag appears in the relations
            3 return all the constraints for whom there is atleast 1 boolean flag
            set
        '''

        self.detectable_constraints = []
        for constraint in self.constraints:
            for path in self.residuals:
                if constraint in path:
                    self.detectable_constraints.append(constraint)
                    break;

        print "Detectable Constraints are : ", self.detectable_constraints


    def list_all_isolable_constratints(self):
        '''
        Blanke Page 164
        Defn : Structural Isolability
            
        Steps :
            1 Find all the analytic redundant relations
            2 Create a matrix of relation to constraints. constraint flag set 
            to true if constraint flag appears in the relations
            3 Return those constraints which for a particular relation is the 
                only flag . i.e. no other constraint has boolean set for the particular
                relation except this constraint
        '''



    def visualize_bipartite(self, with_matching = False, with_orientation = False):
        pos = dict()
        pos.update(((n, (1, i)) for i, n in enumerate(self.constraints)))
        pos.update(((n, (2, i)) for i, n in enumerate(self.variables)))
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
        nx.draw_networkx_nodes(self.G, pos, ax=ax1, nodelist=self.known, node_color='m', node_size=500, alpha=0.8)
        nx.draw_networkx_nodes(self.G, pos, ax=ax1, nodelist=self.unknown, node_color='g', node_size=500, alpha=0.8)
        nx.draw_networkx_nodes(self.G, pos, ax=ax1, nodelist=self.constraints, node_color='y', node_size=500, alpha=0.8)
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_labels(self.G, pos)
        fig.suptitle(self.G.name, fontsize=14, fontweight='bold')
        if with_matching:
            ax1.set_title('Max Matching')
            self.calculate_matching_ranking_constraints()
            nx.draw_networkx_edges(self.G, pos, ax=ax1, edgelist=self.max_match_list, width=8, alpha=0.3, edge_color='b')
        if with_orientation:
            ax1.set_title('With Orientation')
            self.calculate_matching_ranking_constraints()
            nx.draw_networkx_edges(self.G, pos, ax=ax1, edgelist=self.max_match_list, width=5, alpha=0.3, edge_color='b')
            self.calculate_orientation()
            nx.draw_networkx_nodes(self.G, pos, ax=ax1, nodelist=self.unmatched_constraints, node_color='r', node_size=500, alpha=0.8)
            nx.draw_networkx_edges(self.D, pos, ax=ax1, edgelist=self.orientation_graph, arrows=True, width=1, alpha=0.5)
        fig.suptitle(self.G.name, fontsize=14, fontweight='bold')
        plt.show()
