# Math Rules

Most of these rules return a numerical value from operators having one or many numerical operands.
When one operand is missing or invalid, the result is missing.

## FormatNumerical

```kdic-api-docs
Categorical FormatNumerical(Numerical value, Numerical width, Numerical precision)
```

Returns a string formatted version of a numerical value, with given minimum digit number before
separator and given precision after separator.

!!! example

    ```kdic
    FormatNumerical(3.141592, 0, 8) // 3.14159200
    FormatNumerical(3.141592, 2, 5) // 03.14159
    FormatNumerical(3.141592, 0, 0) // 3
    ```

## Sum

```kdic-api-docs
Numerical Sum(Numerical value1, ...)
```

Sum of numerical values.

## Minus

```kdic-api-docs
Numerical Minus(Numerical value)
```

Opposite value.

## Diff

```kdic-api-docs
Numerical Diff(Numerical value1, Numerical value2)
```

Difference between two numerical values.

## Product

```kdic-api-docs
Numerical Product(Numerical value1, ...)
```

Product of numerical values.

## Divide

```kdic-api-docs
Numerical Divide(Numerical value1, Numerical value2)
```

Ratio of two numerical values.

## Index

```kdic-api-docs
Numerical Index()
```

Integer index related to the line number of the current record from a data file (start at 1).

## Random

```kdic-api-docs
Numerical Random()
```

Random number between 0 and 1.

Each time a database is read, the random seed is forced to the same value, such that the sequence of
random numbers will be the same.

Note that the Random rule can be used several times in dictionaries, resulting in independent
sequences of random numbers.

## Round

```kdic-api-docs
Numerical Round(Numerical value)
```

Closest integer value.

## Floor

```kdic-api-docs
Numerical Floor(Numerical value)
```

Largest previous integer value.

## Ceil

```kdic-api-docs
Numerical Ceil(Numerical value)
```

Smallest following integer value.

## Abs

```kdic-api-docs
Numerical Abs(Numerical value)
```

Absolute value.

## Sign

```kdic-api-docs
Numerical Sign(Numerical value)
```

Sign of a numerical value.

Returns 1 for values greater or equal than 0, -1 for values less than 0.

## Mod

```kdic-api-docs
Numerical Mod(Numerical value1, Numerical value2)
```

Returns value1 mod value2. Precisely, `value1 – value2 * Floor(value1/value2)`.

## Log

```kdic-api-docs
Numerical Log(Numerical value)
```

Natural logarithm.

## Exp

```kdic-api-docs
Numerical Exp(Numerical value)
```

Exponential value.

## Power

```kdic-api-docs
Numerical Power(Numerical value1, Numerical value2)
```

Power function.

## Sqrt

```kdic-api-docs
Numerical Sqrt(Numerical value)
```

Square root function.

## Sin

```kdic-api-docs
Numerical Sin(Numerical value)
```

Sine function.

## Cos

```kdic-api-docs
Numerical Cos(Numerical value)
```

Cosine function.

## Tan

```kdic-api-docs
Numerical Tan(Numerical value)
```

Tangent function.

## ASin

```kdic-api-docs
Numerical ASin(Numerical value)
```

Arc-sine function.

## ACos

```kdic-api-docs
Numerical ACos(Numerical value)
```

Arc-cosine function.

## ATan

```kdic-api-docs
Numerical ATan(Numerical value)
```

Arc-tangent function.

## Pi

```kdic-api-docs
Numerical Pi()
```

Pi constant.

## Mean

```kdic-api-docs
Numerical Mean(Numerical value1, ...)
```

Mean of numerical values.

## StdDev

```kdic-api-docs
Numerical StdDev(Numerical value1, ...)
```

Standard deviation of numerical values.

## Min

```kdic-api-docs
Numerical Min(Numerical value1, ...)
```

Min of numerical values (among non-missing values).

## Max

```kdic-api-docs
Numerical Max(Numerical value1, ...)
```

Max of numerical values (among non-missing values).

## ArgMin

```kdic-api-docs
Numerical ArgMin(Numerical value1, ...)
```

Index of the min value in a numerical series. The index starts at 1 and relates to the first value
that is equal to the min.

## ArgMax

```kdic-api-docs
Numerical ArgMax(Numerical value1, ...)
```

Index of the max value in a numerical series. The index starts at 1 and relates to the first value
that is equal to the max.

