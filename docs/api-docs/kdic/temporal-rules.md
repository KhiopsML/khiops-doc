# Temporal rules

## BuildDiffTable

```kdic-api-docs
Table(TargetDic) BuildDiffTable(Table(SourceDic),
                                Type1 Var1, Type1 Var2, ... 
                                : 
                                TargetType1 DiffVar1, TargetType2 DiffVar2, ...)
```

Creation of a target table from a source table, by calculating the differences of values between two consecutive records for a subset of chosen source variables:

- The source table must be sorted according to user needs.

- The source variables Var1, Var2, etc., are specified by the user as those for which the difference is to be calculated.

- The differences are stored in the target table in Numerical target variables named DiffVar1, DiffVar2, etc.

- The calculation of differences depends on the variable type:

    - Numerical, Time, Date, Timestamp, TimestampTZ: difference of values, stored as Numerical in the target variables

    - Categorical: boolean value, with 1 indicating a change in the categorical value

- The target table has the same number of records as the source table. For the first record, the difference variables are set to missing.

- Each native variable in the target table is directly copied from the source table if it has the same name and type, similar to the `BuildTableView` rule.

### Computing a series of temporal differences


!!! example

    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Categorical name;
      Numerical age;
      Table(Sale) sales;
      Unused Table(Sale) sorted_sales = TableSort(sales, purchase_date);
      Table(DiffDateSale) diff_date_sales = BuildDiffTable(sorted_sales, purchase_date : diff_date);
    };
    
    Dictionary Sale (customer_id)
    {
      Categorical customer_id;
      Categorical product;
      Categorical sale_type;
      Numerical cost;
      Date purchase_date;
    };
    
    Dictionary DiffDateSale
    {
      Numerical diff_date; // Calculated by difference of purchase_date with the previous instance
    };
    ```

### Computing a series of differences for all table variables

!!! example

    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Categorical name;
      Numerical age;
      Table(Sale) sales;
      Unused Table(Sale) sorted_sales = TableSort(sales, purchase_date);
      Table(DiffSale) diff_sales = BuildDiffTable(sorted_sales,
                                                  sale_type, cost, purchase_date :
                                                  diff_type, diff_cost, diff_date);
    };
    
    Dictionary Sale (customer_id)
    {
      Categorical customer_id;
      Categorical product;
      Categorical sale_type;
      Numerical cost;
      Date purchase_date;
    };
    
    Dictionary DiffSale
    {
      Categorical sale_type;
      Categorical product;
      Numerical cost;
      Date purchase_date;
      Numerical diff_type; // Set to 1 if sale_type differs from the previous instance, 0 otherwise
      Numerical diff_cost; // Difference of cost with the previous instance
      Numerical diff_date; // Difference of purchase_date with the previous instance
    };
    ```
    