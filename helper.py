from threading import *

class Helper(Thread):
	"""
	This class is a thread of a node that will be register to the datastore of this node
	in order to obtain elements from it.
	"""
	def __init__(self, node, row, column, matrix):
		"""
		Constructor of class which initializes the variables that the run method needs to obtain the right element.
		"""
		Thread.__init__(self);
		self.node = node;
		self.row = row;
		self.column = column;
		self.matrix = matrix;
		self.element = -1;

	def run(self):
		"""
		This method is running when the thread is started and gets one element from the right datastore.
		"""
		self.node.data_store.register_thread(self.node);
		if self.matrix == "a":
			self.element = self.node.data_store.get_element_from_a(self.node, self.row, self.column);
		elif self.matrix == "b":
			self.element = self.node.data_store.get_element_from_b(self.node, self.row, self.column);
