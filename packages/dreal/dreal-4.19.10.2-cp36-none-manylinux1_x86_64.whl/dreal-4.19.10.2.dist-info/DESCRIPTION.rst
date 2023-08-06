dReal4: SMT Solver for Nonlinear Theories of Reals

Please visit https://github.com/dreal/dreal4.


Precompiled Wheels
------------------

We provide precompiled distributions (`.whl`) for the following environments:

 - macOS 10.15 / 10.14 / 10.13 + CPython 3.7
 - Linux + CPython 3.5 / 3.6 / 3.7

You still need to install dReal prerequisites such as IBEX and CLP in
your system. To install them, please follow the instructions below:

macOS 10.15 / 10.14 / 10.13

    brew install dreal --only-dependencies

Ubuntu 18.04 / 16.04

    curl -fsSL https://raw.githubusercontent.com/dreal/dreal4/master/setup/ubuntu/`lsb_release -r -s`/install.sh | sudo bash


Build from Source
-----------------

If `pip` fails to find a precompiled distribution, it fetchs dReal
source and build it from scratch. You need to install the required
packages to do so. To install them, please follow the instructions
below:

macOS 10.15 / 10.14 / 10.13

    brew install dreal --only-dependencies --build-from-source

Ubuntu 18.04 / 16.04

    curl -fsSL https://raw.githubusercontent.com/dreal/dreal4/master/setup/ubuntu/`lsb_release -r -s`/install_prereqs.sh | sudo bash



