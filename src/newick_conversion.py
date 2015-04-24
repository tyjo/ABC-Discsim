# ERCS outputs its data in oriented forest format, we need to convert
# this to Newick for use with Seq-Gen.

def convert_tree(raw_pi, raw_tau):
	'''
	Takes pi and tau output from python ERCS module. Converts to standard
	Newick ouput. Branch lengths are determined by coalescence time.
	'''
	def fix_pi_tau(pi, tau):
		'''
		Turns nonbifurcating trees into bifurcating trees by adding
		0 branch length.
		'''
		coalescence_map = {}
		for index in range(len(pi)):
			coalescence_map[index] = {pi[index]: tau[index]}

		parent_children = construct_tree(pi)

		add = 0
		for parent, children in parent_children.iteritems():
			if len(children) > 2:
				if parent == len(pi) - 1:
					coalescence_map[children[2]] = {parent + 1: tau[children[2]]}
					coalescence_map[parent] = {parent + 1: tau[parent]}
					coalescence_map[len(pi)] = {0: tau[-1]}
				else:
					coalescence_map[children[0]] = {len(pi) - 1: tau[children[0]]}
					coalescence_map[children[1]] = {len(pi) - 1: tau[children[1]]}
					coalescence_map[len(pi) - 1] = {parent: tau[parent]}
					coalescence_map[len(pi)] = {0: tau[-1]}

					change_children = parent_children[len(pi) - 1]
					for child in change_children:
							coalescence_map[child] = {len(pi): tau[child]}
					break

		new_pi = []
		new_tau = []

		for index in sorted(coalescence_map.keys()):
			new_pi.append(int(coalescence_map[index].keys()[0]))
			new_tau.append(coalescence_map[index].values()[0])

		bifurcating = True
		for children in construct_tree(new_pi).values():
			if len(children) > 2:
				bifurcating = False

		if bifurcating:
			return new_pi, new_tau
		else:
			return fix_pi_tau(new_pi, new_tau)

	def construct_tree(pi):
		'''
		Constructs a dictionary. Each key is an integer that corresponds to
		a node in the tree, and each value is a list of integers that correspond
		to the children nodes. If a node has no children, an empty list is returned.
		'''
		tree = {}
		for n in range(1, len(pi)):
			tree[n] = []
		for n in range(1, len(pi)):
			if int(pi[n]) != 0:
				tree[int(pi[n])].append(n)
		return tree

	def child_is_empty(node):
		'''
		Checks if a node contains any children
		'''	
		return tree[node] == []

	def get_parent(node):
		'''
		Returns the parent node of a given node.
		'''
		for n in tree.keys():
			if node in tree[n]:
				return n

	def total_coalescence():
		'''
		Returns the total time it takes for all lineages to
		coalesce.
		'''	
		return max(tau)

	def to_string(node):
		'''
		Relabels the node from an integer to a letter.
		This is necessary to work with FigTree, as FigTree won't
		display node names if they are numeric.
		'''
		label = 'sample'
		return label + str(node)

	def get_coalescence(node):
		'''
		Takes a node and returns the length of the branch to the parent.
		'''
		#returns time of coalescent, only need to check when node has children
		parent = get_parent(node)
		if child_is_empty(node):
			return tau[parent]
		else:
			return tau[parent] - tau[node]

	def convert(node):
		'''
		Runs the actual conversion. This function searches recursively
		through the tree from the top node down.
		'''
		string = '('
		children = tree[node]
		
		
		for child in children:
			
			coal = str(round(get_coalescence(child), 2))
			
			if child_is_empty(child):
				string += to_string(child) + ':' + coal
			else:
				string += convert(child)
			
			if child != children[-1]:
				string += ','

		if node != len(tau) - 1:
			coal = str(round(get_coalescence(node), 2))
			string +='):' + coal
		else:
			string += ');'

		return string

	fixed = fix_pi_tau(raw_pi, raw_tau)
	pi = fixed[0]
	tau = fixed[1]
	tree = construct_tree(pi)
	return convert(len(tau) - 1)

