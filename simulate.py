import discsim
import ercs
import math
import multiprocessing
import random
import re
import subprocess as sub
import src.newick_conversion as newick
import time
from settings import settings
from src.validate_settings import validate


class Simulator(discsim.Simulator):
    def setup(self, event_classes):
        """
        Set simulation parameters
        """
        self.sample = [None] + settings["sample_locations"]
        self.event_classes = event_classes
        self.recombination_probability = settings["recombination_probability"]
        self.num_loci = int(settings["num_partitions"])
        self.num_parents = settings["num_parents"]

    def run_simulation(self, seed, seq_gen_seeds):
        """
        Runs a single simulation. Converts simulation output to
        newick format. Runs Seq-Gen with newick trees to generate
        DNA sequence data. Returns dictionary of DNA sequences for
        each sample.
        """
        self.random_seed = seed
        self.run()
        result = self.get_history()
        self.reset()

        # Save file in Newick Tree Format
        trees = self._make_trees(result)
        
        filename = "tree_" + str(seed)
        num_tree = 1
        for tree in trees:
            with open(filename + "_" + str(num_tree), "w") as f:
                num_tree += 1
                f.write(str(tree) + "\n")
        
        # Call SeqGen
        seqgen_sequences = self._run_seqgen(seed, seq_gen_seeds)

        with open("DNA_" + str(seed), "w") as f:
            for seq in seqgen_sequences:
                sequence = "\t".join(seqgen_sequences[seq])
                f.write("{0}\t{1}\n".format(seq, sequence))

        # File cleanup
        for i in range(1, num_tree):
            sub.call(["rm", filename + "_" + str(i)])
            sub.call(["rm", "DNA_" + str(seed) + "_" + str(i)])
        sub.call(["mv", "DNA_" + str(seed), "output_sequences/"])

        return seqgen_sequences

    def _make_trees(self, oriented_trees):
        """
        Takes pi and tau from the replicates generated by run_replicates
        Converts them to Newick Tree Format.
        Returns list of trees.
        """
        pi = oriented_trees[0]
        tau = oriented_trees[1]
        trees = []

        for i, j in zip(pi, tau):
            # convert simulation time to generation time
            j = self._rescale_coalescent_times(j)

            # sometimes an extra 0L and 0.0 are added on to
            # pi and tau respectively which breaks the newick script.
            # the tree is otherwise correct
            while(j[-1] == 0.0):
                i.pop(-1)
                j.pop(-1)

            trees.append(newick.convert_tree(i, j))

        return trees

    def _run_seqgen(self, seed, seq_gen_seeds):
        """
        Generates DNA sequences using HKY mutation model from newick trees.
        Returns a dictionary from sample to list of sequences per loci.
        """
        filename = "tree_" + str(seed)
        partition_lengths = settings["partitions"][:]
        num_tree = int(settings["num_partitions"])

        for tree in range(1, num_tree + 1):
            i = tree - 1
            sub.call("./seqgen/seq-gen -mHKY -t2 -f0.35,0.15,0.25,0.25 -op -l{0} -s{1} -z{2} < {3}_{4} > DNA_{5}_{4}" \
                .format(settings["partitions"][i], settings["mutation_rates"][i],
                    str(seq_gen_seeds[i]), filename, str(tree), str(seed)),
                shell=True)

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

    def _rescale_coalescent_times(self, tau):
        """
        Rescales coalescent times from simulation time
        to generation time.
        """
        event = self.event_classes[0] # reproduction events
        L_d = float(settings["length"] ** settings["dimensions"])
        A = math.pi * (event.r**2) if settings["dimensions"] == 2 else 2 * event.r
        scaled = map(lambda x: ( x * event.rate * event.u * A ) / L_d, tau )
        return scaled


