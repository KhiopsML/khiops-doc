# Hash Map Rules

## Structure

```kdic-api-docs
Structure(HashMapC) HashMapC(Structure(VectorC) keyVector, Structure(VectorC) valueVector)
```

Builds a hash map of `Categorical` values indexed by `Categorical` keys. The operands must come from
[`VectorC`](vector-rules.md#vectorc) rules of the same size, with unique keys in the
`keyVector`.

## TableHashMapC


```kdic-api-docs
Structure(HashMapC) TableHashMapC(Table table, Categorical key, Categorical value)
```

Builds a hash map of `Categorical` values from keys and values in a table. In case of duplicate keys
in the table, only the first matching value is kept.

## ValueAtKeyC

```kdic-api-docs
Categorical ValueAtKeyC(Structure(HashMapC) hashMap, Categorical key)
```

Returns a value of a categorical hash map at given key. Returns `""` if not found. It allows to
efficiently recode a `Categorical` value into another `Categorical` value.

!!! example

    ```kdic
    Dictionary Person
    {
      Categorical Name;
      Categorical Sex;
      // Maps "male" -> "Mr" and "female" -> "Mrs"
      Categorical Gender =
        ValueAtKeyC(HashMapC(VectorC("male", "female"), VectorC("Mr", "Mrs")), Sex);
    }
    ```

## HashMap

```kdic-api-docs
Structure(HashMap) HashMap(Structure(VectorC) keyVector, Structure(Vector) valueVector)
```

Builds a hash map of numerical values indexed by keys. The operands must be the result of
[`VectorC`](vector-rules.md/#vectorc) and
[`Vector`](vector-rules.md/#vector) rules of the same size, with unique keys in the
vector of keys.

## TableHashMap

```kdic-api-docs
Structure(HashMap) TableHashMap(Table table, Categorical key, Numerical value)
```

Builds a hash map of `Numerical` values from keys and values in a table. In case of duplicate keys
in the table, only the first matching value is kept.

## ValueAtKey

```kdic-api-docs
Numerical ValueAtKey(Structure(HashMap) hashMap, Categorical key)
```

Returns a value of a numerical hash map at given key. Returns missing value is not found. It allows
to efficiently recode a `Categorical` value into a `Numerical` one.

!!! example

    ```kdic
    Dictionary Person
    {
      Categorical Name;
      Categorical Sex;
      // Maps "male" -> 0 and "female" -> 1
      Numerical NumericGender = ValueAtKeyC(HashMapC(VectorC("male", "female"), VectorC(0, 1)), Sex);
    }
    ```

