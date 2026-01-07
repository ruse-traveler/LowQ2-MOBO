# LowQ2-MOBO [Under construction]

An application of the AID2E framework to the ePIC Low-Q2 tagger. 

## Optimization strategy

Optimization will proceed in stages, gradually building up the number of
parameters and objectives. These tages are listed below.

### Steps:

- [ ] Set up initial objective script, configuration files with 2
      parameters: tagger 1 width and height
- [ ] Run optimization with these 2 parameters
- [ ] Expand parameters to include tagger 2 width and height, positions
      of the taggers, and relative positions between tracking disks
- [ ] Add (x, Q2) coverage and cost as objectives and rerun
- [ ] Expand parameters to include tilt of tracking disks, and rerun
      optimization

## Dependencies

- Python 3.11.5
- Conda or Mamba (eg. via [Miniforge](https://github.com/conda-forge/miniforge)) 
- [Ax](https://ax.dev)
- [EIC Software](https://eic.github.io)
- [AID2E Scheduler](https://github.com/aid2e/scheduler_epic)

## Code organization

This repository is structured like so:

  | File/Directory | Description |
  |----------------|-------------|
  | `lowq2-mobo.yml` | conda/mamba environment file |
  | `create-environment` | script to create lowq2-mobo conda/mamba environment |
  | `remove-environment` | script to remove lowq2-mobo conda/mamba environment |
  | `run-lowq2-mobo.py` | wrapper script and point-of-entry to the problem |
  | `launch-mobo` | script to launch a slurm pilot job |
  | `configurations` | collects various configuration files that define the problem |
  | `objectives` | collects analysis scripts to calculate objectives for optimize for |
  | `steering` | collects steering/macro files for running simulations |
  | `interfaces` | collects code to interface the framework with objective scripts or other external code |
  | `examples` | collects of example config files, scripts, etc. for illustrating some of the extended functionality |
  | `scripts` | collects various scripts useful for running, testing, etc. |
  | `tests` | collects test scripts for unit tests |
  | `EICMOBOTestTools` | a python package which consolidates various tools for interfacing with the EIC software stack |
  | `AID2ETestTools` | a python package which consolidates various tools for interfacing with Ax |

There are four configuration files which define the parameters of the problem.

  | File | Description |
  |------|-------------|
  | `run.config` | defines paths to EIC software, components, executables to be used, etc. |
  | `problem.config` | defines metadata and parameters for optimization algorithms |
  | `parameters.config` | defines design parameters to optimize with |
  | `objectives.config` | defines objectives to optimize for |

## Installation

Before beginning, please make sure conda and/or mamba is installed. Once
ready, the environment for the problem can be set up via:

```bash
./create-environment
```

And activated via `conda`
```bash
conda activate lowq2-mobo
```

At any point, this environment can be deleted with
```bash
./remove-environment
```

Then, install the [AID2E scheduler](https://github.com/aid2e/scheduler_epic)
following the instructions in its repository. Remember to configure the
scheduler appropriately if you're going to run with SLURM, PanDA, etc.

Install the local utilities/objectives by running
the command below in this directory:
```bash
pip install -e .
```

Lastly, you'll need to make sure the `eic-shell` is available on your
machine.  You can find instructions to do so [here](https://eic.github.io/tutorial-setting-up-environment/).

## Running the framework

Before beginning, create a local installation of [the ePIC geometry
description](https://github.com/eic/epic) and compile it:
```bash
cd <where-the-geo-goes>
git clone git@github.com:eic/epic.git
cd epic
cmake -B build -S . -DCMAKE_INSTALL_PREFIX=install
cmake --build build
cmake --install build
```

Then, modify `configurations/run.config` so that the paths point to your
installations and relevent scripts, eg.
```json
{
    "_comment"   : "Configures runtime options, and paths to EIC software components",
    "out_path"   : "<where-the-output-goes>",
    "run_path"   : "<where-the-running-happens>",
    "log_path"   : "<where-the-logs-go>",
    "eic_shell"  : "<path-to-your-script>/eic-shell",
    "epic_setup" : "<where-the-geo-goes>/epic/install/bin/thisepic.sh",
    "det_path"   : "<where-the-geo-goes>/epic/install/share/epic",
    "det_config" : "epic_ip6_extended",
    "sim_exec"   : "npsim",
    "sim_input"  : {
        "single_electron" : {
            "location" : "<where-the-mobo-goes>/LowQ2-MOBO/steering/electron",
            "type"     : "gun"
        }
    },
    "rec_exec"    : "eicrecon",
    "rec_collect" : [
        "MCParticles",
        "GeneratedParticles",
        "BackwardBeamlineHits",
        "TaggerTrackerM1LocalTracks",
        "TaggerTrackerM2LocalTracks",
        "TaggerTrackerReconstructedParticles"
    ],
    "scheduler_opts" : {
        "n_jobs"        : -1,
        "partition"     : "<your-partition>",
        "time_limit"    : "03:00:00",
        "memory"        : "8G",
        "cpus_per_task" : 4,
        "account"       : "<your-account>",
        "mail-user"     : "<your-email-address>",
        "mail-type"     : "END,FAIL"
    }
}

```

Where the angle brackets should be replaced with the appropriate
absolute paths. The values `det_path` and `det_config` should be
what `echo $DETECTOR_PATH` and `echo $DETECTOR_CONFIG` return after
sourcing your installation of the geometry.

And finally, modify `configurations/problem.config` and
`configurations/objectives.config` to make sure the
Ax output is placed in the appropriate directory and the code is
picking up the correct objective scripts, eg.
```json
{
    "_comment"         : "Configures problem for Ax",
    "name"             : "Low-Q2 Optimization",
    "problem_name"     : "lowq2_mobo",
    "OUTPUT_DIR"       : "<where-the-output-goes>/out",
    "n_sobol"          : 2,
    "min_sobol"        : 2,
    "max_parallel_gen" : 2,
    "n_max_trials"     : 5
}
```

```json
{
    "_comment"   : "Configure objectives to optimize for",
    "objectives" : {
        "TaggerOneResolution" : {
            "input" : "single_electron",
            "path"  : "<where-the-mobo-goes>/LowQ2-MOBO/objectives",
            "exec"  : "LowQ2LocalResolution.py",
            "rule"  : "python <EXEC> -i <RECO> -o <OUTPUT> -t 1",
            "stage" : "ana",
            "goal"  : "minimize"
        }
    }
}
```

Once appropriately configured, the optimizationc can be run locally
with:
```bash
python run-lowq2-mobo.py
```

It can also be run via Slurm using the script `launch-mobo`, which
dispatches a pilot job.  Update the slurm options accordingly, and
launch the job with:
```bash
sbatch launch-mobo
```

Various analyses can be run on the optimization output with the
script `run-analyses.py`.  After updating the appropariate paths/options
in the script, do:
```bash
python run-analyses.py
```
