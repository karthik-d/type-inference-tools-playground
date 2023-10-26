Experiments and tests on *symbolic execution*, *type inference*, and *property-guided testing* of python code: scripts and codebases.

## Git Submodules in this repository

- HiTyper for Python.
- Atheris for Python.
- CrossHair for Python.
- PyType - Pyhon's type binder.

## Datasets

More information about the datasets used can be found in a [dedicated dataset README](./data/README.md). The following datasets were used for the experiments.

- [ManyTypes4Py](https://www.computer.org/csdl/proceedings-article/msr/2021/871000a585/1tB7kkYXqzS).

## Installations and Dependencies

### HiTyper
- Cloned as a Git submodule.
- Installed using pip: `pip install ./HiTyper/`.
- To experiment with its source code, make changes in the submodule and reinstall with pip.
- To generate TDGs as PDFs, there is a dependecy on GraphViz. Install it as a binary on the system, for instance, using apt: `$ apt-get install graphviz`.

#### Dependencies

- Python >= 3.9
- Linux

> [!Important]
> HiTyper requires running on Python >= 3.9 because there are a lot of new nodes introduced on AST from Python 3.9. However, HiTyper can analyze most files written under Python 3 since Python's AST is backward compatible.
