from sys import exit
from settings import settings

def validate():
	# Recombination probabilities + 1 determines number of gene trees. With 1 gene tree per partition,
	# the number of partitions must equal number of recombination probabilities + 1.
	try:
		assert(len(settings['recombination_probabilities']) + 1 == len(settings['partitions']))
	except:
		exit("Error in settings: Recombination probabilities specifies {0} loci, but {1} partitions specified in SeqGen".format(\
				len(settings['recombination_probabilities']) + 1, len(settings['partitions'])))
	
	# Must specify valid partition lengths for each partition
	try:
		assert(int(settings['num_partitions']) == len(settings['partitions']))
	except:
		exit("Error in settings: num_partitions does not match partitions")

	try:
		assert(len(settings['evolution_rates']) == len(settings['partitions']))
	except:
		exit("Error in settings: must specify evolution rate for every partition")

	# Check sample locations in landscape
	try:
		landscape_size = settings['landscape_size']
		for sample in settings['sample_locations']:
			assert(0 <= sample[0] and sample[0] < landscape_size)
			assert(0 <= sample[1] and sample[1] < landscape_size)
	except:
		exit("Error in settings: sample_location defined out of bounds, 0 <= sample < landscape_size")

	# Type checks
	try:
		assert type(settings['landscape_size']) is int, "landscape_size must be int"
		assert type(settings['sample_locations']) is list, "sample_locations must be list of (int, int)" 
		assert type(settings['recombination_probabilities']) is list, "recombination_probabilities must be list of float"
		assert type(settings['num_replicates']) is int, "num_replicates must be int"
		assert type(settings['small_event']) is dict, "small_event must be dict"
		assert type(settings['large_event']) is dict, "large_event must be dict" 
		assert type(settings['mutation_rate']) is float, "mutation_rate must be float"
		assert type(settings['evolution_rates']) is list, "evolution_rate must be list"
		assert type(settings['seq_length']) is str, "seq_length must be string"
		assert type(settings['num_partitions']) is str, "num_partitions must be str"
		assert type(settings['partitions']) is list, "partitions must be list of str"
		assert type(settings['num_cpus']) is int, "num_cpus must be int"

		# Check list internal types
		for prob in settings['recombination_probabilities']:
			assert type(prob) is float, "recombination_probabilities must be float"

		for sample in settings['sample_locations']:
			assert type(sample) is tuple, "sample_locations must be list of tuples of ints: [(int, int)]"
			assert type(sample[0]) is int, "sample_locations must be integer values"
			assert type(sample[1]) is int, "sample_locations must be integar values"
			assert len(sample) is 2, "sample_locations must only contain two values (int, int)"

		for rate in settings['evolution_rates']:
			assert type(rate) is float, "evolution_rate must be list of float"

		assert type(settings['small_event']['rate'][0]) is float, "small_event rate must be float"
		assert type(settings['small_event']['rate'][1]) is float ,"small_event rate must be float"
		assert len(settings['small_event']['rate']) == 2, "small_event rate can only take 2 priors"
		assert settings['small_event']['rate'][0] <= settings['small_event']['rate'][1], "small_event prior lower bound must be less than upper bound"

		assert type(settings['small_event']['radius'][0]) is int, "small_event radius must be int"
		assert type(settings['small_event']['radius'][1]) is int,"small_event radius must be int"
		assert len(settings['small_event']['radius']) == 2, "small_event radius can only take 2 priors"
		assert type(settings['small_event']['u']) is float, "small_event u must be float"

		assert type(settings['large_event']['rate'][0]) is float, "large_event rate must be float"
		assert type(settings['large_event']['rate'][1]) is float ,"large_event rate must be float"
		assert len(settings['large_event']['rate']) == 2, "large_event rate can only take 2 priors"
		assert settings['large_event']['rate'][0] <= settings['large_event']['rate'][1], "large_event prior lower bound must be less than upper bound"

		assert type(settings['large_event']['radius'][0]) is int, "large_event radius must be int"
		assert type(settings['large_event']['radius'][1]) is int,"large_event radius must be int"
		assert len(settings['large_event']['radius']) == 2, "large_event radius can only take 2 priors"
		assert type(settings['large_event']['u']) is float, "large_event u must be float"

	except AssertionError, e:
		exit("Error in settings: {}".format(e.args[0]))
