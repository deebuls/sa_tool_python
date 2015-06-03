import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import pulp
import string
class SATool:
    """"
    Class for doing structural analysis using graphs.
    The class takes the graph produced by networkx and
    provides manipulation on the data
    """

    def __init__(self, graph):
        if (False == nx.is_bipartite(graph)):
            print "[ERROR]Not a bipartite graph provided."
            sys.exit()

        #Copying the graph provided by the user
        self.G = graph
        
        #Creating a Directed graph with all bidirectional edges
        self.D = graph.to_directed()

        #Separating the variables and constraints
        self.variables, self.constraints = nx.bipartite.sets(self.G)

        #Ensuring that the bipartite == 1 is assigned to varaibles
        Y = list(self.variables)
        if (self.G.node[Y[0]]['bipartite'] == 1):
            X = self.constraints
            self.constraints = self.variables
            self.variables = X

        #Separating the known and the unknown variables
        try:
            known = []
            unknown = []
            for n in self.variables:
                if (self.G.node[n]['type'] == 'known'):
                    known.append(n)
                elif (self.G.node[n]['type'] == 'unknown'):
                    unknown.append(n)
                else:
                    print "[ERROR] Please specify for each node type as 'known' or 'unknown'"
                    sys.exit()

            self.known = set(known)
            self.unknown = set(unknown)
        except KeyError:
                print "[ERROR] Please specify for each node type as 'known' or 'unknown'"
                sys.exit()

        #Creating reduced graph by removing known variables
        self.R = self.G.copy()
        self.R.remove_nodes_from(self.known)

        #Removing edges which cannot be matched
        #Example with derivative casuality
        for x,y in  self.G.edges():
            if 'derivative_casuality' in self.G[x][y] :
                self.R.remove_edge(x,y)


    def calculate_maximum_matching(self):
        try:
            self.max_match_dict = nx.algorithms.bipartite.maximum_matching(self.R)
            self.max_match_list = list(self.max_match_dict.items())
            print self.max_match_list
        except:
            print "Networkx Development version required for calculationg maximum matching"
            print "Please read Installation instructions "
            exit()

    def calculate_maximum_matching_max_flow_algorithm(self):
        '''
        Using Max flow algorithm to determine the maximum matching in bipartite graph.
        We need to convert the Bi partite graph to a network as following .
        Steps:
            1. All edges should go from variables to constraints
            2. Add a source node S
            3. Source node should have edge from it to all the variables
            4. Add a sink node
            5. Sink node should have edges from all the constraints to the sink node
            6. 
        '''
        prob = pulp.LpProblem("maximal_matching", pulp.LpMaximize)
       
        # Variables
        var = {}
        for x,y in  self.R.edges():
            var[x+y]=pulp.LpVariable(x+".__."+y , 0, 1, pulp.LpInteger)
    
        # Objective
        prob += pulp.lpSum([var[i] for i in var])

        # Constraints
        for n in self.R.nodes_iter():
            if len(self.R.neighbors(n)) > 1 :
                keys = []
                for x in self.R.neighbors(n):
                    if var.has_key(n+x): 
                        print n , " neighbor :", x
                        keys.append(n+x) 
                    print keys
                
                if(len(keys)):
                    prob += pulp.lpSum([var[i] for i in keys]) <= 1

        print prob
        # Finding multiple Solutions for maximal flow
        while True:

            prob.solve()
            print "Status : ", pulp.LpStatus[prob.status]
            if pulp.LpStatus[prob.status] == "Optimal":
                match = ([(string.split(v.name, sep='.__.' ))for v in prob.variables() if v.varValue == 1])
                
                print match

                # Adding this so that the same solution doesnt come up again
                prob += pulp.lpSum([v for v in prob.variables() if v.varValue == 1]) == 1
            else:
                break

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

        for v in self.known:
            for c in self.unmatched_constraints:
                paths =  nx.all_simple_paths(self.D_with_orientation, v, c )
                print(list(paths))

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


    def calculate_orientation(self):
        '''
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
        '''
        self.calculate_maximum_matching()
        #Finding unmatched constratints
        self.unmatched_constraints =  self.constraints - set(self.max_match_dict.keys())

        self.orientation_graph_edge_list = []

        for e in self.max_match_list:
            #check if the edge starts from a constraint node
            if (self.D.node[e[0]]['bipartite'] == 1):
                self.orientation_graph_edge_list.append(e)
                for s in self.D.successors(e[0]):
                    if (s != e[1]):
                        self.orientation_graph_edge_list.append((s,e[0]))
                        
        #for non matched constraints
        for constraint in self.unmatched_constraints:
            for variable in self.D.successors(constraint):
                self.orientation_graph_edge_list.append((variable,constraint))

        ## TODO
        ## creating Graph with orintation 
        ## including both known and unknown variables
        ## can be removed to just use  the D graph 
        ## need to modify the D graph with the orientation obtained
        self.D_with_orientation = nx.DiGraph(self.orientation_graph_edge_list)


    def visualize_bipartite(self, with_matching=False,with_orientation=False):
        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(self.constraints) ) # put nodes from self.variables at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(self.variables) ) # put nodes from self.constraints at x=2
    
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8,8))
        # nodes
        nx.draw_networkx_nodes(self.G,pos,ax=ax1,
                            nodelist=self.known,
                            node_color='m',
                            node_size=500,
                            alpha=0.8)
        nx.draw_networkx_nodes(self.G,pos,ax=ax1,
                            nodelist=self.unknown,
                            node_color='g',
                            node_size=500,
                            alpha=0.8)
        nx.draw_networkx_nodes(self.G,pos,ax=ax1,
                            nodelist=self.constraints,
                            node_color='y',
                            node_size=500,
                        alpha=0.8)
        # edges
        nx.draw_networkx_edges(self.G,pos,width=1.0,alpha=0.5)
        nx.draw_networkx_labels(self.G,pos)

        fig.suptitle(self.G.name, fontsize=14, fontweight='bold')
        #plt.savefig("./images/" + self.G.name + ".png")
        if(with_matching ):
            ax1.set_title("Max Matching")
            self.calculate_maximum_matching()
            nx.draw_networkx_edges(self.G,pos,ax=ax1,
                                edgelist=self.max_match_list,
                                width=8,alpha=0.3,edge_color='b')
            #plt.savefig("./images/" + self.G.name+"_MaxMatching" + ".png")
        if(with_orientation):
            ax1.set_title("With Orientation")
            self.calculate_maximum_matching()
            self.calculate_maximum_matching()
            nx.draw_networkx_edges(self.G,pos,ax=ax1,
                                edgelist=self.max_match_list,
                                width=5,alpha=0.3,edge_color='b')
            self.calculate_orientation()
            # nodes
            nx.draw_networkx_nodes(self.G,pos,ax=ax1,
                                nodelist=self.unmatched_constraints,
                                node_color='r',
                                node_size=500,
                                alpha=0.8)
            nx.draw_networkx_edges(self.D_with_orientation,pos,ax=ax1,
                       #edgelist=self.orientation_graph_edge_list, arrows=True,
                       arrows=True,
                       width=1,alpha=0.5)
            #plt.savefig("./images/" + self.G.name+"_WithOrientation" + ".png")
        '''
        red_patch = mpatches.Patch(color='red', label='Unmatched Constraint')
        yellow_patch = mpatches.Patch(color='yellow', label='Variables')
        green_patch = mpatches.Patch(color='green', label='Constraints')
        plt.legend(handles=[red_patch, yellow_patch, green_patch]) 
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        '''
        fig.suptitle(self.G.name, fontsize=14, fontweight='bold')
        plt.show()
