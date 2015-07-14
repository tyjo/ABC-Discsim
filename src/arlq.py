# Converts Seq-Gen output into the proper format for Arlequin.

from settings import settings

'''
def convert_to_arp(seed, sequence_dict):
	# Open Arlequin template file - copy data into new file
	with open("GeneSamples_TEMPLATE.arp") as arlq:
		with open("ARQ_abc_" + str(seed) + ".arp", "w") as f:
			partitions = settings["partitions"][:]
			for line in arlq:
				if "[[Samples]]" in line:
					f.write("	[[Samples]]\n")
					f.write("\n")

					for sample in sequence_dict:
						f.write("\t\tSampleName=\"" + sample + "\"\n")
						f.write("\t\tSampleSize=1\n")
						f.write("\t\tSampleData= {\n")
						f.write(sample[-1] + "\t1\t")
						f.write("\t".join(sequence_dict[sample]) + "\n")

				elif "SampleName=\"sample" in line or "SampleSize=5" in line or "SampleData= {" in line or len(line) > 75:
					pass
				else: 
					f.write(line)
'''
import re

def convert_to_arp(seed, sequence_dict):
	with open("ARQ_abc_" + str(seed) + ".arp", "w") as f:
		f.write("[Profile]\n")
		f.write("\tTitle=\"Discsim generated data\"\n")
		f.write("\tNbSamples=1\n") # need to double check this
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
			f.write(re.search("\d+", sample).group(0) + "\t1\t")
			f.write("\t".join(sequence_dict[sample]) + "\n")
		f.write("\n}")