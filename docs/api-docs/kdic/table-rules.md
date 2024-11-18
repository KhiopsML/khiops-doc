# Table Rules
Table rules return an empty (categorical) or missing (numerical) value when the table is empty.

If the table is empty, the rules below return:

- An empty value (`""`) for rules that return `Categorical`
- A missing value for rules that return `Numerical`

## TableCount

```kdic-api-docs
Numerical TableCount(Table table)
```

Size of a table.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Number of sales for a customer
        Numerical saleNumber = TableCount(sales);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Number of sales for a customer
          Numerical saleNumber = TableCount(sales);
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



## TableCountDistinct

```kdic-api-docs
Numerical TableCountDistinct(Table table, Categorical value)
```

Number of distinct values for a `Categorical` value in a table. A missing value is considered as
a special value (empty) and counted as well.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Number of different products in a customer's sales
        Numerical saleProductNumber = TableCountDistinct(sales, product);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Number of different products in customer's sales
          Numerical saleProductNumber = TableCountDistinct(sales, product);
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



## TableEntropy

```kdic-api-docs
Numerical TableEntropy(Table table, Categorical value)
```

Entropy of a `Categorical` value in a table. The entropy of a categorical value is analogous to the
variance of a `Numerical` value. It is large in case of all values having the same frequency in the
table, and small in the case of few frequent values.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Entropy of the distribution of products of a customer's sales
        Numerical saleProductEntropy = TableEntropy(sales, product);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Entropy of the distribution of products of a customer's sales
          Numerical saleProductEntropy = TableEntropy(sales, product);
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


## TableMode

```kdic-api-docs
Categorical TableMode(Table table, Categorical value)
```


Most frequent value for a `Categorical` value in a table. In case of ties in frequency, the method
returns the first value by lexicographic order.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Most frequent product in a customer's sales
        Categorical saleMainProduct = TableMode(sales, product);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Most frequent product in a customer's sales
          Categorical saleMainProduct = TableMode(sales, product);
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


## TableModeAt

```kdic-api-docs
Categorical TableModeAt(Table table, Categorical value, Numerical rank)
```

N-th most frequent value for a `Categorical` value in a table. Returns an empty value for ranks
beyond the number of different values.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Second most frequent product in a customer's sales
        Categorical saleSecondMainProduct = TableModeAt(sales, product, 2);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Second most frequent product in a customer's sales
          Categorical saleSecondMainProduct = TableModeAt(sales, product, 2);
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

## TableMean

```kdic-api-docs
Numerical TableMean(Table table, Numerical value)
```

Mean of numerical values in a table.

This rule (and the other similar ones) takes only the non missing values into account. Its returns missing if the table is empty or if all the values are missing.


!!! example

    === "Diff from Base Example"
        ```kdic
        // Mean product cost for a customer's sales
        Numerical saleMeanCost = TableMean(sales, cost);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Mean product cost for a customer's sales
          Numerical saleMeanCost = TableMean(sales, cost);
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


## TableStdDev

```kdic-api-docs
Numerical TableStdDev(Table table, Numerical value)
```

Standard deviation of numerical values in a table.


!!! example

    === "Diff from Base Example"
        ```kdic
        // Standard deviation of product costs for a customer's sales
        Numerical saleStdDevCost = TableStdDev(sales, cost);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Standard deviation of product costs for a customer's sales
          Numerical saleStdDevCost = TableStdDev(sales, cost);
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


## TableMedian

```kdic-api-docs
Numerical TableMedian(Table table, Numerical value)
```

Median of numerical values in a table.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Cost standard deviation for a customer's sales
        Numerical saleMedianCost = TableMedian(sales, cost);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Cost standard deviation for a customer's sales
          Numerical saleStdDevCost = TableStdDev(sales, cost);
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

## TableMin

```kdic-api-docs
Numerical TableMin(Table table, Numerical value)
```

Min of numerical values in a table.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Mininum product cost for a customer's sales
        Numerical saleMinCost = TableMin(sales, cost);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Mininum product cost for a customer's sales
          Numerical saleMinCost = TableMin(sales, cost);
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


## TableMax

```kdic-api-docs
Numerical TableMax(Table table, Numerical value)
```

Max of numerical values in a table.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Maximum product cost for a customer's sales
        Numerical saleMaxCost = TableMax(sales, cost);
        // Year's day of last purchase in sales
        Numerical saleLastYearDay = TableMax(sales, YearDay(purchaseDate));
        ```

    === "Full Example"
        ```kdic hl_lines="8-11"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Maximum product cost for a customer's sales
          Numerical saleMaxCost = TableMax(sales, cost);
          // Year's day of last customer sale
          Numerical saleLastYearDay = TableMax(sales, YearDay(purchaseDate));
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


## TableSum

```kdic-api-docs
Numerical TableSum(Table table, Numerical value)
```

Sum of numerical values in a table.

!!! example

    === "Diff from Base Example"
        ```kdic
        // Total cost of a customer's sales
        Numerical saleTotalCost = TableSum(sales, cost);
        ```

    === "Full Example"
        ```kdic hl_lines="8-9"
        Root Dictionary Customer(customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
          Entity(Address) customerAddress; // 0-1 relationship
          Table(Sale) sales;               // 0-n relationship
          // Total cost of a customer's sales
          Numerical saleTotalCost = TableSum(sales, cost);
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
