# Reinforcement Rules

The reinforcement rules exploit a set of lever variables among the variables of a classifier to
improve prediction scores.


## ClassifierReinforcer

```kdic-api-docs
Structure(ClassifierReinforcer) ClassifierReinforcer(Structure(Classifier), 
                                                     Structure(VectorC) leverVariableNames)
```

Builds a `ClassifierReinforcer` structure from a `Classifier` structure and a list of lever variables, provided as literal values.
The resulting `ClassifierReinforcer` contains all the necessary information
to compute reinforcement scores for each lever variable and target value.

## ReinforcementInitialScoreAt

```kdic-api-docs
Numerical ReinforcementInitialScoreAt(Structure(ClassifierReinforcer), Categorical targetValue)
```

Returns the initial prediction score for the prediction of a given target value.


## ReinforcementVariableAt

```kdic-api-docs
Categorical ContributionVariableAt(Structure(ClassifierReinforcer),
                                   Categorical targetValue, Numerical rank)
```

Returns the name of the lever variable at the specified reinforcement rank (starting at 1) for a target value,
based on lever variables ordered by decreasing reinforcement scores.


## ReinforcementPartAt

```kdic-api-docs
Categorical ReinforcementPartAt(Structure(ClassifierReinforcer),
                                Categorical targetValue, Numerical rank)
```

Returns the label of the lever variable part at the specified reinforcement rank (starting at 1) for a target value,
based on lever variables ordered by decreasing reinforcement scores.


## ReinforcementFinalScoreAt

```kdic-api-docs
Numerical ReinforcementFinalScoreAt(Structure(ClassifierReinforcer),
                                    Categorical targetValue, Numerical rank)
```

Returns the final score after reinforcement at the specified reinforcement rank (starting at 1) for a target value,
based on lever variables ordered by decreasing reinforcement scores.

## ReinforcementClassChangeTagAt

```kdic-api-docs
Numerical ReinforcementFinalScoreAt(Structure(ClassifierReinforcer),
                                    Categorical targetValue, Numerical rank)
```

Returns the class change tag after reinforcement at the specified reinforcement rank (starting at 1) for a target value,
based on lever variables ordered by decreasing reinforcement scores:

- 0 indicates the initial predicted target value was already the target to reinforce,

- -1 indicates the final predicted target value remains different from the target to reinforce,

- 1 indicates the final predicted target value is now the target to reinforce.


