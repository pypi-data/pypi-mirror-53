# Sqreen Native Python Module

[![Build Status](https://dev.azure.com/sqreenci/AgentPythonNative/_apis/build/status/sqreen.AgentPythonNative?branchName=master)](https://dev.azure.com/sqreenci/AgentPythonNative/_build/latest?definitionId=1&branchName=master)

The native libraries are added to this Python module with git submodules.

Build the binary wheel with:
```
pip install cmake
python setup.py bdist_wheel
```

Build the source package (without the libraries) with:
```
python setup.py sdist
```
