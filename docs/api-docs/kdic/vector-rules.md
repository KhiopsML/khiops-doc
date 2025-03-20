# Vector Rules

## VectorC

```kdic-api-docs
Structure(VectorC) VectorC(Categorical value1, ...)
```

Builds a vector of `Categorical` values. The operands must be literal values (no variables or
rules).

## TableVectorC

```kdic-api-docs
Structure(VectorC) TableVectorC(Table table, Categorical value)
```

Builds a vector of `Categorical` values from values in a table.

## ValueAtC

```kdic-api-docs
Categorical ValueAtC(Structure(VectorC) vector, Numerical index)
```

Returns a value of a `Categorical` vector at given index (index starts at 1). Returns `""` if the
index is out of bounds.

## Vector

```kdic-api-docs
Structure(Vector) Vector(Numerical value1, ...)
```

Builds a vector of `Numerical` values. The operands must be literal values (no variables or rules).

## TableVector

```kdic-api-docs
Structure(Vector) TableVector(Table table, Numerical value)
```

Builds a vector of `Numerical` values from values in a table.

## ValueAt

```kdic-api-docs
Numerical ValueAt(Structure(Vector) vector, Numerical index)
```

Returns the value of a `Numerical` vector at given index (indexes starts at 1). Returns a missing
value if the index is out of bounds.
