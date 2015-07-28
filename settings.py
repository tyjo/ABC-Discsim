settings = {
    ### ERCS Settings ###
    'length': 290, # torus side length
    'sample_locations': [ 88.1935679318, 102.77478067, 109.283093403, 85.5087732054, 83.8330909796, 77.1396199893, 71.5663564539,
                          69.9554796181, 55.8741941738, 44.8572778828, 42.1632252436, 56.4667005962, 65.0487858078, 209.5,
                          196.724080268, 289.303208764, 194.307765014, 189.808419369, 188.540085309, 186.632955261, 182.587247346,
                          186.420023266, 143.009669914, 138.380713489, 134.492390093, 122.207139741, 108.690586981, 98.8123939702,
                          68.6871455577, 182.63353691, 156.146648248, 33.4144976007, 23.360404246, 18.5 ],
    'recombination_probability': 0.5,
    'num_replicates': 10000,
    'num_parents': 1,

    # If true, parameters for events are 
    # set based on population density.
    'estimate_neighborhood_size': True,
    'neighborhood_size': (4, 1000),
    'small_event': { 'rate': 1.0, 'radius': 2 },

    # Only used if estimate_population_size is False
    # Estimate extinction rate / radius
    'large_event': { 'rate': (10.0, 1000.0), 'radius': (15, 15), 'u': (25, 1000) }, # range of priors for event rate
    
    ### SeqGen Settings ###
    'mutation_rates': [ 1.25e-8, 1.25e-8, 3.475e-8, 3.475e-8, 3.475e-8 ], 
    'seq_length': '2823',
    'num_partitions': '5',
    'partitions': ['1181', '959', '280', '163', '240'],

    ### Multiprocessing settings ###
    # If set to 0, all CPUs are used
    'num_cpus': 8,
}
