# tephrange

> Python functions to calculate tephra terminal velocity and transport range

Tephrange is a collection of Python functions that can be used to calculate fall velocity of volcanic ash particles.
It is based on FORTRAN code that was used to estimate order-of-magnitude particle travel distances for the paper [Big grains go far: understanding the discrepancy between tephrochronology and satellite infrared measurements of volcanic ash](https://amt.copernicus.org/articles/8/2069/2015/amt-8-2069-2015-metrics.html).


## Installation instructions

`tephrange` can be installed directly from GitHub (providing you have a local
installation of git) with the following:

```
pip install git+https://github.com/volcan01010/tephrange.git
```


## Examples


### Fall velocity

Calculate for velocity for a 100 micron andesite particle at sea level, using either Stokes or Ganser equation.

```python
>>> from tephrange.fall_velocity import stokes, ganser
>>> stokes(100 * 1e-6)
0.6990815224284429
>>> ganser(100 * 1e-6)
0.40740774852655665
```

For Ganser you can also set the sphericity:

```python
>>> ganser(100 * 1e-6, sphericity=1)
0.5515837041219246
```

Both functions allow you to pass the density, atmospheric density and atmospheric viscosity.


### Atmospheric properties

The `atmos` module contains functions to return temperature, pressure,
density and viscosity based on the ICAO Standard Atmosphere.

```python
>>> from tephrange.atmos import get_atmos_temp_press
>>> get_atmos_temp_press(0)
(288.15, 101325.0)
>>> get_atmos_temp_press(8848)
(230.63799999999998, 31443.60143420036)
```

### Density

The `density` module contains a function to calculate the density of an ash
grain based on the density of pumice and dense rock from the same eruption.
It uses the method described in the Bonadonna and Phillips (2003) paper.

```python
>>> from tephrange.density import bp2003
>>> bp2003(250 * 1e-6, rho_pumice=440, rho_glass=2300)
1137.5
```

### Travel distance

The functions above are combined in the `Particle` class.
A Particle can be initialised with defined physical properties and is then
able to calculate how far it can travel if falling from a given altitude with
a given windspeed.

```python
>>> from tephrange.particle import Particle
>>> p = Particle(65 * 1e-6, sphericity=0.7, particle_density=2000)
>>> p.calculate_distance(release_height=10000, windspeed=10,
                         fall_step=10, velocity_function='ganser')
476.4523519938956
```

## Feedback

Please send any feedback / bug reports via the [GitHub issue tracker](https://github.com/volcan01010/tephrange/issues).

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
