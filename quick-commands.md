# HiTyper

## l1-parse.py

- `hityper findusertype -s hityper-listings/l1-parse.py -p hityper-listings -v -d outputs`
- `hityper gentdg -s hityper-listings/l1-parse.py -p hityper-listings -d outputs -f json -o`
- `hityper infer -s hityper-listings/l1-parse.py -p hityper-listings -d outputs/ -n 5 -t`

## l2-abstract_node.py

- `hityper findusertype -s hityper-listings/l2-abstract_node.py -p hityper-listings -v -d outputs`
- `hityper gentdg -s hityper-listings/l2-abstract_node.py -p hityper-listings -d outputs -f pdf -o`
- `hityper infer -s hityper-listings/l2-abstract_node.py -p hityper-listings -d outputs/ -n 2 -t`


## python3-titw/expressions.py

- `hityper findusertype -s python3-titw/expressions.py -p python3-titw -v -d outputs`
- `hityper gentdg -s python3-titw/expressions.py -p python3-titw -d outputs -f json -o`
- `hityper infer -s python3-titw/expressions.py -p python3-titw -d outputs/ -n 5 -t`

# PyType

# l1-string-int-add.py

- `hityper infer -s pytype-listings/l1-string-int-add.py -p pytype-listings -d outputs/ -n 5 -t`

# l2-strict-typing.py

- `hityper infer -s pytype-listings/l2-strict-typing.py -p pytype-listings -d outputs/ -n 5 -t`