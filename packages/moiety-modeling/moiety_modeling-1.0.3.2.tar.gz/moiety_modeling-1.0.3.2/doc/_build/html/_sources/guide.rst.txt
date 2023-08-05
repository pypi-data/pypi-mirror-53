User Guide
==========

Description
~~~~~~~~~~~

The :mod:`moiety_modeling` package provides a simple Python interface for moiety model representation, model optimization and model selection. Both moiety models and isotopologue datasets are stored in`JSON` files, which can be used for further model optimization, selection, analysis and visualization. 

Installation
~~~~~~~~~~~~

`moiety_modeling` runs under Python 3.6+ and is available through python3-pip. Install via pip or clone the git repo and install the following dependencies and you are ready to go!

Install on Linux
----------------

Pip installation (method 1)
...........................

.. code:: bash

    python3 -m pip install moiety-modeling

GitHub Package installation (method 2)
......................................

Make sure you have git_ installed:

.. code:: bash

   git clone https://github.com/MoseleyBioinformaticsLab/moiety_modeling.git
    
Dependecies 
...........

`moiety_modeling` requires the following Python libraries:
    
    * docopt_ for creating the command-line interface.
    * jsonpickle_ for saving Python objects in a JSON serializable form and outputting to a file.
    * numpy_ and matplotlib_ for visualization of optimized results.
    * scipy_ for application of optimization methods.
    * SAGA-optimize_ for parameters optimization. 

Basic usage
~~~~~~~~~~~
The :mod:`moiety_modeling` package can be used in several ways:
   
    * As a library for accessing and manipulating moiety models and isotopologue datasets stored in the `JSON` files.
    * As a command-line tool:
        * Optimize the moiety model parameters.
        * Analyze the optimization results of moiety model, and select the optimal model.
        * Visuslize the optimized results.

.. note:: Read :doc:`tutorial` to learn more and see code examples on using the :mod:`moiety_modeling` as a library and as a command-line tool.

.. _pip: https://pip.pypa.io/
.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/
.. _docopt: https://github.com/docopt/docopt
.. _jsonpickle: https://github.com/jsonpickle/jsonpickle
.. _numpy: http://www.numpy.org/
.. _matplotlib: https://github.com/matplotlib/matplotlib
.. _scipy: https://github.com/scipy/scipy
.. _SAGA-optimize: https://pypi.org/project/SAGA-optimize/
