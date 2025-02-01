"""
This module contains the Graph class which represents a directed graph with weighted edges.
"""

class Graph:
    """
    A class representing a directed graph with weighted edges.

    Attributes
    ----------
    edges : dict
        Maps a node to a list of its connected neighbors.
    weights : dict
        Maps a tuple (from_node, to_node) to the weight of that edge.
    """

    def __init__(self):
        """
        Initializes the graph with empty edges and weights.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.edges = {}
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        """
        Adds a directed edge between 'from_node' and 'to_node' with a given weight.

        Parameters
        ----------
            from_node : Any
                The starting node of the edge.
            to_node : Any
                The ending node of the edge.
            weight : float
                The weight or cost of traveling from 'from_node' to 'to_node'.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

    def __str__(self):
        """
        Returns a string representation of the graph's edges.

        Returns
        -------
            str
                The string form of the edges dictionary.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return str(self.edges)