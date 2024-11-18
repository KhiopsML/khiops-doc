# Data Copy and Conversion

## Copy

```kdic-api-docs
Numerical Copy(Numerical value)
```

Copy of a numerical value. Allows to rename a variable.

## CopyC

```kdic-api-docs
Categorical CopyC(Categorical value)
```

Copy of a categorical value.

## CopyD

```kdic-api-docs
Date CopyD(Date value)
```

Copy of a date value.

## CopyT

```kdic-api-docs
Time CopyT(Time value)
```

Copy of a time value.

## CopyTS

```kdic-api-docs
Timestamp CopyTS(Timestamp value)
```

Copy of a timestamp value.

## CopyTSTZ

```kdic-api-docs
TimestampTZ CopyTSTZ(Timestamp value)
```

Copy of a timestampTZ value.

## AsNumerical

```kdic-api-docs
Numerical AsNumerical(Categorical value)
```

Conversion of a categorical value to a numerical value. If the value to be converted is a numerical
value, the rule returns the converted value. If the input value is missing or is not a numerical
value, the method returns the system missing value.

## AsNumericalError

```kdic-api-docs
Categorical AsNumericalError(Categorical value)
```

Label of a conversion error when converting a categorical value to a numerical value. This rule
allows to analyse the missing or erroneous values of a numerical variable. This can be done by using
a categorical type for the numerical variable to analyse, then by creating a derived variable with
the current derivation rules. Thus, statistics on missing or erroneous values can easily be
collected.

List of conversion errors:

- Unconverted end of string
- Underflow
- Overflow `-inf`
- Overflow `+inf`
- Conversion `OK`

## RecodeMissing

```kdic-api-docs
Numerical RecodeMissing(Numerical inputValue, Numerical replaceValue)
```

Returns the input value if it is different from the missing value and the replace value otherwise.

## AsCategorical

```kdic-api-docs
Categorical AsCategorical(Numerical value)
```

Conversion of a numerical value to a categorical value. This allows to process the input numerical
values as unordered categorical values, and thus to analyse the variable using a value grouping
method rather than a discretization method.
