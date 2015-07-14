# This defines samples within the landscape in ERCS. Each tuple defines
# a coordinate where (0, 0) is the bottom left corner.
sampleA = [(25, 75), (24, 74), (24, 76), (26, 74), (26, 76)]
sampleB = [(75, 75), (74, 74), (74, 76), (76, 74), (76, 74)]
#sampleC = [(250, 250), (240, 240), (240, 260), (260, 240), (260, 260)]
#sampleD = [(750, 250), (740, 240), (740, 260), (760, 240), (760, 260)]
sample = sampleA + sampleB# + sampleC + sampleD

settings = {
	### ERCS Settings ###
	'length': 100, # torus side length
	# Need to update GeneSamples_TEMPLATE.arp if you change this.
	'sample_locations': sample,
	'recombination_probability': 0.5,
	'num_replicates': 1,

	# If true, parameters for events are 
	# set based on population density.
	'estimate_population_size': True,
	'population_size': (10000.0, 20000.0), # range of priors for population size
	'small_event': { 'rate': 1.0, 'radius': 2 },

	# Only used if estimate_population_size is False
	# Estimate extinction rate / radius
	'large_event': { 'rate': (10.0, 10000.0), 'radius': (5, 25) }, # range of priors for event rate
	
	### SeqGen Settings ###
	'mutation_rate': 1.1e-8, # Base mutation rate
	'seq_length': '10000',
	'num_partitions': '10',
	'partitions': ['1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000'], #'1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000'],

	### Multiprocessing settings ###
	# If set to 0, all CPUs are used
	'num_cpus': 1,
}
