# PyInspectX

A simple Python package to access all variables, per scope after a runtime. Can be used
for multiple purposes. Mainly debugging.

## Installation

```bash
pip install pyinspectx
```

## Usage

The main class of the program is the ```Inspector``` class. This class can be used to inspect the variables inside the runtime.

> We start generating the modified code. This code can be ran like you wish.
> The snippet below shows how to generate the modified code.

```python
from pyinspectx import Inpesctor

testCode = open(os.path.abspath(os.path.join(os.getcwd(), 'example.py')), 'r', encoding='utf-8').read()

inspector = PyInspectX.Inspector()
inspector.modify_code(testCode)

modified_code = inspector.get_modified_code()
print(modified_code)
```

> There is a built in method that generates a temp file inside the current working directory and runs the result for you. The output can be accessed inside a variable.

```python
from pyinspectx import Inpesctor

testCode = open(os.path.abspath(os.path.join(os.getcwd(), 'example.py')), 'r', encoding='utf-8').read()

inspector = PyInspectX.Inspector()
inspector.modify_code(testCode)

output = inspector.run_modified_code()
print(output)
```

** IMPORTANT: Do not run the code using exec() or eval()! Wrong results will occure. **

## TODO
* Add general (regex and keyword) support to block basic variable names inside the runtime.
* Add support to customize injected code variable names so they don't conflict with the runtime.
* Make a better viewer for the raw data
* New JSON output format so it can be used for automation and testing.
* FInd more edge cases
* Check for compatibility with other Python versions and systems.