# HiTyper
![](https://img.shields.io/badge/Version-1.0-blue)



This is the tool released in the ICSE 2022 paper ["Static Inference Meets Deep Learning: A Hybrid Type InferenceApproach for Python"](https://arxiv.org/abs/2105.03595).

## Workflow

HiTyper is a hybrid type inference tool built upon Type Dependency Graph (TDG), the typical workflow of it is as follows:

![](https://github.com/JohnnyPeng18/HiTyper/blob/main/imgs/workflow.png)

For more details, please refer to the [paper](https://arxiv.org/abs/2105.03595).

## Methdology

The general methdology of HiTyper is:

1) Static inference is accurate but suffer from coverage problem due to dynamic features

2) Deep learning models are feature-agnostic but they can hardly maintain the type correctness and are unable to predict unseen user-defined types

The combination of static inference and deep learning shall complement each other and improve the coverage while maintaining the accuracy.

## Install

To use HiTyper on your own computer, you can build from source: (If you need to modify the source code of HiTyper, please use this method and re-run the `pip install .` after modification each time)

```sh
git clone https://github.com/JohnnyPeng18/HiTyper.git && cd HiTyper
pip install .
```

**Requirements:**

- Python>=3.9
- Linux

HiTyper requires running under Python >= 3.9 because there are a lot of new nodes introduced on AST from Python 3.9. However, HiTyper can analyze most files written under Python 3 since Python's AST is backward compatible.

You are recommended to use `Anaconda` to create a clean Python 3.9 environment and avoid most dependency conflicts:

````sh
conda create -n hityper python=3.9
````

## Usage

Currently HiTyper has the following command line options: (Some important settings are stored in file `config.py`, you may need to modify it before running HiTyper)

### findusertype

```sh
hityper findusertype [-h] [-s SOURCE] -p REPO [-v] [-d OUTPUT_DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Path to a Python source file
  -p REPO, --repo REPO  Path to a Python project
  -v, --validate        Validate the imported user-defined types by finding their implementations
  -d OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Path to the store the usertypes
```

**Example:**

```sh
hityper findusertype -s python_project_repo/test.py -p python_project_repo -v -d outputs
```

*This command generates the user-defined types collected by HiTyper and save them as `.json` files under `outputs/` folder.*

### gentdg

```sh
hityper gentdg [-h] [-s SOURCE] -p REPO [-o] [-l LOCATION] [-a] [-c] [-d OUTPUT_DIRECTORY] [-f {json,pdf}]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Path to a Python source file
  -p REPO, --repo REPO  Path to a Python project
  -o, --optimize        Remove redundant nodes in TDG
  -l LOCATION, --location LOCATION
                        Generate TDG for a specific function
  -a, --alias_analysis  Generate alias graphs along with TDG
  -c, --call_analysis   Generate call graphs along with TDG
  -d OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Path to the generated TDGs
  -f {json,pdf}, --output_format {json,pdf}
                        Formats of output TDGs
```

**Example:**

```
hityper gentdg -s python_project_repo/test.py -p python_project_repo -d outputs -f json -o
```

*This command generates the TDG for all functions in file `python_project_repo/test.py` and save them into `outputs` folder.* 

Note that if you choose `json` format to save TDG, it will be only ONE `json` file that contains all TDGs in the source file. However, if you choose `pdf` format to save TDG, then there will be multiple `pdf` files and each one correspond to one function in the source file. This is because a pdf file can hardly contain a large TDG for every functions.

For the location indicated by `-l`, use the format `funcname@classname` and use `global` as the classname if the function is a global function.

HiTyper uses [PyCG](https://github.com/vitsalis/PyCG) to build call graphs in call analysis. Alias analysis and call analysis are temporarily built-in but HiTyper does not use them in inference. Further updates about them will be involved in HiTyper. 

### infer

```sh
hityper infer [-h] [-s SOURCE] -p REPO [-l LOCATION] [-d OUTPUT_DIRECTORY] [-m RECOMMENDATIONS] [-t] [-n TOPN]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Path to a Python source file
  -p REPO, --repo REPO  Path to a Python project
  -l LOCATION, --location LOCATION
                        Type inference for a specific function
  -d OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Path to the generated TDGs
  -m RECOMMENDATIONS, --recommendations RECOMMENDATIONS
                        Path to the recommendations generated by a DL model
  -t, --type4py         Use Type4Py as the recommendation model
  -n TOPN, --topn TOPN  Indicate the top n predictions from DL models used by HiTyper
```

**Example:**

```
hityper infer -s python_project_repo/test.py -p python_project_repo -d outputs -n 1 -t 
```

*This command generates the inferred types for all variables, arguments and return values in the source file and save them into `output` folder.*

If you do not specify `-m` or `-t` option, then HiTyper will only use the static inference part to infer types. Static inference generally takes several minutes.

For the location indicated by `-l`, use the format `funcname@classname` and use `global` as the classname if the function is a global function.

**Recommendation Model:**

Note that HiTyper natively supports the recommendations from Type4Py and it invokes the following API provided by Type4Py to get recommendations if you use option `-t`:

```
https://type4py.com/api/predict?tc=0
```

**This will upload your file to the Type4Py server!** If you do not want to upload your file, you can use the [docker](https://github.com/saltudelft/type4py/wiki/Using-Type4Py-Rest-API) provided by Type4Py and changes the API in `config.py` into:

```
http://localhost:PORT/api/predict?tc=0
```

**HiTyper's performance deeply depends on the maximum performance of recommendation model (especially the performance to predict argument types). Type inference of HiTyper can fail if the recommendation model cannot give a valid prediction while static inference does not work!!!** 

If you want to use another more powerful model, you write code like `__main__.py` to adapt HiTyper to your DL model.

### eval

```sh
hityper eval [-h] -g GROUNDTRUTH -c CLASSIFIED_GROUNDTRUTH -u USERTYPE [-m RECOMMENDATIONS] [-t] [-n TOPN]

optional arguments:
  -h, --help            show this help message and exit
  -g GROUNDTRUTH, --groundtruth GROUNDTRUTH
                        Path to a ground truth dataset
  -c CLASSIFIED_GROUNDTRUTH, --classified_groundtruth CLASSIFIED_GROUNDTRUTH
                        Path to a classified ground truth dataset
  -u USERTYPE, --usertype USERTYPE
                        Path to a previously collected user-defined type set
  -m RECOMMENDATIONS, --recommendations RECOMMENDATIONS
                        Path to the recommendations generated by a DL model
  -t, --type4py         Use Type4Py as the recommendation model
  -n TOPN, --topn TOPN  Indicate the top n predictions from DL models used by HiTyper
```

**Example:**

```sh
hityper eval -g groundtruth.json -c detailed_groundtruth.json -u usertypes.json -n 1 -t
```

*This command evaluates the performance of HiTyper on a pre-defined groundtruth dataset. It will output similar results like stated in `Experiment Results` part.*

Before evaluating Hityper using this command, please use `hityper findusertype` command to generate `usertypes.json`. This typically takes several hours, depending on the number of files.

This option is designed only for future research evaluation.

## Experiment Results

**Dataset:**

The following results are evaluated using the [ManyTypes4Py](https://zenodo.org/record/4719447#.YjxcpBNBxb8) dataset. 

Since the original dataset does not contain Python source files, to facilitate future research, we here also attached a [link](https://drive.google.com/file/d/1HdZyd3dKAUkiv2Nl0Zynp_YhrqU6HfMx/view?usp=sharing) for the Python source files HiTyper uses to infer types. Attached dataset is not identical with the original one because the original one contains some GitHub repos that do not allow open access or have been deleted.

Note that as stated in the paper, there exists few cases (such as subtypes and same types with different names) that HiTyper should be correct but still counted as wrong in the evaluation process.

**Metrics:**

For the definition of metrics used here, please also refer to the paper. These metrics can be regarded as a kind of "recall", which evaluates the coverage of HiTyper on a specific dataset. We do not show the "precision" here as HiTyper only outputs results when it does not observe any violations with current typing rules and TDG.

**Only using the static inference part:**

| Category           | Exact Match | Match to Parametric | Partial Match |
| ------------------ | ----------- | ------------------- | ------------- |
| Simple Types       | 59.00%      | 59.47%              | 62.15%        |
| Generic Types      | 55.50%      | 69.68%              | 71.90%        |
| User-defined Types | 40.40%      | 40.40%              | 44.30%        |
| Arguments          | 7.65%       | 8.05%               | 14.39%        |
| Return Values      | 58.71%      | 64.61%              | 69.06%        |
| Local Variables    | 61.56%      | 65.66%              | 67.05%        |

You can use the following command to reproduce the above results:

```sh
hityper eval -g ManyTypes4Py_gts_test_verified.json -c ManyTypes4Py_gts_test_verified_detailed.json -u ManyTypes4Py_test_usertypes.json 
```

We do not show the performance of HiTyper integrating different DL models here since there are many factors impacting the performance of DL models such as datasets, hyper-parameters, etc. Please align the performance by yourself before utilizing recommendations from DL models.
 
What's more, we are currently working on building a DL model that's more suitable for HiTyper. Stay tuned!

**Other datasets:**

If you want to evaluate HiTyper on other datasets, please generate files with the same format with `ManyTypes4Py_gts_test_verified.json`, `ManyTypes4Py_gts_test_verified_detailed.json`, or you can modify the code in `__main__.py`. To check a type's category, you can use `hityper.typeobject.TypeObject.checkType()`.

In any case, you must also prepare the source files for static analysis.

**Old results:**

If you want the exact experiment results stated in the paper, please download them at this [link](https://drive.google.com/file/d/1zFVStp085bfv8WU7UCk9pIE2HEEf-CUh/view?usp=sharing).

## Todo

- Add supports for inter-procedural analysis
- Add supports for types from third-party modules
- Add supports for external function calls
- Add supports for stub files

## Cite Us

If you use HiTyper in your research, please cite us:

```latex
@article{peng2022hityper,
  author    = {Yun Peng and Cuiyun Gao and Zongjie Li and Bowei Gao and David Lo and Qirun Zhang and Michael R. Lyu},
  title     = {Static Inference Meets Deep Learning: A Hybrid Type Inference Approach for Python},
  journal   = {CoRR},
  volume    = {abs/2105.03595},
  year      = {2022},
  url       = {https://arxiv.org/abs/2105.03595}
}
```

## Contact

We actively maintain this project and welcome contributions. 

If you have any question, please contact research@yunpeng.work.

