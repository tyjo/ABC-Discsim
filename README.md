# _Inference of dispersal and colonization and dispersal under a spatially-continuous coalescent model_ (in progress)

Simulation code used for data generation in _Inference of dispersal and colonization and dispersal under a spatially-continuous coalescent model_. This is a work in progress.

## Dependencies
* Python v2.7
* ERCS v1.0.1: https://pypi.python.org/pypi/ercs
* Arlequin v3.5.1.3: http://cmpg.unibe.ch/software/arlequin35/
* Seq-Gen v1.3.3: http://tree.bio.ed.ac.uk/software/seqgen/

## Overview and Setup
The main simulation code is run from simulate.py. Parameter settings are specified in settings.py.

``python simulate.py``

 The script runs simulations as follows:

1. Generate gene trees from ERCS
2. Simulate the corresponding DNA sequences with Seq-Gen
3. Convert the DNA sequences into the appropriate format for Arlequin

The simulation code sets up files for analysis in Arlequin, however Arlequin is not called directly. Instead Arlequin is run as a standalone through their provided scripts. For detailed instruction see the Arlequin manual.

Simulation parameters are specified in settings.py. Settings to run each of the 4 models tested in the paper are provided. Rename any of the files to _settings.py_ to run the alternate models.

1. settings.py : the main model
2. settings-25loci.py: increased number of loci
3. settings-5000bp.py: increased number of base pairs 
4. settings-recomb: reduced recombination rate

The simulation code expects the compiled program Seq-Gen (named "seq-gen") in the seqgen folder. First download and compile the program from the link above. Rename the compiled program "seq-gen" and place in the folder named "seqgen."

Simulation parameters and random seeds used to run approximate Bayesian computation analysis are saved in the _parameters.txt_ file. The seed used to run the simulation correspond to the names of the files generated for Arlequin.