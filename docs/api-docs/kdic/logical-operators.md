# Logical Operators

These rules use boolean operands (numerical values with 0 for false and not 0 for true) and return
boolean values encoded as 0 or 1 numerical values.

## And

```kdic-api-docs
Numerical And(Numerical boolean1, ...)
```

And logical operator.

## Or

```kdic-api-docs
Numerical Or(Numerical boolean1, ...)
```

Or logical operator.

## Not

```kdic-api-docs
Numerical Not(Numerical boolean)
```

Not logical operator.

## If

```kdic-api-docs
Numerical If(Numerical test, Numerical valueTrue, Numerical valueFalse)
```

Ternary operator returning second operand (true) or third operand (false) according to the
condition in first operand.

## IfC

```kdic-api-docs
Categorical IfC(Numerical test, Categorical valueTrue, Categorical valueFalse)
```

Ternary operator returning second operand (true) or third operand (false) according to the
condition in first operand.

## IfD

```kdic-api-docs
Date IfD(Numerical test, Date valueTrue, Date valueFalse)
```

Ternary operator returning second operand (true) or third operand (false) according to the
condition in first operand.

## IfT

```kdic-api-docs
Time IfT(Numerical test, Time valueTrue, Time valueFalse)
```

Ternary operator returning second operand (true) or third operand (false) according to the
condition in first operand.

## IfTS

```kdic-api-docs
Timestamp IfTS(Numerical test, Timestamp valueTrue, Timestamp valueFalse)
```

Ternary operator returning second operand (true) or third operand (false) according to the
condition in first operand.

## IfTSTZ

```kdic-api-docs
TimestampTZ IfTSTZ(Numerical test, TimestampTZ valueTrue, TimestampTZ valueFalse)
```

Ternary operator returning second operand (true) or third operand (false) according to the
condition in first operand.

## Switch

```kdic-api-docs
Numerical Switch(Numerical test, Numerical valueDefault, Numerical value1, ..., Numerical valueK)
```

Switch operator that returns the numerical value corresponding to the index given by the test
operand if it is between 1 and K. The default value is returned if the index if outside the
bounds.

## SwitchC

```kdic-api-docs
Categorical SwitchC(Numerical test, Categorical valueDefault, Categorical value1, ..., Categorical valueK)
```

Switch operator that returns the categorical value corresponding to the index given by the test
operand if it is between 1 and K. The default value is returned if the index if outside the
bounds.


