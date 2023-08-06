# Scallop - quantitative evaluation of single-cell cluster memberships

[![pipeline status](https://img.shields.io/gitlab/pipeline/alexmascension/scallop/master?label=build%3Amaster)](https://gitlab.com/alexmascension/scallop/commits/master)
[![Coverage report master](https://codecov.io/gl/alexmascension/scallop/branch/master/graph/badge.svg)](https://codecov.io/gl/alexmascension/scallop/branch/master)
[![Docs master](https://readthedocs.org/projects/pip/badge/?version=master&label=docs%3Amaster)](https://scallop.readthedocs.io/en/master/)
[![pipeline status](https://img.shields.io/gitlab/pipeline/alexmascension/scallop/dev?label=build%3Adev)](https://gitlab.com/alexmascension/scallop/commits/dev)
[![Coverage report dev](https://codecov.io/gl/alexmascension/scallop/branch/dev/graph/badge.svg)](https://codecov.io/gl/alexmascension/scallop/branch/dev)
[![Docs dev](https://readthedocs.org/projects/pip/badge/?version=dev&label=docs%3Adev)](https://scallop.readthedocs.io/en/dev/)
[![Pypi version](https://img.shields.io/pypi/v/scallop)](https://img.shields.io/pypi/v/scallop)



Scallop is a module for the evaluation of single-cell clustering solutions. 
It allows users to assess the quality of clustering using different
algorithms and parameter choices. 

Scallop provides users with a cell-wise robustness score based on bootstrap experiments, 
and a versatile plotting toolkit for visualization purposes. 

Scallop is meant to be used 
with annData objects from Scanpy. 
