# Preparation Sparse Rules

These rules extend the [`Data Preparation`](data-preparation-rules.md) and [`Recoding`](recoding-rules.md) rule to blocks of variables, 
in order to get a sparse block of prepared variables from a sparse block of variables.
This is achieved by applying the definition of all the necessary data preparation models for the entire block.

## DataGridBlock

```kdic-api-docs
Structure(DataGridBlock) DataGridBlock(Structure(ValueSet) varKeys, 
                                       Structure(DataGrid) dataGrid1, ...)
```

Builds a `DataGridBlock` structure from a list of VarKeys and a list a data grids, each corresponding to a specific preparation model.
The number of VarKeys in the first operand must match the number of data grids provided, with each VarKey identifying the data grid at the corresponding position.
The VarKeys can be either integers, represented using a ValueSet structure, or alphanumeric values represented using a ValueSetC structure.

## DataGridStatsBlock

```kdic-api-docs
Structure(DataGridStatsBlock) DataGridStatsBlock(Structure(DataGridBlock) dataGridBlock, 
                                                 Block(Numerical) valueBlock)
```

Builds a `DataGridStatsBlock` structure from a `DataGridBlock` structure and a block of variables, which can be
either Numerical variables (`Block(Numerical)`) or Categorical variables (`Block(Categorical)`).

The `VarKeys` used in both operands must be of the same type, either all integers or all alphanumerical values.
All VarKeys in the block of variables to be prepared must be present in the first operand, 
to retrieve the corresponding data grid model.
The output of this rule is a sparse block containing prepared statistics for each variable, 
similar to the [`DataGridStats`](recoding-rules.md#datagridstats) rule in the case of dense variables.

## DataGridCellBlock

```kdic-api-docs
Block(Numerical) DataGridCellBlock(Structure(DataGridBlock) dataGridBlock, Block(Numerical) valueBlock)
```

Builds a numerical block from a `DataGridBlock` structure and a block of variables, which can be
either Numerical variables (`Block(Numerical)`) or Categorical variables (`Block(Categorical)`).
The constraints are the same as for the [`DataGridStatsBlock`](preparation-sparse-rules.md) rule.
The output of this rule is a sparse block of numerical indices for each variable, 
similar to the [`CellIndex`](recoding-rules.md#cellindex) rule in the case of dense variables.


