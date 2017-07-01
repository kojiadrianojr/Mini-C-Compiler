class Node:
	def __init__(self,type,children=None,leaf=None):
		self.type = type
		if children:
			self.children = children
		else:
			self.children = []
		self.leaf = leaf
	def disp(self):
		print("Internal node",self.type,self.leaf)
		if self.children:
			for e in self.children:
				print("children-->",e[1].leaf)
		#print('\n')
