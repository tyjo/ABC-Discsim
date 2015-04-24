import subprocess as sub
from settings import settings

def run_seqgen(seed, seq_gen_seeds):
	"""
	Runs seqgen under one of five mutation models.
	"""
	def mod1(partition_length, scale, seed, seq_gen_seed, tree):
		# HKY - Posada
		sub.call("seqgen/seq-gen -mHKY -t2 -f0.35,0.15,0.25,0.25 -op -l{0} -s{1} -z{2} < {3}_{4} \
			> DNA_{5}_{4}".format(\
				partition_length, scale, str(seq_gen_seed), filename, str(tree), str(seed)),
			shell=True)

	def mod2(partition_length, scale, seed, seq_gen_seed, tree):
		# F84 model - Seq-Gen Manual
		sub.call("seqgen/seq-gen -mF84 -t2 -op -l{0} -s{1} -z{2} < {3}_{4} \
			> DNA_{5}_{4}".format(\
				partition_length, scale, str(seq_gen_seed), filename, str(tree), str(seed)),
			shell=True)

	def mod3(partition_length, scale, seed, seq_gen_seed, tree):
		# Jukes-Cantor model - Seq-Gen Manual
		sub.call("seqgen/seq-gen -mHKY -op -l{0} -s{1} -z{2} < {3}_{4} \
			> DNA_{5}_{4}".format(\
				partition_length, scale, str(seq_gen_seed), filename, str(tree), str(seed)),
			shell=True)

	def mod4(partition_length, scale, seed, seq_gen_seed, tree):
		# HKY + gamma - Posada
		sub.call("seqgen/seq-gen -mHKY -t2 -f0.35,0.15,0.25,0.25 -a0.5 -op -l{0} -s{1} -z{2} < {3}_{4} \
			> DNA_{5}_{4}".format(\
				partition_length, scale, str(seq_gen_seed), filename, str(tree), str(seed)),
			shell=True)

	def mod5(partition_length, scale, seed, seq_gen_seed, tree):
		# GRT + gamma - Posada
		sub.call("seqgen/seq-gen -mGTR -f0.35,0.15,0.25,0.25 -a0.5 -r2.0,4.0,1.8,1.4,6,1 \
			-op -l{0} -s{1} -z{2} < {3}_{4} > DNA_{5}_{4}".format(\
				partition_length, scale, str(seq_gen_seed), filename, str(tree), str(seed)),
			shell=True)

	filename = "tree_" + str(seed)
	partition_lengths = settings["partitions"][:]
	num_tree = int(settings["num_partitions"])
	scales = []
	for s in settings["evolution_rates"][:]:
		scales.append(str(float(s) * settings["mutation_rate"]))	
	
	# Cycles through five mutation models for each DNA sequence.
	for tree in range(1, num_tree + 1):
		i = tree - 1
		if tree % 5 == 1:
			mod1(partition_lengths[i], scales[i], seed, seq_gen_seeds[i], tree)

		elif tree % 5 == 2: 
			mod2(partition_lengths[i], scales[i], seed, seq_gen_seeds[i], tree)

		elif tree % 5 == 3:
			mod3(partition_lengths[i], scales[i], seed, seq_gen_seeds[i], tree)

		elif tree % 5 == 4:
			mod4(partition_lengths[i], scales[i], seed, seq_gen_seeds[i], tree)

		elif tree % 5 == 0:
			mod5(partition_lengths[i], scales[i], seed, seq_gen_seeds[i], tree)


	# Combine all sequence data by sample
	sequences = {}
	for j in range(1, num_tree + 1):
		with open("DNA_" + str(seed) + "_" + str(j)) as f:
			lines = f.readlines()
			for line in lines[1:]:
				line.strip('\n')
				split = line.split()
				if split[0] in sequences:
					sequences[split[0]].append(split[1])
				else:
					sequences[split[0]] = [split[1]]

	return sequences

	

