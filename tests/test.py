import pyinspectx as PyInspectX

# Load example file
testCode = open('test.py', 'r', encoding='utf-8').read()

# Debugger
inpesctor = PyInspectX.Inspector(testCode)
inpesctor.modify_code()