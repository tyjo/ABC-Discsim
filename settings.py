settings = {
    ### ERCS Settings ###
    'length': 100, # torus side length
    'dimensions': 2,
    'sample_locations': [ (12.5, 12.5), (37.5, 37.5), (62.5, 12.5), (87.5, 37.5), 
                          (12.5, 62.5), (37.5, 87.5), (62.5, 62.5), (87.5, 87.5) ],
    'recombination_probability': 0.5,
    'num_replicates': 10,
    'num_parents': 2,

    # If true, parameters for events are 
    # set based on population density.
    'estimate_neighborhood_size': True,
    'neighborhood_size': (200, 200),
    'small_event': { 'rate': (1000.0, 1000.0), 'radius': (2.0, 2.0) },

    # Only used if estimate_population_size is False
    # Estimate extinction rate / radius
    'large_event': { 'rate': (10.0, 1000.0), 'radius': (15, 15), 'u': (25, 1000) }, # range of priors for event rate
    
    ### SeqGen Settings ###
    'mutation_rates': [ 1.1e-8, 1.1e-8, 1.1e-8, 1.1e-8, 1.1e-8, 1.1e-8, 1.1e-8, 1.1e-8, 1.1e-8, 1.1e-8], 
    'seq_length': '5000',
    'num_partitions': '10',
    'partitions': ['1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000', '1000'],

    ### Multiprocessing settings ###
    # If set to 0, all CPUs are used
    'num_cpus': 8,
    'debug': True,
}
