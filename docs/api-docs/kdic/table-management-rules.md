# Table Management Rules

We modify our `Customer` example by replacing the `sales` table with three tables with the same
`Sale` schema, one for each month from January through March.
```kdic
Root Dictionary Customer(customer_id)
{
  Categorical customer_id;
  Numerical age;
  Categorical sex;
  Entity(Address) customerAddress; // 0-1 relationship
  Table(Sale) salesJanuary;        // 0-n relationship
  Table(Sale) salesFebruary;       // 0-n relationship
  Table(Sale) salesMarch;          // 0-n relationship
};

// the same as the first Customer example
// ...
```


## TableAt

```kdic-api-docs
Entity TableAt(Table table, Numerical rank)
```

Extraction of an entity of a table at a given rank.

!!! example

    === "Delta from the Base Example"
        ```kdic
        Entity(Sale) firstJanuarySale = TableAt(salesJanuary, 1); // First sale of January
        ```

    === "Full Example"
        ```kdic hl_lines="10"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          Entity(Sale) firstJanuarySale = TableAt(salesJanuary, 1); // First sale of January
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



## TableAtKey

```kdic-api-docs
Entity TableAtKey(Table table, Categorical keyField1, Categorical keyField2, ...)
```

Extraction of an entity of a table at a given key. The number of key fields must match that of the
dictionary of the table.

## TableExtraction

```kdic-api-docs
Table TableExtraction(Table table, Numerical firstRank, Numerical lastRank)
```

Extraction of a sub-table containing the entities of the table between `firstRank` and `lastRank`.
Ranks below 1 or beyond the size of the table are ignored.

!!! example

    === "Delta from the Base Example"
        ```kdic
        Table(Sale) firstTenJanuarySales = TableExtraction( salesJanuary, 1, 10 ); // First 10 sales of January
        ```

    === "Full Example"
        ```kdic hl_lines="10"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          Table(Sale) firstTenJanuarySales = TableExtraction(salesJanuary, 1, 10); // First 10 sales of January
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

## TableSelection

```kdic-api-docs
Table TableSelection(Table table, Numerical selectionCriterion)
```

Selection of a sub-table containing the entities of the table that meet the selection criterion.

!!! example

    === "Delta from the Base Example"
        ```kdic
        // January sales for product "Foo"
        Table(Sale) januaryProductFooSales = TableSelection(salesJanuary, EQc(product,”Foo”));
        // Sales for first week of year
        Table(Sale) week1Sales = TableSelection(salesJanuary, LE(YearDay(purchaseDate), 7)));
        ```

    === "Full Example"
        ```kdic hl_lines="10 11"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          // January sales for product "Foo"
          Table(Sale) januaryProductFooSales = TableSelection(salesJanuary, EQc(product,”Foo”));
          // Sales for first week of year
          Table(Sale) week1Sales = TableSelection(salesJanuary, LE(YearDay(purchaseDate), 7)));
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

## TableSelectFirst

```kdic-api-docs
Entity TableSelectFirst(Table table, Numerical selectionCriterion)
```

Return the first entity of the table that meet the selection criterion. It is equivalent to
combining the [`TableSelection`](#tableselection)
and [`TableAt`](#tableat) rules at the first rank.


!!! example

    === "Delta from the Base Example"
        ```kdic
        // First sale among those of the year's first week
        Entity(Sale) firstWeek1Sales = TableSelectFirst( salesJanuary, LE(YearDay(purchaseDate), 7)) );
        ```

    === "Full Example"
        ```kdic hl_lines="10 11"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          // First sale among those of the year's first week
          Entity(Sale) firstWeek1Sales = TableSelectFirst(salesJanuary, LE(YearDay(purchaseDate), 7)));
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


## TableSort

```kdic-api-docs
Table TableSort(Table table, SimpleType sortValue1, SimpleType sortValue2, ...)
```

Sorts a table by increasing order according to a list of one to many sort values. Each sort value is
of type `Numerical`, `Categorical`, `Time`, `Date`, `Timestamp` or `TimestampTZ`, and can be either
a native table variable or the result of a rule.

## EntitySet

```kdic-api-docs
Table EntitySet(Entity entity1, Entity entity2, ...)
```

Builds a table from a set of entities. All the entities in the operands must have the same
`Dictionary` definition; the result table will also have the same `Dictionary` definition.


