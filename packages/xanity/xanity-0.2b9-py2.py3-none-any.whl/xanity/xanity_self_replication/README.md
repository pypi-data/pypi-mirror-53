#  xanity is experiment sanity

Xanity is meant to allow easy and free creation of multiple experiments among which
there is shared python codebase and system environment.

Xanity helps manage the following:

 - experimetal environments ( via [ana/mini]conda )

    - ensures experiments are run in the proper environment
    - creates new environments
    - updates environments when new packages are needed
    
 - experiment and analysis source code

    - archives all source code at every run and keeps it with the data
    - maps associations between individual experiments and analyses

 - experiment parameters
 
    - builds parameter sweeps
    - runs experiments repeatedly with swept parameters
    - catalogs all sweep data
    
 - experiment data
    - organizes all experimental data
    - ensures everything produced during runtime is properly cataloged
    
 - logs
    - provides easy logging interface
    - generates a master log file
    - generates per-experiment log files
    
### Dependencies:
 - conda - (from Anaconda or, my preference, *__Miniconda__*)
    - [https://conda.io/miniconda.html]

# Usage:
__xanity commands generally assume they're being called from a $PWD inside a xanity
project directory tree.__

Some commands accept additional arguments to specify 
the xanity project path:

```
xanity init[ialize] [--with-examples] [new-dir]
  "    init               "             "
     
    Create a bare-bones xanity project directory tree in either the $PWD
    or a [new-dir].


xanity env setup

    Create or update the conda environment associated with the project.


xanity status
    
    Print the status of the current xanity project.


xanity run [experiment_names] [-a analyses[...]]
    
    Run all (or the specified) experiments and optionally, analyses.
    

xanity analyze [-a analyses] [run_data_path]
  "    analyse       "              "
  "    anal          "              "
  "    analysis      "              "

    Run all (or the specified) analyses on the most recent (or specified) data.
    

xanity session
  "     sess
  "     sesh
       
    Drops you into a new bash shell inside your project's environment.

xanity data
    suite of tools to manage data from previously run experiments
```

# Example:

00. install miniconda if you need it:
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh
    bash Miniconda2-latest-Linux-x86_64.sh
    ```

0. install xanity into your system's python(3) (or if you want, a conda env):

    ```bash
    pip[3] install xanity
    ```
    
1. initialize a xanity project and move inside with:

    ```bash
    xanity init --with-examples xanity_test_proj
    cd xanity_test_proj
    ```

    this will create a skeleton directory tree for your experiments and analyses
    which will be populated with some examples.

2. Open xanity_test_proj/experiments/experiment1.py and have a look.  This is a
    skeletal experiment.

3. Open xanity_test_proj/analyses/analysis1.py and have a look.  This is a
    skeletal analysis.

4. find the conda-environment.yaml file and tweak its contents to suit your requiremnts.

5. resolve these requirements (create/update a conda env) with: 

    ```bash
    xanity env setup
    ```

6. run everything with:
    
    ```bash
    xanity run
    ```

7. you will find all the experimental data organized under the data/runs directory tree.
   Source-code snapshots are tarred and kept with the data they produced. Logs are kept too.

8. you can run an analysis script on a completed run:

    `xanity analyze experiment1`

   this will look for the most recent (or specified) dir of run data, and run the analysis found
   at analyses/myfaveexp on that data.

9. relax. collect Nobel.

# Experiment file skeleton:
## (xanity-proj-root/experiments/*.py)

Each experiment module must have a main() function defined:
  - xanity will look for and invoke the main() function in each experiment.
  - Any parameters to the experiment should be arguments to the main() function.
    
The `xanity.experiment_parameters()` call registers the parameter sweeps
to use when running the experiment.
    
Include the `xanity.run()` function call.
    - The run() hook will run the experiment if it's invoked directly as 
    a script or module:

```python
# experiments/example_experiment.py

import xanity
import numpy as np

# flag this experiment for analysis
xanity.analyze_this()

# register parameter sweeps you'd like to do
xanity.experiment_parameters({
    'n_trials': [100,150,200],
    'train_frac': [0.9, 0.5, 0.1],
    'scale': [1,2,3,]
})

# parameters the experiment will accept
def main(n_trials=200, scale =5, main_frac=0.8):
    
    fakevar = scale * np.random.rand(n_trials)**2
    xanity.log("here is a print from experiment 1")
    xanity.save_variable(fakevar)

if __name__=='__main__':
    xanity.run()

```
    
# Analysis file skeleton:
## (xanity-proj-root/analyses/*.py)

Each analysis module must have a main() function defined.
  - xanity will look for and invoke the main() function in each analysis.
  - The only parameter to the analysis is the path to the root of a run (or set of runs).
    
The call to xanity.associated_experiments() registers the names of experiments
 to associate with this analysis.

Include the `xanity.run()` function call.
    - The run() hook will run the analysis if it's invoked directly as a script or module

```python
# analyses/example_analysis.py

import xanity
import matplotlib.pyplot as plt

# define which experiments to associate this analysis with
xanity.associated_experiments([
        'experiment1',
        #'experiment2',
        #'experiment3',
        ])

# the analysis takes a single argument... path of data (xanity will provide)

def main(data_dir):
    
    data, paths = xanity.load_variable('fakevar')
    
    plt.figure()
    for d in data:
        d.sort()
        plt.plot(d)
        
    plt.show()

if __name__=='__main__':
    xanity.run()
    
```