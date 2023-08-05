The moiety_modeling Tutorial 
============================

The `moiety_modeling` can be used to:
    * Construct a moiety model.
    * Optimize parameters of a moiety model.
    * Analyze optimized results and select the optimal model.
    * Visualize the optimized results.

In this document, each use will be explained in details.

The moiety_modeling API tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using moiety_modeling to construct a moiety model
-----------------------------------------------

In moiety modeling, we dissemble molelcules into molecular parts called moieties (called functional groups in chemistry), and then deconvolute molecular isotopic incorporation into moiety isotopic. A constructed moiety model is then stored in a JSON file.

Here is an example of moiety model construction.

.. code:: Python
    
    >>> import moiety_modeling
    >>> import jsonpickle
    >>> ribose = moiety_modeling.Moiety("ribose", {'13C': 5}, isotopeStates={'13C': [0, 2, 3, 5]}, nickname='r')   # moiety creation
    >>> glucose = moiety_modeling.Moiety("glucose", {'13C': 6}, isotopeStates={'13C': [0, 3, 6]}, nickname='g')
    >>> acetyl = moiety_modeling.Moiety("acetyl", {'13C': 2}, isotopeStates={'13C': [0, 2]}, nickname='a')
    >>> uracil = moiety_modeling.Moiety("uracil", {'13C': 4}, isotopeStates={'13C': [0, 1, 2, 3]}, nickname='u')
    >>> relationship1 = moiety_modeling.Relationship(glucose1, '13C3', ribose1, '13C2', '*', 2)   # relationship creation
    >>> relationship2 = moiety_modeling.Relationship(ribose1, '13C3', ribose1, '13C2')
    >>> relationship3 = moiety_modeling.Relationship(glucose1, '13C0', ribose1, '13C0')
    >>> relationship4 = moiety_modeling.Relationship(glucose1, '13C6', ribose1, '13C5')
    >>> UDP_GlcNAC = moiety_modeling.Molecule('UDP_GlcNAC', [ribose, glucose, acetyl, uracil])   # molecule creation
    >>> model = moiety_modeling.Model('6_G0R2A1U3_g3r2r3_g6r5', [ribose, glucose, acetyl, uracil], [UDP_GlcNAC], [relationship1, relationship2, relationship3, relationship4])  
    >>> with open('model.json', 'w') as outFile:   # store the model into JSONPickle file.
            outFile.write(jsonpickle.encode({'models': [model]}))

The moiety states can also be constructed using all the possible states.

.. code:: Python

    >>> glucose = moiety_modeling.Moiety("glucose", {'13C': 6, '18O': 5}, states=['13C_0.18O_0', '13C_6.18O_5'], nickname='g')
    >>> ribose = moiety_modeling.Moiety("ribose", {'13C': 5, '18O': 4}, states=['13C_0.18O_0', '13C_5.18O_4'], nickname='r')
    >>> acetyl = moiety_modeling.Moiety("acetyl", {'13C': 2, '18O': 1}, states=['13C_0.18O_0', '13C_2.18O_1'], nickname='a')    
    >>> uracil = moiety_modeling.Moiety("uracil", {'13C': 4, '18O': 2}, states=['13C_0.18O_0', '13C_1.18O_0', '13C_2.18O_1', '13C_2.18O_0', '13C_3.18O_0', '13C_3.18O_1'], nickname='u')

Using moiety_modeling to store isotopologue dataset
---------------------------------------------------

The Dataset class in the 'moiety_modeling' package organizes a single mass spectroscopy isotopologue profile dataset into a dictionary-based data structure.

Here is an example of dataset construction.