!!! example

    === "Delta from the Base Example"
        ```kdic
        // Sales table for the first quarter
        Table(Sale) salesSamples = EntitySet(
          TableAt(salesJanuary, 1), TableAt(salesFebruary, 1), TableAt(salesMarch, 1)
        );
        ```

    === "Full Example"
        ```kdic hl_lines="10"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          // Sales table for the first quarter
          Table(Sale) salesSamples = EntitySet(
            TableAt(salesJanuary, 1), TableAt(salesFebruary, 1), TableAt(salesMarch, 1)
          );
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

## TableUnion

```kdic-api-docs
Table TableUnion(Table table1, Table table2, ...)
```

Union of a set of tables. The union table contains the entities that belong to one of the table
operands.

!!! example

    === "Delta from the Base Example"
        ```kdic
        // Sales table for the first quarter
        Table(Sale) salesQuarter1 = TableUnion(salesJanuary, salesFebruary, salesMarch);
        ```

    === "Full Example"
        ```kdic hl_lines="10 11"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          // Sales table for the first quarter
          Table(Sale) salesQuarter1 = TableUnion(salesJanuary, salesFebruary, salesMarch);
          );
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

## TableIntersection

```kdic-api-docs
Table TableIntersection(Table table1, Table table2, ...)
```

Intersection of a set of tables. The intersection table contains the entities that belong to all the table operands.


!!! example

    === "Delta from the Base Example"
        ```kdic
        // Sales of the first quarter
        Table(Sale) salesQuarter1 = TableUnion(salesJanuary, salesFebruary, salesMarch);
        // January sales (same as salesJanuary)
        Table(Sale) salesMonth1 = TableIntersection(salesJanuary, salesQuarter1);
        ```

    === "Full Example"
        ```kdic hl_lines="10 11 12"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          // Sales of the first quarter
          Table(Sale) salesQuarter1 = TableUnion(salesJanuary, salesFebruary, salesMarch);
          // January sales (same as salesJanuary)
          Table(Sale) salesMonth1 = TableIntersection(salesJanuary, salesQuarter1);
          );
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


## TableDifference

```kdic-api-docs
Table TableDifference(Table table1, Table table2)
```

Difference between two tables. The difference table contains the entities that belong to either of the two table operands, but not to their intersection.

!!! example

    === "Delta from the Base Example"
        ```kdic
        // Sales table for months 1 and 2
        Table(Sale) salesMonth1and2 = TableUnion(salesJanuary, salesFebruary);
        // Sales table for months 2 and 3
        Table(Sale) salesMonth2and3 = TableUnion(salesFebruary, salesMarch);
        // Sales table for the first and the third month
        // Note that this is the same as TableUnion(salesJanuary, salesFebruary)
        Table(Sale) salesMonth2and3 = TableDifference(salesMonth1and2, salesMonth2and3);
        ```

    === "Full Example"
        ```kdic hl_lines="10-16"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) salesJanuary;        // 0-n relationship
          Table(Sale) salesFebruary;       // 0-n relationship
          Table(Sale) salesMarch;          // 0-n relationship
          // Sales table for months 1 and 2
          Table(Sale) salesMonth1and2 = TableUnion(salesJanuary, salesFebruary);
          // Sales table for months 2 and 3
          Table(Sale) salesMonth2and3 = TableUnion(salesFebruary, salesMarch);
          // Sales table for the first and the third month
          // Note that this is the same as TableUnion(salesJanuary, salesFebruary)
          Table(Sale) salesMonth2and3 = TableDifference(salesMonth1and2, salesMonth2and3);
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


## TableSubUnion

```kdic-api-docs
Table TableSubUnion(Table table, Table subTable)
```


Union of the sub-tables of a table. This applies in the case of a snowflake schema.

!!! example
    For this example we use a different and slightly more complex version of the `Customer`
    database, specifically we have the following schema
    ```
    Customer
    |
    +--0-n-- Service
    |        |
    |        +--0-n-- Usage
    |
    +--0-1-- Address
    ```
    So we have a Customer that has signed up for one or more services. For each service, the
    customer may have one or more usages. The customer has a unique address as before.

    We use the `TableSubUnion` rule to obtain all usages for a given customer.


    ```kdic hl_lines="7-8"
    Root Dictionary Customer(id_customer)
    {
      Categorical id_customer;
      Categorical Name;
      Table(Service) Services;
      Entity(Address) Address;
      // Table of all usages for all services
      Table(Usage) allUsages = TableSubUnion(services, usages);
    };

    Dictionary Address(id_customer)
    {
      Categorical id_customer;
      Numerical StreetNumber;
      Categorical StreetName;
      Categorical id_city;
    };

    Dictionary Service(id_customer, id_product)
    {
      Categorical id_customer;
      Categorical id_product;
      Date SubscriptionDate;
      Table(Usage) Usages;
    };

    Dictionary Usage(id_customer, id_product)
    {
      Categorical id_customer;
      Categorical id_product;
      Date Date;
      Time Time;
      Numerical Duration;
    };
    ```


## TableSubIntersection

```kdic-api-docs
Table TableSubIntersection(Table table, Table subTable)
```

Intersection of the sub-tables of a table.