def generate_event_parameters(num_replicates):
    """
    Make parameter sets for simulations, write to output file.
    """
    def neighborhood_parameter_set():
        seed = random.randint(1, 2**31 - 1)
        seq_gen_seeds = [random.randint(1, 2**31 - 1) for i in range(int(settings["num_partitions"]))]
        rate = random.uniform(settings["small_event"]["rate"][0], settings["small_event"]["rate"][1])
        radius = random.uniform(settings["small_event"]["radius"][0], settings["small_event"]["radius"][1])
        n_size = random.uniform(settings["neighborhood_size"][0], settings["neighborhood_size"][1])
        u0 = settings["num_parents"] / float(n_size)
        event_classes = [  ercs.DiscEventClass(rate = rate, r = radius, u = u0) ]
        return (seed, seq_gen_seeds, event_classes, n_size)

    def posterior_parameter_set(f_lines, length):
        seed = random.randint(1, 2**31 - 1)
        seq_gen_seeds = [random.randint(1, 2**31 - 1) for i in xrange(int(settings["num_partitions"]))]
        rate = 1.0
        line = f_lines[random.randint(1, length)].strip("\n").split(",")
        radius = float(line[0])
        u = settings["num_parents"] / float(line[1])
        event_classes = [ ercs.DiscEventClass(rate = rate, r = radius, u = u)]
        return (seed, seq_gen_seeds, event_classes, line[1])
    
    random.seed()
    filename = "parameters_{}_{}.txt".format(time.strftime("%x"), time.strftime("%X"))
    filename = filename.replace("/","_").replace(":","")

    if(settings["posterior_predictive_checks"]):

        with open(settings["posterior_parameter_file"]) as f:
            lines = f.readlines()
            length = len(lines)
            parameters = [ posterior_parameter_set(lines, length) for i in xrange(num_replicates) ]
        
        with open(filename, "w") as f:
            seed_parameters = {}
            f.write("seed\trate\tradius\tu\tn_size\n")
            for seed, seq_gen_seeds, event_classes, pop_size in parameters:
                event = event_classes[0]
                seed_parameters[str(seed)] = (event.rate, event.r, event.u, pop_size)
            # Need to sort by string value to have same ordering as Arlequin
            for seed in sorted(seed_parameters):
                f.write("{}\t{}\t{}\t{}\t{}\n".format(seed, seed_parameters[seed][0], seed_parameters[seed][1],
                                                            seed_parameters[seed][2], seed_parameters[seed][3]))

    else:
        parameters = [ neighborhood_parameter_set() for i in xrange(num_replicates) ]

        with open(filename, "w") as f:
            seed_parameters = {}
            f.write("seed\trate\tradius\tu\tn_size\n")
            for seed, seq_gen_seeds, event_classes, pop_size in parameters:
                event = event_classes[0]
                seed_parameters[str(seed)] = (event.rate, event.r, event.u, pop_size)
            # Need to sort by string value to have same ordering as Arlequin
            for seed in sorted(seed_parameters):
                f.write("{}\t{}\t{}\t{}\t{}\n".format(seed, seed_parameters[seed][0], seed_parameters[seed][1],
                                                            seed_parameters[seed][2], seed_parameters[seed][3]))

    return parameters


def convert_to_arp(seed, sequence_dict):
    """
    Generate an Arlequin file from DNA sequences.
    """
    with open("ARQ_abc_" + str(seed) + ".arp", "w") as f:
        f.write("[Profile]\n")
        f.write("\tTitle=\"Discsim generated data\"\n")
        f.write("\tNbSamples=1\n")
        f.write("\tGenotypicData=0\n")
        f.write("\tGameticPhase=1\n")
        f.write("\tRecessiveData=0\n")
        f.write("\tDataType=DNA\n")
        f.write("\tLocusSeparator=TAB\n")
        f.write("\tMissingData='?'\n")
        f.write("\n")

        f.write("[Data]\n")
        f.write("\t[[Samples]]\n")
        f.write("\n") 

        f.write("\t\tSampleName=\"Population1\"\n")
        f.write("\t\tSampleSize=" + str(len(settings["sample_locations"])) + "\n")
        f.write("\t\tSampleData= {\n")
        
        for sample in sequence_dict:
            f.write(re.search("\d+", sample).group(0) + "_1\t1\t")
            f.write("\t".join(sequence_dict[sample]) + "\n")
        
        f.write("\n}\n")

    sub.call("mv " + "ARQ_abc_" + str(seed) + ".arp ./arlsumstat_files/ &> /dev/null &", shell=True)


def subprocess_worker(t):
    """
    Runs a single simulation.
    """
    # pop_size is unused here
    seed, seq_gen_seeds, event_classes, pop_size = t
    sim = Simulator(settings["length"])
    sim.setup(event_classes)

    seqgen_sequences = sim.run_simulation(seed, seq_gen_seeds)
    convert_to_arp(seed, seqgen_sequences)


def run_simulations():
    """
    Sets up multiprocessing parameters. Maps arguments
    to subprocess workers.
    """
    # Multiprocessing parameters
    if settings["num_cpus"] == 0:
        processes = multiprocessing.cpu_count()
    else:
        processes = settings["num_cpus"]

    workers = multiprocessing.Pool(processes=processes, maxtasksperchild=1000)
    args = generate_event_parameters(settings["num_replicates"])
    
    if not settings["debug"]:
        replicates = workers.map(subprocess_worker, args)
    else:
        for arg in args:
            subprocess_worker(arg)



if __name__ == "__main__":
    print "Validating settings file..."
    validate()

    print "Starting simulations..."
    start_time = time.strftime("%x") + " " + time.strftime("%X")
    run_simulations()

    print "Done!"
    print "Start Time: " + start_time
    print "Stop Time: " + time.strftime("%x") + " " + time.strftime("%X")



