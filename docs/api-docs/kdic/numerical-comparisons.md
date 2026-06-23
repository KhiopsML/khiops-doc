# Numerical Comparisons


These rules evaluate numerical expressions and return boolean results encoded as `0` (false) or `1` (true).

**Important notes:**

- The special value `#Missing` represents a missing value and can be used as a numerical operand in any derivation rule.

- When involved in comparisons, `#Missing` is considered inferior to any valid value.

## EQ


```kdic-api-docs
Numerical EQ(Numerical value1, Numerical value2)
```

Equality test between two numerical values.

!!! example

    ```kdic
    Dictionary Person
    {
      Categorical Name;
      Numerical Age;
      // Returns 1 if Age is 18, otherwise returns 0
      Numerical IsAge18 = EQ(Age, 18);
      // Returns 1 if Age is missing, otherwise returns 0
      Numerical IsAgeMissing = EQ(Age, #Missing);  
    }
    ```


## NEQ

```kdic-api-docs
Numerical NEQ(Numerical value1, Numerical value2)
```

Inequality test between two numerical values.

## G

```kdic-api-docs
Numerical G(Numerical value1, Numerical value2)
```

Greater than test between two numerical values.


## GE

```kdic-api-docs
Numerical GE(Numerical value1, Numerical value2)
```

Greater than or equal test between two numerical values.

!!! example

    ```kdic
    Dictionary Person
    {
      Categorical Name;
      Numerical Age;
      // Returns 1 if Age is greater than or equal to 18, otherwise returns 0
      Numerical IsAdult = GE(Age, 18);               
    }
    ```

## L

```kdic-api-docs
Numerical L(Numerical value1, Numerical value2)
```

Less than test between two numerical values.

!!! example

    ```kdic
    Dictionary Person
    {
      Categorical Name;
      Numerical Age;
      // Returns 1 if Age is less than 18 (or missing), otherwise returns 0
      Numerical IsYoungOrMissing = L(Age, 18);               
      // Returns 1 if Age is less than 18 and not missing, otherwise returns 0
      Numerical IsYoung = And(L(Age, 18), NEQ(Age, #Missing)); 
    }
    ```


## LE

```kdic-api-docs
Numerical LE(Numerical value1, Numerical value2)
```

Less than or equal test between two numerical values.


