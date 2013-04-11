"""
    This module represents a cluster's computational node.

    Computer Systems Architecture course
    Assignment 1 - Cluster Activity Simulation
    march 2013
"""
from helper import Helper
import resource

class Node:
    """
        Class that represents a cluster node with computation and storage functionalities.
    """

    def __init__(self, node_ID, block_size, matrix_size, data_store):
        """
            Constructor.

            @param node_ID: a pair of IDs uniquely identifying the node; 
            IDs are integers between 0 and matrix_size/block_size
            @param block_size: the size of the matrix blocks stored in this node's datastore
            @param matrix_size: the size of the matrix
            @param data_store: reference to the node's local data store
        """

        self.node_ID 	 = node_ID;
	self.block_size  = block_size;
	self.matrix_size = matrix_size;
	self.data_store  = data_store;

	self.node_ID_i = node_ID[0];
	self.node_ID_j = node_ID[1];

    def set_nodes(self, nodes):
        """
            Informs the current node of the other nodes in the cluster. 
            Guaranteed to be called before the first call to compute_matrix_block.

            @param nodes: a list containing all the nodes in the cluster
        """
        self.nodes = nodes;

    def multiply(self, a, b, num_rows, num_columns):
	"""
	This method receive two matrixes and multiply its.
	"""
	c = [[0 for i in range(num_columns)] for j in range(num_rows)];
        for i in range(num_rows):
    		for j in range(num_columns):
    			suma = 0;
    			for k in range(self.matrix_size):
    				suma += a[i][k] * b[k][j];
    			c[i][j] = suma;
	return c;

    def compute_matrix_block(self, start_row, start_column, num_rows, num_columns):
        """
            Computes a given block of the result matrix.
            The method invoked by FEP nodes.

            @param start_row: the index of the first row in the block
            @param start_column: the index of the first column in the block
            @param num_rows: number of rows in the block
            @param num_columns: number of columns in the block

            @return: the block of the result matrix encoded as a row-order list of lists of integers
        """
	"""
	This method is searching for the elements that this node needs in order to compute his block.
	Firstly finds the node from where a element should be taken, starts a thread which will obtain the element, and then
	puts that element in a matrix.
	Those are made twice, for each matrix.
	After calculating the two matrixes, the method 'multiply' gives the result that is returning the result.
	"""
	A = [[0 for i in range(self.matrix_size)] for j in range(num_rows)];
	B = [[0 for j in range(num_columns)] for j in range(self.matrix_size)];
        for i in range(num_rows):
		for j in range(self.matrix_size):
			row = start_row + i;
			id_row = row / self.block_size;
			id_column = j / self.block_size;

			node = self.nodes[(self.matrix_size / self.block_size) * id_row + id_column];	

			i_a = node.node_ID[0];
			j_a = node.node_ID[1];
			size = node.block_size;
	
			helper = Helper(node, row - i_a * size, j - j_a * size, "a");
			helper.start();
			helper.join();
			A[i][j] = helper.element;
	
	for i in range(self.matrix_size):
		for j in range(num_columns):
			column = start_column + j;
			id_row = i / self.block_size;
			id_column = column / self.block_size;

			node = self.nodes[(self.matrix_size / self.block_size) * id_row + id_column];	

			i_b = node.node_ID[0];
			j_b = node.node_ID[1];
			size = node.block_size;
	
			helper = Helper(node, i - i_b * size, column - j_b * size, "b");
			helper.start();
			helper.join();
			B[i][j] = helper.element;

	return self.multiply(A, B, num_rows, num_columns);

    def shutdown(self):
        """
            Instructs the node to shutdown (terminate all threads).
        """
        pass


