# Technical Structures

This section summarizes the derivation rules that are used internally by Khiops to:

- store data preparation and predictor models in dictionary files, and
- to compute any model output values such as variable recoding, prediction, density estimation.

The aim of this section is to enable a quick understanding of these rules: **it is not intended to
be used by the user to construct new variables**.

## Overview

Khiops exploits several technical types to store the results of data preparation and modeling into
dictionaries:

- Vectors:
    - `Structure(VectorC)`: `Categorical` values vector.
    - `Structure(Vector)`: `Numerical` values vector.
- Hash Maps:
    - `Structure(HashMapC)`: `Categorical` values hash map.
    - `Structure(HashMap)`: `Numerical` values hash map.
- Data Preparation:
    - `Structure(DataGrid)`: A data grid is defined by its input partitions (discretizations or value
      groupings) and by the frequencies of the cells of the cross-product of the input partitions.
    - Partitions:
        - `Structure(IntervalBounds)`: `Numerical` partition, defined by a sorted list of interval
          bounds.
        - `Structure(ValueGroups)`: `Categorical` partition, defined by a set of exclusive groups of
          values (`Structure(ValueGroup)`).
        - `Structure(ValueGroup)`: Set of exclusive categorical values.
        - `Structure(ValueSet)`: `Numerical` partition, defined by a set of exclusive numerical values.
        - `Structure(ValueSetC)`: `Categorical` partition, defined by a set of exclusive categorical
          values.
    - `Structure(Frequencies)`: Frequency vector.
- Data Preparation Statistics:
    - `Structure(DataGridStats)`: The `DataGridStats` structure is defined by a data grid and a set
      a variables related to the input partitions of the data grid; the statistics are computed with
      respect to the data grid cell related to the input values.
- Predictors:
    - `Structure(Classifier)`: Classifier specification.
    - `Structure(Regressor)`: Regressor specification.
    - `Structure(RankRegressor)`: Rank regressor specification.
- Coclustering Deployment:
  - `Structure(DataGridDeployment)`: The `DataGridDeployment` structure is defined by a data grid,
    the index of the deployed variable and a set a vectors of values (`Vector` and `VectorC`) for
    each input partitions of the data grid except the deployed variable, plus an optional vector of
    frequencies; this structure provides predictions related to the deployed variable, given the
    input distribution of the other variables.