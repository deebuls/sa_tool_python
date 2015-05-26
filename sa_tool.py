import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
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

        self.G = graph
        self.D = graph.to_directed()
        self.variables, self.constraints = nx.bipartite.sets(self.G)
        Y = list(self.variables)
        if (self.G.node[Y[0]]['bipartite'] == 1):
            X = self.constraints
            self.constraints = self.variables
            self.variables = X

    def calculate_maximum_matching(self):
        try:
            self.max_match_dict = nx.algorithms.bipartite.maximum_matching(self.G)
            self.max_match_list = list(self.max_match_dict.items())
        except:
            print "Networkx Development version required for calculationg maximum matching"
            print "Please read Installation instructions "
            exit()

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

        self.orientation_graph = []

        for e in self.max_match_list:
            #check if the edge starts from a constraint node
            if (self.D.node[e[0]]['bipartite'] == 1):
                self.orientation_graph.append(e)
                for s in self.D.successors(e[0]):
                    if (s != e[1]):
                        self.orientation_graph.append((s,e[0]))
                        
        #for non matched constraints
        for constraint in self.unmatched_constraints:
            for variable in self.D.successors(constraint):
                self.orientation_graph.append((variable,constraint))

    def visualize_bipartite(self, with_matching=False,with_orientation=False):
        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(self.constraints) ) # put nodes from self.variables at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(self.variables) ) # put nodes from self.constraints at x=2
    
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8,8))
        # nodes
        nx.draw_networkx_nodes(self.G,pos,ax=ax1,
                            nodelist=self.variables,
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
            nx.draw_networkx_edges(self.D,pos,ax=ax1,
                       edgelist=self.orientation_graph, arrows=True,
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
