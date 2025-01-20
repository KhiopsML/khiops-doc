# Entity Rules

If the entity does not exists, the rules below return:

- An empty value (`""`) for rules that return `Categorical`
- A missing value for rules that return `Numerical`

## Exist

```kdic-api-docs
Numerical Exist(Entity entityValue)
```

Checks is an entity exists. Returns 0 or 1.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Value is 1 if the address exists for the customer
        Numerical ExistingAddress = Exist(customerAddress);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 1-1 relationship
          Table(Sale) sales;               // 1-n relationship
          // Value is 1 if the address exists for the customer
          Numerical ExistingAddress = Exist(customerAddress);
        };

        Dictionary Address(customer_id)
        {
          Categorical customer_id;
          Categorical street;
          Categorical city;
          Categorical zipcode;
          Categorical State;
        };

        Dictionary Sale(customer_id)
        {
          Categorical customer_id;
          Categorical product;
          Numerical cost;
          Date purchaseDate;
        };
        ```


## GetValue

```kdic-api-docs
Numerical GetValue(Entity entityValue, Numerical value)
```

Access to a `Numerical` value of an entity. Returns a missing value if the entity does not exist.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Street name length
        Numerical streetNameLength = GetValue(customerAddress, Length(street));
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 1-1 relationship
          Table(Sale) sales;               // 1-n relationship
          // Street name length
          Numerical streetNameLength = GetValue(customerAddress, Length(street));
        };

        Dictionary Address(customer_id)
        {
          Categorical customer_id;
          Categorical street;
          Categorical city;
          Categorical zipcode;
          Categorical State;
        };

        Dictionary Sale(customer_id)
        {
          Categorical customer_id;
          Categorical product;
          Numerical cost;
          Date purchaseDate;
        };
        ```


## GetValueC

```kdic-api-docs
Categorical GetValueC(Entity entityValue, Categorical value)
```

Access to a `Categorical` value of an entity. Returns an empty `Categorical` value if the entity
does not exist.

!!! example

    === "Diff from Base Example"
        ```kdic
        Categorical city = GetValueC(customerAddress, city); // City from address
        ```

    === "Full Example"
        ```kdic hl_lines="8"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 1-1 relationship
          Table(Sale) sales;               // 1-n relationship
          Categorical city = GetValueC(customerAddress, city); // City from address
        };

        Dictionary Address(customer_id)
        {
          Categorical customer_id;
          Categorical street;
          Categorical city;
          Categorical zipcode;
          Categorical State;
        };

        Dictionary Sale(customer_id)
        {
          Categorical customer_id;
          Categorical product;
          Numerical cost;
          Date purchaseDate;
        };
        ```

## GetValueD

```kdic-api-docs
Date GetValueD(Entity entityValue, Date value)
```

Access to a `Date` value of an entity. Returns empty `Date` value if the entity does not exist.

## GetValueT

```kdic-api-docs
Time GetValueT(Entity entityValue, Time value)
```

Access to a `Time` value of an entity. Returns an empty `Time` value if the entity does not exist.

## GetValueTS

```kdic-api-docs
Timestamp GetValueTS(Entity entityValue, Timestamp value)
```

Access to a `Timestamp` value of an entity. Returns an empty `Timestamp` value if the entity does
not exist.

## GetValueTSTZ

```kdic-api-docs
TimestampTZ GetValueTSTZ(Entity entityValue, TimestampTZ value)
```

Access to a `TimestampTZ` value of an entity. Returns an empty `TimestampTZ` value if the entity
does not exist.

## GetEntity

```kdic-api-docs
Entity GetEntity(Entity entityValue, Entity value)
```

Access to an `Entity` value of an entity.

## GetTable

```kdic-api-docs
Table GetTable(Entity entityValue, Table value)
```

Access to a `Table` value of an entity.
