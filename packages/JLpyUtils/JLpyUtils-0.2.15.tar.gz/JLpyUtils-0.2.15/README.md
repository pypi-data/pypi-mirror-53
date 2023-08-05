[![Build Status](https://travis-ci.com/jlnerd/JLpyUtils.svg?branch=master)](https://travis-ci.com/jlnerd/JLpyUtils)
[![codecov](https://codecov.io/gh/jlnerd/JLpyUtils/branch/master/graph/badge.svg)](https://codecov.io/gh/jlnerd/JLpyUtils)


# JLpyUtils
__Author: [John T. Leonard](https://www.linkedin.com/in/johntleonard/)__<br>
__Repo: [JLpyUtils](https://github.com/jlnerd/JLpyUtils)__

Custom modules/classes/methods for various data science, computer vision, and machine learning operations in python
    
## Installing & Importing
In your command line interface (CLI):
```
$ pip install --upgrade JLpyUtils
```
After this, the package can be imported into jupyter notebook or python in general via the comman:
```import JLpyUtils```


# Modules:
```
JLpyUtils.ML
JLpyUtils.plot
JLpyUtils.img
JLpyUtils.video
JLpyUtils.file_utils
JLpyUtils.summary_tables
JLpyUtils.kaggle
```

## Modules Overview

Below, we highlight several of the most interesting modules in more detail.

### JLpyUtils.ML
Machine learning module for python focusing on streamlining and wrapping sklearn, xgboost, dask_ml, & tensorflow/keras functions

__JLpyUtils.ML Sub-Modules:__
```
JLpyUtils.ML.preprocessing 
JLpyUtils.ML.model_selection
JLpyUtils.ML.NeuralNet
JLpyUtils.ML.inspection
JLpyUtils.ML.postprocessing
````

The sub-modules within JLpyUtils.ML are summarized below:

#### JLpyUtils.ML.preprocessing 
Functions related to preprocessing/feature engineering for machine learning

The main class of interest is the ```JLpyUtils.ML.preprocessing.feat_eng_pipe``` class, which iterates through a standard feature engineering sequence and saves the resulting engineered data. The standard sequence is:

1. LabelEncode.categorical_features
2. Scale.continuous_features
    * for Scaler_ID in Scalers_dict.keys()
3. Impute.categorical_features
    * for Imputer_cat_ID in Imputer_categorical_dict[Imputer_cat_ID].keys():<br>
        *for Imputer_iter_class_ID in Imputer_categorical_dict[Imputer_cat_ID].keys():
4. Imputer.continuous_features
    * for Imputer_cont_ID in Imputer_continuous_dict.keys():
        * for Imputer_iter_reg_ID in Imputer_continuous_dict[Imputer_cont_ID].keys():
5. OneHotEncode
6. CorrCoeffThreshold
Finished!
        
#### JLpyUtils.ML.model_selection
Functions/classes for running hyperparameter searches across multiple types of models & comparing those models

The main class of interest is the ```JLpyUtils.ML.model_selection.GridSearchCV``` class, which runs hyperparameter GridSearchCV across different types of models & compares the results to allow one to find the best-of-best (BoB) model. The functions is compatible with evaluating sklearn models, tensorflow/keras models, and xgboost models.

#### JLpyUtils.ML.NeuralNet
sub-modules/functions/classes for streamlining common neural-net architectures implemented in tensorflow/keras.

The most notetable sub-modules are the ```DenseNet``` and ```Conv2D``` modules, which provide a keras implementation of a general dense neural network & 2D convolutional neural network, where the depth & general architecture of the network s are defined by generic hyperparameters, such that one can easily perform a grid search across multiple neural network architectures.

#### JLpyUtils.ML.inspection
Functions to inspect features and/or models after training

#### JLpyUtils.ML.postprocessing
ML model outputs postprocessing helper functions


### JLpyUtils.plot
This module contains helper functions related to common plotting operations via matplotlib.

The most noteable functions are:

```JLpyUtils.plot.corr_matrix()```: Plot a correlation matrix chart

```JLpyUtils.plot.ccorr_pareto()```: Plot a pareto bar-chart for 1 label of interest within a correlation dataframe

```JLpyUtils.plot.hist_or_bar()```: Iterate through each column in a dataframe and plot the histogram or bar chart for the data.

### JLpyUtils.img
This module contains functions/classes related to image analysis, most of which wrap SciKit image functions in some way.

The most noteable functions are: 

```JLpyUtils.img.auto_crop.use_edges()```: Use skimage.feature.canny method to find edges in the image passed and autocrop on the outermost edges

```JLpyUtils.img.decompose_video_to_img()```: Use cv2 to pull out image frames from a video and save them as png files


### JLpyUtils.kaggle
This module contains functions for interacting with kaggle. The simplest and most useful function is:
```
JLpyUtils.kaggle.competition_download_files(competition)
```
where ```competition``` is the competition name, such as  "home-credit-default-risk"

### JLpyUtils.file_utils
This module contains simple but extremely useful helper functions to save and load standard file types including 'hdf', 'csv', 'json', 'dill'. Essentially the ```save``` and ```load``` functions take care of the boiler plate operations related to saving or loading on the file-types specified above.

