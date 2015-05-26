SaTool-python:
=======
# Structural Analysis Tool 

This paper introduces SaTool-python, an open-source implementation of the
tool, for doing structural analysis.
”SATOOL - A Software Tool for structural analysis of complex automa-
tion systems ”[1] , introduces a tool for structural analysis, the use of the
Matlab -based 3 implementation is presented and special features are intro-
duced, which were motivated by industrial users.

# Code Example
### Creating the Bipartite Graph from the incidence matrix
```python

    B = nx.Graph(name="Example 5.17")
    B.add_nodes_from(['x1', 'x2', 'x3', 'x4', 'x5'], bipartite=0, color='r') # Add the node attribute "bipartite"
    B.add_nodes_from(['c1','c2','c3', 'c4', 'c5', 'c6'], bipartite=1, color='b')
    B.add_edges_from([('x1','c1'),('x1','c2'),('x1','c4') ])
    B.add_edges_from([('x2','c2'),('x2','c5')])
    B.add_edges_from([('x3','c2'),('x3','c3')])
    B.add_edges_from([('x4','c3'),('x4','c4'),('x4','c6') ])
    B.add_edges_from([('x5','c5'),('x5','c6')])
    
```

### Calling the sa tool for analyis

    
```python
    sa1 = sa_tool.SATool(B)
    
```
### Visualizing the Bipartite Graph 
```python
    sa1.visualize_bipartite()
    
```
### Calculating the Maximum Matching
```python
    sa1.calculate_maximum_matching()
    
```
### Visualizing the Matching 
```python
    sa1.visualize_bipartite(with_matching=True)
    
```
### Calculating the Orientation
```python
    sa1.calculate_orientation()
    
```
### Visualizing the Orientation
```python
    sa1.visualize_bipartite(with_orientation=True)
    
```

[1] Denmark, K. (2006). Satool-a software tool for structural analysis of complex
auomation systems.

