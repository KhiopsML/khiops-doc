# Predictor Rules

## NBClassifier

```kdic-api-docs
Structure(Classifier) NBClassifier(Structure(DataGridStats) dataGridStats1, ...)
```

Builds a Naive Bayes `Classifier` structure from a set of data grids stats that encode the target
conditional probabilities. Each data grid stats results from a preparation model (data grid) and
input values, which allows the computation of conditional probabilities.

## SNBClassifier

```kdic-api-docs
Structure(Classifier) SNBClassifier(
  Structure(Vector) variableWeights, Structure(DataGridStats) dataGridStats1, ...
)
```
Builds a Selective Naive Bayes `Classifier` structure. The first parameter is weight
[`Vector`](vector-rules.md/#vector) for the selected variables. The remaining parameters are the
same as for the [`NBClassifier`](#nbclassifier) rule.


## TargetValue

```kdic-api-docs
Categorical TargetValue(Structure(Classifier) classifier)
```

Computes a `Classifier`'s most probable target value.

## TargetProb

```kdic-api-docs
Numerical TargetProb(Structure(Classifier) classifier)
```

Computes the `Classifier`s probability of the most probable target value.

## TargetProbAt

```kdic-api-docs
Numerical TargetProbAt(Structure(Classifier) classifier, Categorical targetValue)
```

Computes the `Classifier` probability (score) of a given target value.

## BiasedTargetValue

```kdic-api-docs
Categorical BiasedTargetValue(Structure(Classifier) classifier, Structure(Vector) biasValues)
```

Computes the `Classifier` highest score target value, after adding a bias to each initial target
value score.

## NBRankRegressor

```kdic-api-docs
Structure(RankRegressor) NBRankRegressor(Structure(DataGridStats) dataGridStats1, ...)
```

Builds a Naive Bayes `RankRegressor` structure from a set of data grids stats.

## SNBRankRegressor

```kdic-api-docs
Structure(RankRegressor) SNBRankRegressor(
  Structure(Vector) variableWeights, Structure(DataGridStats) dataGridStats1, ...
)
```

Builds a Selective Naive Bayes `RankRegressor`. The first parameter is weight
[`Vector`](vector-rules.md/#vector) for the selected variables. The remaining parameters are the
same as for the [`NBRankRegressor`](#nbrankregressor) rule.


## TargetRankMean

```kdic-api-docs
Numerical TargetRankMean(Structure(RankRegressor) rankRegressor)
```

Computes the `RankRegressor` target rank mean.

## TargetRankStandardDeviation

```kdic-api-docs
Numerical TargetRankStandardDeviation(Structure(RankRegressor) rankRegressor)
```

Computes the `RankRegressor` target rank's standard deviation.

## TargetRankDensityAt

```kdic-api-docs
Numerical TargetRankDensityAt(Structure(RankRegressor) rankRegressor, Numerical rank)
```

Computes the `RankRegressor` density of the target rank for a given normalized rank (between 0 and
1).

## TargetRankCumulativeProbAt

```kdic-api-docs
Numerical TargetRankCumulativeProbAt(Structure(RankRegressor) rankRegressor, Numerical rank)
```

Computes the `RankRegressor` probability that the target rank is below a given normalized rank.


## NBRegressor

```kdic-api-docs
Structure(Regressor) NBRegressor(
  Structure(RankRegressor) nbRankRegressor, Structure(DataGrid) targetValues
)
```

Builds a Naive Bayes `Regressor` structure. The first parameter is a Naive Bayes `RankRegressor`.
The second parameter is the distribution of the numerical target values, encoded as a univariate
numerical data grid based on a vector of values partition.

## SNBRegressor

```kdic-api-docs
Structure(Regressor) SNBRegressor(
  Structure(RankRegressor) snbRankRegressor, Structure(DataGrid) targetValues
)
```

Builds a Selective Naive Bayes `Regressor` structure from a `RankRegressor`.The first parameter is
a Naive Bayes `RankRegressor`. The second parameter is the distribution of the numerical target
values, encoded as a univariate numerical data grid based on a vector of values partition.



## TargetMean

```kdic-api-docs
Numerical TargetMean(Structure(Regressor) regressor)
```

Computes the `Regressor` mean target value.

## TargetStandardDeviation

```kdic-api-docs
Numerical TargetStandardDeviation(Structure(Regressor) regressor)
```

Computes the `Regressor` standard deviation of the target value.

## TargetDensityAt

```kdic-api-docs
Numerical TargetDensityAt(Structure(Regressor) regressor, Numerical value)
```

Computes the `Regressor` density of the target for a given value.
