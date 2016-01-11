from sys import exit
from settings import settings

def validate(): 
    # Must specify valid partition lengths for each partition
    try:
        assert(int(settings['num_partitions']) == len(settings['partitions']))
    except:
        exit("Error in settings: num_partitions does not match partitions")

    # Type checks
    try:
        assert type(settings['length']) is int, "length must be int"
        assert type(settings['sample_locations']) is list, "sample_locations must be list of (float, float)" 
        assert type(settings['recombination_probability']) is float, "recombination_probability must be float"
        assert type(settings['num_replicates']) is int, "num_replicates must be int"
        assert type(settings['small_event']) is dict, "small_event must be dict"
        assert type(settings['mutation_rates']) is list, "mutation_rate must be list of float"
        assert len(settings['mutation_rates']) == len(settings['partitions']), "must specify mutation rate for each partition"
        assert type(settings['seq_length']) is str, "seq_length must be string"
        assert type(settings['num_partitions']) is str, "num_partitions must be str"
        assert type(settings['partitions']) is list, "partitions must be list of str"
        assert type(settings['num_cpus']) is int, "num_cpus must be int"

        # Check list internal types
        for rate in settings['mutation_rates']:
            assert(type(rate) is float, "mutation_rates must be double")

        assert type(settings['small_event']['rate'][0]) is float, "small_event rate must be float"
        assert type(settings['small_event']['radius'][0]) is float, "small_event radius must be double"
        assert type(settings['small_event']['radius'][1]) is float, "small_event radius must be double"

    except AssertionError, e:
        exit("Error in settings: {}".format(e.args[0]))
