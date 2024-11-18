## DataGrid

```kdic-api-docs
Structure(DataGrid) DataGrid(Structure(Partition) partition1, ..., Structure(Frequencies))
```

Builds a `DataGrid` structure.

The first parameters are partitions: the results of the rules [`IntervalBounds`](#intervalbounds),
[`ValueGroups`](#valuegroups), [`ValueSetC`](#valuesetc) or [`ValueSet`](#valueset). The last
argument are the data grid cell frequencies.

!!! example

    The following contingency table (a two-dimensional data grid)

    | Interval      | Iris-setosa | Iris-versicolor | Iris-virginica |
    | :-----------: | :---------: | :-------------: | :------------: |
    | `]-inf;0.75]` | 38          | 0               | 0              |
    | `]0.75;1.55]` | 0           | 33              | 0              |
    | `]1.55;+inf[` | 0           | 3               | 34             |

    is encoded in a dictionary using a constructed variable:

    ```kdic
    Dictionary Example
    {
      Structure(DataGrid) PPetalWidth = DataGrid(
        IntervalBounds(0.75, 1.55),
        ValueSetC("Iris-setosa", "Iris-versicolor", "Iris-virginica"),
        Frequencies(38, 0, 0, 0, 33, 3, 0, 0, 34)
      );
    };
    ```

    The cells are indexed column-first. In this example, contingency table indexation is as follows:

    | Interval      | Iris-setosa | Iris-versicolor | Iris-virginica |
    | :-----------: | :---------: | :-------------: | :------------: |
    | `]-inf;0.75]` | 1           | 4               | 7              |
    | `]0.75;1.55]` | 2           | 5               | 8              |
    | `]1.55;+inf]` | 3           | 6               | 9              |

    Several derivation rules use a data grid structure to retrieve a cell given a vector of input
    values. For example, the vector of values `(1.1, "Iris-versicolor")` falls into the cell of
    index 5.

    The value vector can be partially complete. In this case, the other dimension has default values
    corresponding to the first part of their dimension. For example, the single value vector `(1.1)`
    falls into the cell of index 2.

    The value types can be either `Numerical` or `Categorical` according to the data grid input
    partition types. In the following, this will be indicated using `SimpleType` for such parameter
    types.

## IntervalBounds

```kdic-api-docs
Structure(IntervalBounds) IntervalBounds(Numerical bound1, ...)
```

Builds a partition into interval.

## ValueGroup

```kdic-api-docs
Structure(ValueGroup) ValueGroup(Categorical value1, ...)
```

Builds a group of values. The special value `*` cannot correspond to a value extracted from datasets
(these ones are trimmed before being processed). This special value can be used as a "garbage value"
to match any value that are not explicitly defined elsewhere.

## ValueGroups

```kdic-api-docs
Structure(ValueGroups) ValueGroups(Structure(ValueGroup) valueGroup1, ...)
```

Builds a partition into groups of values. The special value `*` must be defined in exactly one value
group, which is assigned to unknown values.

## ValueSetC

```kdic-api-docs
Structure(ValueSetC) ValueSetC(Categorical value1, ...)
```

Builds a partition into categorical values.

## ValueSet

```kdic-api-docs
Structure(ValueSet) ValueSet(Numerical value1, ...)
```

Builds a partition into numerical values.

## Frequencies

```kdic-api-docs
Structure(Frequencies) Frequencies(Numerical frequency1, ...)
```

Builds a vector of frequencies.
