# Converts Seq-Gen output into the proper format for Arlequin.

from settings import settings

def convert_to_arp(seed, sequence_dict, scales):
	# Open Arlequin template file - copy data into new file
	with open("GeneSamples_TEMPLATE.arp") as arlq:
		with open("ARQ_abc_" + str(seed) + ".arp", "w") as f:
			nonbifurcation = False
			sample_count = 1
			num_loci = settings["num_partitions"][:]
			partitions = settings['partitions'][:]
			for line in arlq:
				if "#Number of chromosome        : " in line:
						f.write("#Number of chromosome        : " + num_loci)

				elif "#Chromosome no 1" in line:
					for i in range(1, int(num_loci) + 1):
						f.write("#Chromosome no " + str(i) + "\n")
						f.write("#---------------\n")
						f.write("#Num Linkage Blocks: 1\n")
						f.write("\n")
						f.write("#Blocks n 1\n")
						f.write("#DNA\n")
						f.write("#Num linked loci      : " + str(int(partitions.pop(0))) + "\n")
						f.write("#Recombination rate per generation      : " + \
							str(settings['recombination_probabilities'][0]) + "\n")
						f.write("#Mutation rate per generation      : " + \
							str(float(scales.pop(0))) + "\n")
						f.write("\n")

				elif "#Chromosome no" in line or "#---------------" in line or "#Num Linkage Blocks:" in line \
				  or "#Blocks n" in line or "#DNA" in line or "#Num linked loci " in line or \
				  "#Recombination rate per generation" in line or "#Mutation rate per generation" in line:
				  pass


				elif "SampleName=\"sample" in line:
					f.write("\t\tSampleName=\"sample" + str(sample_count) + "\"\n")
					f.write("\t\tSampleSize=" + num_loci + "\n")
					f.write("\t\tSampleData= {\n")
					start_from = (sample_count - 1) * 5
					end = ((sample_count - 1) * 5) + 5
					for i in range(start_from, end):
						f.write(str(sample_count) + "_" + str(i+1) + " 1\t")
						sequence = sequence_dict.get("sample" + str(i+1), -1)
						if sequence == -1:
							nonbifurcation = True
						else:
							for n in sequence:
								f.write(str(n) + "\t")
						f.write("\n")
					sample_count += 1
				elif "SampleSize=5" in line or "SampleData= {" in line or len(line) > 75:
					pass
				else: f.write(line)
	return nonbifurcation