.. code:: Python

    >>> import moiety_modeling
    >>> import jsonpickle
    >>> dataset1 = moiety_modeling.Dataset("12h", {'UDP_GlcNAC': 
                  [{'labelingIsotopes': '13C_0', 'height': 0.0175442549, 'heightSE': 0},
                   {'labelingIsotopes': '13C_1', 'height': 0, 'heightSE': 0},
                   {'labelingIsotopes': '13C_2', 'height': 0.0007113347, 'heightSE': 0},
                   {'labelingIsotopes': '13C_3', 'height': 0.0002990498, 'heightSE': 0},
                   {'labelingIsotopes': '13C_4', 'height': 0.0012322448, 'heightSE': 0},
                   {'labelingIsotopes': '13C_5', 'height': 0.0962990868, 'heightSE': 0},
                   {'labelingIsotopes': '13C_6', 'height': 0.0737941503, 'heightSE': 0},
                   {'labelingIsotopes': '13C_7', 'height': 0.0194440036, 'heightSE': 0},
                   {'labelingIsotopes': '13C_8', 'height': 0.063026207, 'heightSE': 0},
                   {'labelingIsotopes': '13C_9', 'height': 0.0058731399, 'heightSE': 0},
                   {'labelingIsotopes': '13C_10', 'height': 0.0312896069, 'heightSE': 0},
                   {'labelingIsotopes': '13C_11', 'height': 0.3124695022, 'heightSE': 0},
                   {'labelingIsotopes': '13C_12', 'height': 0.0573898846, 'heightSE': 0},
                   {'labelingIsotopes': '13C_13', 'height': 0.277122791, 'heightSE': 0},
                   {'labelingIsotopes': '13C_14', 'height': 0.0234859781, 'heightSE': 0},
                   {'labelingIsotopes': '13C_15', 'height': 0.0200187655, 'heightSE': 0},
                   {'labelingIsotopes': '13C_16', 'height': 0, 'heightSE': 0},
                   {'labelingIsotopes': '13C_17', 'height': 0, 'heightSE': 0}]})
    >>> dataset2 = moiety_modeling.Dataset("24h", {'UDP_GlcNAC': 
                  [{'labelingIsotopes': '13C_0', 'height': 0.00697626, 'heightSE': 0},
                   {'labelingIsotopes': '13C_1', 'height': 0, 'heightSE': 0},
                   {'labelingIsotopes': '13C_2', 'height': 0.0008426934, 'heightSE': 0},
                   {'labelingIsotopes': '13C_3', 'height': 0.0007070956, 'heightSE': 0},
                   {'labelingIsotopes': '13C_4', 'height': 0.0006206594, 'heightSE': 0},
                   {'labelingIsotopes': '13C_5', 'height': 0.068147345, 'heightSE': 0},
                   {'labelingIsotopes': '13C_6', 'height': 0.0499393097, 'heightSE': 0},
                   {'labelingIsotopes': '13C_7', 'height': 0.023993641, 'heightSE': 0},
                   {'labelingIsotopes': '13C_8', 'height': 0.062901247, 'heightSE': 0},
                   {'labelingIsotopes': '13C_9', 'height': 0.0056603032, 'heightSE': 0},
                   {'labelingIsotopes': '13C_10', 'height': 0.0281210238, 'heightSE': 0},
                   {'labelingIsotopes': '13C_11', 'height': 0.2482899264, 'heightSE': 0},
                   {'labelingIsotopes': '13C_12', 'height': 0.0613088541, 'heightSE': 0},
                   {'labelingIsotopes': '13C_13', 'height': 0.3325253653, 'heightSE': 0},
                   {'labelingIsotopes': '13C_14', 'height': 0.0499904271, 'heightSE': 0},
                   {'labelingIsotopes': '13C_15', 'height': 0.0537153908, 'heightSE': 0},
                   {'labelingIsotopes': '13C_16', 'height': 0.0062604583, 'heightSE': 0},
                   {'labelingIsotopes': '13C_17', 'height': 0, 'heightSE': 0}]})   # dataset creation
    >>> with open('dataset.json', 'w') as outFile: # store dataset into JSONPickle file.
            outFile.write(jsonpickle.encode({'datasets': [dataset1, dataset2]}))

Setting optimization parameters
-------------------------------

The optimization parameters are stored in a JSON file. Several optimization methods, including SAGA and three scipy optimization methods ('TNC', 'SLSQP', 'L_BFGS_B'), are available in the package. When using the SAGA optimization method, optimization parameters for SAGA should be specified. The parameters for scipy optimization methods can also be modified. Please refer the correponding API for detailed information.

Here is the example of optimization parameters construction. 

.. code:: Python
    
    >>> import jsonpickle
    >>> setting = {'SAGA': {'methodParameters': {'alpha': 1, 'crossoverRate': 0.05, 'mutationRate': 3, 'populationSize': 20, 
                   'startTemperature': 0.5, 'stepNumber': 500, 'temperatureStepSize': 100},
                   'noPrintAllResults': 1, 'noPrintBestResults': 0, 'optimizationSetting': 'SAGA_500'}, 
                   'TNC': {'methodParameters': None, 'optimizationSetting': 'TNC'} }
    >>> with open('optimizationSetting.json', 'w') as outFile:
            outFile.write(jsonpickle.encode({'optimizations': setting}))

The moiety_modeling CLI tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using moiety_modeling to optimize parameters of moiety model
------------------------------------------------------------

To conduct the optimization, moiety model, datasets, and optimization settings should be provided. Please use the -h for more information of the option parameters.

.. code:: Python

    python3 -m moiety_modeling modeling --models=<model_jsonfile> --datasets=<dataset_jsonfile> --optimizations=<optimizationSetting_json> --repetition=100 --split --multiprocess --energyFunction=logDifference

Using moiety_modeling to analyze optimized results and select the optimal model
-------------------------------------------------------------------------------

The `moiety_modeling` package provides facilities to analyze the optimization results, select the optimal model, and compare the selection results under different optimization settings. Please refer to API for detailed information of option parameters.

.. code:: Python

    python3 -m moiety_modeling analyze optimizations --a <optimizationPaths_txtfile>   # To analyze the optimization results of multiple moiety models together.
    python3 -m moiety_modeling analyze optimizations --s <optimzationResults_jsonfile>   # To analyze the optimization results of a single moiety model. 
    python3 -m moiety_modeling analyze rank <analysisPaths_txtfile> --rankCriteria=AICc   # To rank models according to the selection criteria.
    python3 -m moiety_modeling analyze table <rankPaths_txtfile>   # To compare the selection results under different optimizaton settings.

Using moiety_modeling to visualize the optimized results
-------------------------------------------------------

The 'moiety_modeling' package provides facilities to visualize the optimization results.

.. code:: Python

    python3 -m moiety_modeling plot moiety <analysisResults_jsonfile>   # To plot the distribution of calculated moiety modeling parameters.
    python3 -m moiety_modeling plot isotopologue <analysisResults_jsonfile>   # To plot the comparison of calculated and observed isotopologue intensities.



