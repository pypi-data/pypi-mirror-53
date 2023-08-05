===========
pyDiffusion
===========

.. image:: https://img.shields.io/pypi/status/pydiffusion.svg
    :target: https://pypi.python.org/pypi/pydiffusion/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/v/pydiffusion.svg
    :target: https://pypi.python.org/pypi/pydiffusion/
    :alt: Latest version

.. image:: https://img.shields.io/pypi/pyversions/pydiffusion.svg
    :target: https://pypi.python.org/pypi/pydiffusion/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/pydiffusion.svg
    :target: https://pypi.python.org/pypi/pydiffusion/
    :alt: License

**pyDiffusion** combines tools like **diffusion simulation**, **diffusion data smooth**, **forward simulation analysis (FSA)**, etc. to help people analyze diffusion data efficiently.

Dependencies
------------

* Python 3.5+
* numpy, matplotlib, scipy, pandas

Installation
------------

Via pip(recommend)

.. code-block::

    pip install pydiffusion

Examples
--------

Diffusion Simulation
~~~~~~~~~~~~~~~~~~~~

Based on Ni-Mo interdiffusion coefficients data at 1100C, simulate the diffusion process for 800 hours. See `Diffusion Simulation Example`_.

.. image:: https://github.com/zhangqi-chen/pyDiffusion/blob/master/docs/examples/DiffusionSimulation_files/DiffusionSimulation_3.png

Forward Simulation Analysis (FSA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate interdiffusion coefficients of Ni-Mo at 1100C based on raw diffusion data (1000 hours). See `FSA Example`_.

.. image:: https://github.com/zhangqi-chen/pyDiffusion/blob/master/docs/examples/FSA_files/FSA_2.png

Error Analysis
~~~~~~~~~~~~~~

The interdiffusion coefficients in Ti-Zr system at 1000C are calculated using FSA. The error bounds of the diffusivity data are estimated using error analysis tool. See `Error Analysis Example`_.

.. image:: https://github.com/zhangqi-chen/pyDiffusion/blob/master/docs/examples/ErrorAnalysis_files/ErrorAnalysis_3.png

Citing
------

If you use pydiffusion in your research, please consider citing the following article published in JORS:

Chen, Z., Zhang, Q. and Zhao, J.-C., 2019. pydiffusion: A Python Library for Diffusion Simulation and Data Analysis. Journal of Open Research Software, 7(1), p.13. DOI: http://doi.org/10.5334/jors.255

.. _Diffusion Simulation Example: https://github.com/zhangqi-chen/pyDiffusion/blob/master/docs/examples/DiffusionSimulation.rst
.. _FSA Example: https://github.com/zhangqi-chen/pyDiffusion/blob/master/docs/examples/FSA.rst
.. _Error Analysis Example: https://github.com/zhangqi-chen/pyDiffusion/blob/master/docs/examples/ErrorAnalysis.rst
