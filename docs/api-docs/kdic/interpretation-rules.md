# Interpretation Rules

The interpretation rules allow to calculates the individual importance of classifier variables using 
[Shapley values:octicons-link-external-16:][shapley-values]{:target="_blank"}.

[shapley-values]: https://en.wikipedia.org/wiki/Shapley_value "Visit the Wikipedia page"


## ClassifierInterpreter

```kdic-api-docs
Structure(ClassifierInterpreter) ClassifierInterpreter(Structure(Classifier))
```

Builds a `ClassifierInterpreter` structure from a `Classifier` structure.
The resulting `ClassifierInterpreter` contains all the necessary information
to derive interpretation indicators for each classifier variable and target value.

## ContributionAt

```kdic-api-docs
Numerical ContributionAt(Structure(ClassifierInterpreter), 
                         Categorical targetValue, Categorical classifierVariableName)
```

Retuns the Shapley value for a given target value and classifier variable.


## ContributionVariableAt

```kdic-api-docs
Categorical ContributionVariableAt(Structure(ClassifierInterpreter),
                                   Categorical targetValue, Numerical rank)
```

Returns the name of the variable at the specified importance rank (starting at 1) for a target value,
based on variables ordered by decreasing Shapley values.

## ContributionPartAt

```kdic-api-docs
Categorical ContributionPartAt(Structure(ClassifierInterpreter), 
                               Categorical targetValue, Numerical rank)
```

Returns the label of the variable part at the specified importance rank (starting at 1) for a target value,
based on variables ordered by decreasing Shapley values.

## ContributionValueAt

```kdic-api-docs
Numerical ContributionValueAt(Structure(ClassifierInterpreter),
                              Categorical targetValue, Numerical rank)
```

Returns the Shapley value at the specified importance rank (starting at 1) for a target value,
based on variables ordered by decreasing Shapley values.
