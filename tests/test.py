# Import the pyinspectx module locally
import sys, os
sys.path.insert(0, '../pyinspectx')

import pyinspectx as PyInspectX

# Load example file
testCode = open(os.path.abspath(os.path.join(os.getcwd(), 'tests/example.py')), 'r', encoding='utf-8').read()

# Debugger
inspector = PyInspectX.Inspector()
inspector.modify_code(testCode)