if __name__ == "__main__":
	# Test values
	pi1 = [-1, 8L, 8L, 9L, 9L, 9L, 9L, 9L, 10L, 10L, 0L]
	tau1 = [-1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 3.0, 4.0]

	pi2 = [-1, 7L, 7L, 8L, 8L, 8L, 8L, 9L, 9L, 0]
	tau2 = [-1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0]

	pi3 = [-1, 6L, 6L, 6L, 7L, 7L, 8L, 8L, 0]
	tau3 = [-1, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 4.0]

	pi4 = [-1, 4, 4, 5, 5, 0]
	tau4 = [-1, 0.0, 0.0, 0.0, 30441.57, 46750.11]

	pi5 = [-1, 7L, 7L, 7L, 9L, 8L, 8L, 9L, 10L, 10L, 0]
	tau5 = [-1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 3.0, 3.5, 5.0]

	pi6 = [-1, 21L, 22L, 21L, 21L, 21L, 26L, 25L, 25L, 25L, 26L, 23L, 23L, 23L, 23L, 23L, 24L, 24L, 24L, 23L, 24L, 22L, 28L, 29L, 28L, 27L, 27L, 29L, 30L, 30L, 0L]
	tau6 =[-1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 32.7418704991378, 334.63338764576457, 629.9764585954227, 629.9764585954227, 826.4274709553723, 826.4274709553723, 1998.3064062203891, 2837.7657739811125, 16949.513865394227, 28047.895372157527]

	pi7 = [-1, 23L, 24L, 23L, 24L, 23L, 22L, 21L, 22L, 21L, 21L, 23L, 28L, 23L, 26L, 24L, 25L, 27L, 25L, 25L, 25L, 23L, 25L, 29L, 26L, 27L, 28L, 29L, 29L, 0L]
	tau7 = [-1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.10985644042186, 4.10985644042186, 8.221697332774426, 8.221697332774426, 10.536852580571875, 14.265107279556807, 35.958551353629076, 45.6233202663075, 45.871626594037416]

	pi8 = [-1, 3, 3, 6, 6, 6, 0]
	tau8 = [-1, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0]
	print 'Testing trees...'
	print 'Tree1: ',
	print convert_tree(pi1, tau1) == '((sample1:2.0,sample2:2.0):2.0,((sample5:3.0,sample6:3.0):0.0,(sample7:3.0,(sample3:3.0,sample4:3.0):0.0):0.0):1.0);'
	print 'Tree2: ',
	print convert_tree(pi2, tau2) == '((sample1:1.0,sample2:1.0):2.0,((sample3:2.0,sample4:2.0):0.0,(sample5:2.0,sample6:2.0):0.0):1.0);'
	print 'Tree3: ',
	print convert_tree(pi3, tau3) == '((sample3:1.0,(sample1:1.0,sample2:1.0):0.0):3.0,(sample4:2.0,sample5:2.0):2.0);'
	print 'Tree4: ',
	print convert_tree(pi4, tau4) == '(sample3:46750.11,(sample1:30441.57,sample2:30441.57):16308.54);'
	print 'Tree5: ',
	print convert_tree(pi5, tau5) == '((sample5:3.0,sample6:3.0):2.0,(sample4:3.5,(sample3:2.0,(sample1:2.0,sample2:2.0):0.0):1.5):1.5);'
	print 'Tree6: ',
	print convert_tree(pi6, tau6) == '(((sample2:334.63,((sample1:32.74,sample3:32.74):0.0,(sample4:32.74,sample5:32.74):0.0):301.89):2503.13,((sample16:629.98,sample17:629.98):0.0,(sample18:629.98,sample20:629.98):0.0):2207.79):25210.13,(((sample15:629.98,sample19:629.98):0.0,((sample11:629.98,sample12:629.98):0.0,(sample13:629.98,sample14:629.98):0.0):0.0):16319.54,((sample9:826.43,(sample7:826.43,sample8:826.43):0.0):1171.88,(sample6:826.43,sample10:826.43):1171.88):14951.21):11098.38);'
	print 'Tree7: ',
	print convert_tree(pi7, tau7) == '((sample12:45.62,(sample14:14.27,(sample15:8.22,(sample2:8.22,sample4:8.22):0.0):6.04):31.36):0.25,(((sample13:8.22,(sample10:4.11,(sample7:4.11,sample9:4.11):0.0):4.11):0.0,((sample1:8.22,sample3:8.22):0.0,(sample5:8.22,sample11:8.22):0.0):0.0):37.65,(sample17:35.96,((sample19:10.54,sample20:10.54):0.0,((sample6:4.11,sample8:4.11):6.43,(sample16:10.54,sample18:10.54):0.0):0.0):25.42):9.91):0.0);'
	print 'Tree8: ',
	print convert_tree(pi8, tau8) == '(sample5:2.0,((sample1:1.0,sample2:1.0):1.0,sample4:2.0):0.0);'