# tephrange

> Python functions to calculate tephra terminal velocity and transport range

Tephrange is a Python implementation of code used to calculate the fall
velocity of tephra particles.
The original code was written in FORTRAN and was used to estimate
order-of-magnitude particle travel distances for the paper
[Big grains go far: understanding the discrepancy between tephrochronology and satellite infrared measurements of volcanic ash](https://amt.copernicus.org/articles/8/2069/2015/amt-8-2069-2015-metrics.html).


## Installation instructions

`tephrange` can be installed directly from GitHub (providing you have a local
installation of git) with the following:

```
pip install git+https://github.com/volcan01010/tephrange.git
```


## Example uses


## Bug reports


## Development

### Configuring a development environment

To modify the code, first clone the Tephrange repository into your local machine:
```bash
git clone https://github.com/volcan01010/tephrange
```

Then move to the root directory of the project (`tephrange`, which contains the `setup.py` file),
and run the following command to install Tephrange in development mode, preferably within a
clean virtual environment:

```bash
pip install -r requirements_full.txt
python -m pip install -e .
```

The `-e` flag makes the files in the current working directory available
throughout the virtual environment and, therefore, changes are reflected straight away.

The first `pip install` command installs all the dependencies to run tests,
debug and do analysis e.g. Jupyter notebook server.

Run tests (on Linux) with:

```bash
./bin/run_tests.sh
```

### Developers

Tephrange was created by Dr John A Stevenson at University of Edinburgh, now British Geological Survey ([volcan01010](https://github.com/volcan01010)).
The functions with the `atmos` and `fall_velocity` modules were based on FORTAN
routines written by Dr Frances Beckett at the UK Met Office.
The object-oriented approach to calculating particle trajectories was based on
code written by Dr Elizabeth Watson, then of University of Leeds.

### Licence

`tephrange` is distributed under the [MIT licence](LICENSE).
