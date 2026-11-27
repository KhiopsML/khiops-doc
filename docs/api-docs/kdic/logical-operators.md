# Logical Operators

These operators always return `0` (false) or `1` (true), even if an operand is missing (unlike most derivation rules). Operands are normally the results of [comparison rules](numerical-comparisons.md), but any Numerical value is accepted, as in many programming languages: zero is false and any non-zero value, including a missing value, is true (so `Not(#Missing)` returns `0`).

To treat missing values differently, use `EQ(value, #Missing)` or [`RecodeMissing`](data-copy-and-conversion.md#recodemissing).

## And

```kdic-api-docs
Numerical And(Numerical boolean1, ...)
```

And logical operator.

!!! example

    ```kdic
    Dictionary Person
    {
      Categorical Name;
      Numerical Age;
      Categorical City;
      // Returns 1 if Age is less than 18 (or missing) and City is "New York", otherwise returns 0
      Numerical IsSelected1 = And(L(Age, 18), EQ(City, "New York"));
      // Returns 1 if Age is less than 18 and not missing and City is "New York", otherwise returns 0
      Numerical IsSelected2 = And(And(L(Age, 18), NEQ(Age, #Missing)), EQ(City, "New York"));
      // Returns 1 if Age is missing and City is "New York", otherwise returns 0
      Numerical IsSelected3 = And(EQ(Age, #Missing), EQ(City, "New York"));
    }
    ```

## Or

```kdic-api-docs
Numerical Or(Numerical boolean1, ...)
```

Or logical operator.

!!! example

    ```kdic
    Dictionary Person
    {
      Categorical Name;
      Numerical Age;
      Categorical City;
      // Returns 1 if Age is less than 18 (or missing) or City is "New York", otherwise returns 0
      Numerical IsSelected1 = Or(L(Age, 18), EQ(City, "New York"));
      // Returns 1 if Age is less than 18 and not missing, or City is "New York", otherwise returns 0
      Numerical IsSelected2 = Or(And(L(Age, 18), NEQ(Age, #Missing)), EQ(City, "New York"));
      // Returns 1 if Age is missing or City is "New York", otherwise returns 0
      Numerical IsSelected3 = Or(EQ(Age, #Missing), EQ(City, "New York"));
    }
    ```


## Not

```kdic-api-docs
Numerical Not(Numerical boolean)
```

Not logical operator.

## If

```kdic-api-docs
Numerical If(Numerical test, Numerical valueTrue, Numerical valueFalse)
```

Ternary operator returning the second operand (`valueTrue`) or the third operand (`valueFalse`) according to the
condition in the first operand. The condition follows the same convention as the logical operators: zero is false and any non-zero value, including a missing value, is true.

## IfC

```kdic-api-docs
Categorical IfC(Numerical test, Categorical valueTrue, Categorical valueFalse)
```

Ternary operator returning the second operand (`valueTrue`) or the third operand (`valueFalse`) according to the
condition in the first operand.

## IfD

```kdic-api-docs
Date IfD(Numerical test, Date valueTrue, Date valueFalse)
```

Ternary operator returning the second operand (`valueTrue`) or the third operand (`valueFalse`) according to the
condition in the first operand.

## IfT

```kdic-api-docs
Time IfT(Numerical test, Time valueTrue, Time valueFalse)
```

Ternary operator returning the second operand (`valueTrue`) or the third operand (`valueFalse`) according to the
condition in the first operand.

## IfTS

```kdic-api-docs
Timestamp IfTS(Numerical test, Timestamp valueTrue, Timestamp valueFalse)
```

Ternary operator returning the second operand (`valueTrue`) or the third operand (`valueFalse`) according to the
condition in the first operand.

## IfTSTZ

```kdic-api-docs
TimestampTZ IfTSTZ(Numerical test, TimestampTZ valueTrue, TimestampTZ valueFalse)
```

Ternary operator returning the second operand (`valueTrue`) or the third operand (`valueFalse`) according to the
condition in the first operand.


## IfText

```kdic-api-docs
Text IfText(Numerical test, Text valueTrue, Text valueFalse)
```

Ternary operator returning the second operand (`valueTrue`) or the third operand (`valueFalse`) according to the
condition in the first operand.

## Switch

```kdic-api-docs
Numerical Switch(Numerical test, Numerical valueDefault, Numerical value1, ..., Numerical valueK)
```

Switch operator that returns the numerical value corresponding to the index given by the test
operand if it is between 1 and K. The default value is returned if the index is outside the
bounds, or if it is missing.

## SwitchC

```kdic-api-docs
Categorical SwitchC(Numerical test, Categorical valueDefault, Categorical value1, ..., Categorical valueK)
```

Switch operator that returns the categorical value corresponding to the index given by the test
operand if it is between 1 and K. The default value is returned if the index is outside the
bounds, or if it is missing.


