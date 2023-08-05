moiety_modeling
===============

.. image:: https://img.shields.io/pypi/v/moiety_modeling.svg
   :target: https://pypi.org/project/moiety_modeling
   :alt: Current library version

.. image:: https://img.shields.io/pypi/pyversions/moiety_modeling.svg
   :target: https://pypi.org/project/moiety_modeling
   :alt: Supported Python versions

.. image:: https://api.travis-ci.org/MoseleyBioinformaticsLab/moiety_modeling.svg?branch=master
   :target: https://travis-ci.org/MoseleyBioinformaticsLab/moiety_modeling
   :alt: Travis CI status


`moiety_modeling` package provides facilities for moiety model representation, model optimization and model selection.


Citation
~~~~~~~~

Please cite the GitHub repository until our manuscript is accepted for 
publication: https://github.com/MoseleyBioinformaticsLab/moiety_modeling.git


Installation
~~~~~~~~~~~~

'moiety_modeling' runs under Python 3.6+ and is available through python3-pip.
Install via pip or clone the git repo and install the following depencies and 
you are ready to go!


Install on Linux
~~~~~~~~~~~~~~~~

Pip installation
----------------

.. code:: bash

   python3 -m pip install moiety-modeling

GitHub Package installation
---------------------------

Make sure you have git_ installed:

.. code:: bash

   git clone https://github.com/MoseleyBioinformaticsLab/moiety_modeling.git


Dependencies
------------

'moiety_modeling' requires the following Python libraries:

    * docopt_ for creating the command-line interface.
    * jsonpickle_ for saving Python objects in a JSON serializable form and outputting to a file.
    * numpy_ and matplotlib_ for visualization of optimized results.
    * scipy_ for application of optimization methods.
    * SAGA-optimize_ for parameters optimization. 


Quickstart
~~~~~~~~~~

Using moiety_modeling to optimize parameters of moiety model.

.. code:: bash

   python3 -m moiety_modeling modeling --models=<model_jsonfile> --datasets=<dataset_jsonfile> --optimizations=<optimizationSetting_json> --repetition=100 --split --multiprocess --energyFunction=logDifference

Using moiety_modeling to analyze optimized results and select the optimal model.

.. code:: bash

   python3 -m moiety_modeling analyze optimizations --a <optimizationPaths_txtfile>
   python3 -m moiety_modeling analyze rank <analysisPaths_txtfile> --rankCriteria=AICc

Using moiety_modeling to visualize the optimzed results.

.. code:: bash 

   python3 -m moiety_modeling plot moiety <analysisResults_jsonfile>

.. note:: Read the User Guide and the ``moiety_modeling`` Tutorial on ReadTheDocs_ to learn more and to see code examples on using the ``moiety_modeling`` as a library and as a command-line tool.

License
~~~~~~~

Made available under the terms of The modified Clear BSD License. See full license in LICENSE_.

Authors
~~~~~~~

* **Huan Jin**
* **Hunter N.B. Moseley**


.. _pip: https://pip.pypa.io/
.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/
.. _docopt: https://github.com/docopt/docopt
.. _jsonpickle: https://github.com/jsonpickle/jsonpickle
.. _numpy: http://www.numpy.org/
.. _matplotlib: https://github.com/matplotlib/matplotlib
.. _scipy: https://github.com/scipy/scipy
.. _SAGA-optimize: https://pypi.org/project/SAGA-optimize/
.. _LICENSE: https://github.com/MoseleyBioinformaticsLab/moiety_modeling/blob/master/LICENSE
.. _ReadTheDocs: https://moiety-modeling.readthedocs.io/en/latest/


