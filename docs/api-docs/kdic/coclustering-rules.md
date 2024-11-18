## Coclustering Rules

A coclustering model is stored using a `DataGrid` structure. With a `DataGridDeployment` structure,
it can be deployed on a given dimension variable, for a distribution conditional on the values on
the rest coclustering variables. Other deployment rules can then be used to obtain the closest
part for the deployed variable, the distance to all the other parts on the deployed variable,
and to compute the aggregated frequencies on the parts of all the input variables.

## DataGridDeployment

```kdic-api-docs
Structure(DataGridDeployment) DataGridDeployment(
  Structure(DataGrid) dataGrid, Numerical deployedVariableIndex,
  Vector inputValues1, Vector inputValues2, ..., [Vector inputFrequencies]
)
```

Builds a `DataGridDeployment` structure for a given deployment variable of a data grid. The input
values (`Vector` for `Numerical` values and `VectorC` for `Categorical` values) correspond to the
distribution of the input values. The frequency vector is optional.

## PredictedPartIndex

```kdic-api-docs
Numerical PredictedPartIndex(Structure(DataGridDeployment) DataGridDeployment)
```

Computes the index of the closest part of the deployed variable.

## PredictedPartDistances

```kdic-api-docs
Structure(Vector) PredictedPartDistances(Structure(DataGridDeployment) DataGridDeployment)
```

Computes the distance to all the parts of the deployed variable.

## PredictedPartFrequenciesAt

```kdic-api-docs
Structure(Vector) PredictedPartFrequenciesAt(
  Structure(DataGridDeployment) DataGridDeployment, Numerical inputVariableIndex
)
```

