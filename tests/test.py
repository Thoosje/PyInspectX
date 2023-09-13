# Import the pyinspectx module locally
import sys, os
sys.path.insert(0, '../pyinspectx')

import pyinspectx as PyInspectX

# Load example file
testCode = open(os.path.abspath(os.path.join(os.getcwd(), 'tests/example.py')), 'r', encoding='utf-8').read()

# Debugger
inspector = PyInspectX.Inspector()
inspector.modify_code(testCode)
modified_code = inspector.get_modified_code()

#print(modified_code)
exec(modified_code, {}, {}) # Pass {} for globals and locals so else our current scope will be used.
# TODO: Move this into a method for the inspector class and return in a better viewable format.