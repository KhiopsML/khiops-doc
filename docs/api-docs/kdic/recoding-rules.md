# Recoding Rules
Many recoding methods take a partition as a first parameter and a value of the same type (`Numerical`
or `Categorical`) as a second one. They retrieve the part of the partition containing the value,
and output an index, which may be

- an integer value ranging from 1 to S, where S is the partition size,
- or an identifier (like `I1`), which is a generic `Categorical` value,
- or a label (like `]-∞; 2]`), which is a comprehensible `Categorical` value.

## InInterval

```kdic-api-docs
Numerical InInterval(Structure(IntervalBounds) interval, Numerical inputValue)
```

Returns `1` if the input value belongs to the interval, `0` otherwise. The interval bounds must
contain exactly two bounds, for intervals of type `]lowerBound; upperBound]`. For left-open or
right-open intervals, use comparison derivation rules, such as [`G`](numerical-comparisons.md#g),
[`GE`](numerical-comparisons.md#ge), [`L`](numerical-comparisons.md#l) or
[`LE`](numerical-comparisons.md#le).

## InGroup

```kdic-api-docs
Numerical InGroup(Structure(ValueGroup) valueGroup, Categorical inputValue)
```

Returns 1 if the input value belongs to the value group, 0 otherwise.

## CellIndex

```kdic-api-docs
Numerical CellIndex(Structure(DataGrid) dataGrid, SimpleType inputValue1, ...)
```

Computes the `Numerical` cell index of a list of values given a data grid. The list of values are
either numerical `Numerical` or `Categorical` according to the data grid input partition types.

## CellId

```kdic-api-docs
Categorical CellId(Structure(DataGrid) dataGrid, SimpleType inputValue1, ...)
```

Computes the `Categorical` cell identifier of a list of values given a data grid.

## CellLabel

```kdic-api-docs
Categorical CellLabel(Structure(DataGrid) dataGrid, SimpleType inputValue1, ...)
```

Computes the cell label of a list of values given a data grid.

## ValueIndexDG

```kdic-api-docs
Numerical ValueIndexDG(Structure(DataGrid) dataGrid, SimpleType inputValue)
```

Computes the `Numerical` index of a value given a univariate data grid.

## PartIndexAt

```kdic-api-docs
Numerical PartIndexAt(Structure(DataGrid) dataGrid, Numerical index, SimpleType inputValue)
```

Computes the `Numerical` part index of a value given a data grid and an index of dimension in the
data grid. The index must be between 1 and the number of dimension in the data grid, and the value
of the type (Numerical or Categorical) relative to the given dimension of the data grid.

## PartIdAt

```kdic-api-docs
Categorical PartIdAt(Structure(DataGrid) dataGrid, Numerical index, SimpleType inputValue)
```

Computes the categorical part identifier of a value given a data grid and an index of dimension in
the data grid.

## ValueRank

```kdic-api-docs
Numerical ValueRank(Structure(DataGrid) dataGrid, Numerical inputValue)
```

Computes the average normalized rank of a numerical value given a univariate numerical data grid.

## InverseValueRank

```kdic-api-docs
Numerical InverseValueRank(Structure(DataGrid) dataGrid, Numerical inputRank)
```

Computes the average value related to a normalized rank given a univariate numerical data grid.

## DataGridStats

```kdic-api-docs
Structure(DataGridStats) DataGridStats(Structure(DataGrid) dataGrid, SimpleType inputValue1, ...)
```

Computes statistics (conditional probabilities) for a list of values given a data grid. The number
of input values correspond of the inputs variables, which might be inferior to the number of
dimensions in that data grid. The remaining dimensions in the data grid correspond to the output
variables.

## SourceConditionalInfo

```kdic-api-docs
Numerical SourceConditionalInfo(Structure(DataGridStats), Numerical outputIndex)
```

Computes the source conditional info (negative log of the conditional probability) for the input
cell related to the data grids stats and for the index of the target cell of the data grid given as
a parameter (index starts at 1).

## IntervalId

```kdic-api-docs
Categorical IntervalId(Structure(IntervalBounds) intervalBounds, Numerical value)
```

Computes the `Categorical` part identifier of a `Numerical` value given a partition into intervals.

## ValueId

```kdic-api-docs
Categorical ValueId(Structure(ValueSet) values, Numerical value)
```

Computes the `Categorical` part identifier of a `Numerical` value given a partition into a set of
numerical values.

## GroupId

```kdic-api-docs
Categorical GroupId(Structure(ValueGroups) valueGroups, Categorical value)
```

Computes the `Categorical` part identifier of a `Categorical` value given a partition into a set of
groups of categorical values.

## ValueIdC

```kdic-api-docs
Categorical ValueIdC(Structure(ValueSetC) values, Categorical value)
```

Computes the `Categorical` part identifier of a `Categorical` value given a partition into a set of
categorical values. If value is not found in the value set, returns the part identifier of the
special value `*` if it is defined, 1 otherwise.

## IntervalIndex

```kdic-api-docs
Numerical IntervalIndex(Structure(IntervalBounds) intervalBounds, Numerical value)
```

Computes the `Numerical` part index of a `Numerical` value given a partition into intervals.

## ValueIndex

```kdic-api-docs
Numerical ValueIndex(Structure(ValueSet) values, Numerical value)
```

Computes the `Numerical` part index of a `Numerical` value given a partition of numerical value
sets.

## GroupIndex

```kdic-api-docs
Numerical GroupIndex(Structure(ValueGroups) valueGroups, Categorical value)
```

Computes the `Numerical` part index of a `Categorical` value given a partition of groups of
categorical values.

## ValueIndexC

```kdic-api-docs
Numerical ValueIndexC(Structure(ValueSetC) values, Categorical value)
```

Computes the `Numerical` part index of a `Categorical` value given a partition into a set of
`Categorical` values. If the value is not found in the value set, it returns the index of the
special value `*` if it is defined, 1 otherwise.
