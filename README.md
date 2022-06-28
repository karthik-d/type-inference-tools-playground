## Current Git Submodules

- HiTyper


## Installations and Dependencies

### HiTyper
- Cloned as a Git Submodule
- Installed using pip, as `pip install ./HiTyper/`
- To experiment with its source code, make changes in the submodule and reinstall with pip
- To generate TDGs as PDFs, there is a dependecy on GraphViz. Install it as a binary on the system, for instance, using apt: `$apt-get install graphviz`

#### Dependencies

- Python>=3.9
- Linux

**NOTE**: HiTyper requires running under Python >= 3.9 because there are a lot of new nodes introduced on AST from Python 3.9. However, HiTyper can analyze most files written under Python 3 since Python's AST is backward compatible.


## Datasets

More information about the datasets used can be found in a dedicated README, [here](./data/README.md)

- ManyTypes4Py