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

## BuildTemporalJoin

```kdic-api-docs
Table(TargetDic) BuildTemporalJoin(Table(SourceDic) sourceTable, TemporalType sourceTime,
                                   Table(HistoricalDic) historicalTable, TemporalType historicalTime,
                                   Numerical periodStart, Numerical periodEnd
                                   :
                                   Entity(SourceDic) outputSourceEntity,
                                   Entity(HistoricalDic) outputHistoricalEntity)
```

For each source-table instance, finds the closest instance in the historical table whose temporal
value falls within the specified period relative to the source instance. At most one historical
instance is selected per source instance.

- `sourceTime` and `historicalTime` are evaluated in their respective table dictionaries and must have
  the same type: `Numerical`, `Date`, `Time`, `Timestamp`, or `TimestampTZ`. Their difference
  (`historicalTime - sourceTime`) is measured in days for `Date`, seconds for `Time`, `Timestamp`, and
  `TimestampTZ`, and as the numerical difference for `Numerical`.

- `periodStart` and `periodEnd` must be non-missing numerical constants satisfying
  `periodStart <= periodEnd`. They define inclusive offsets relative to `sourceTime`, in the
  corresponding distance unit. A historical instance is eligible when its difference from the source
  instance is within these bounds.

- Neither input table needs to be sorted. The rule selects the eligible instance with the smallest
  absolute difference. If candidates are equally distant, it selects the earlier temporal value;
  if their temporal values are equal, it selects the one that appeared first in the historical table.
  Historical instances with missing temporal values are ignored; a source instance with a missing
  temporal value has no match.

- The output contains one newly created instance per source-table instance, in the same order.
  `outputSourceEntity` refers to the original source instance; `outputHistoricalEntity` refers to the
  selected historical instance, or is missing if there is no match. The same historical instance can
  match several source instances.

- The target table has two native `Entity` variables, whose names are specified after the `:` separator
  as `outputSourceEntity` and `outputHistoricalEntity`. It can include additional derived variables
  that extract or combine information from both instances.

### Matching purchases with recent credit assessments

For each customer, this example links every purchase to the closest credit assessment recorded on
or before the purchase date, within the preceding 30 days. A derived variable combines both dates
to measure the number of days between assessment and purchase. If no assessment falls in the period,
the `assessment` entity is missing.

!!! example

    ```kdic
    Root Dictionary Customer(customer_id)
    {
      Categorical customer_id;
      Categorical name;
      Table(Purchase) purchases; // Customer's purchases
      Table(CreditAssessment) credit_assessments; // Customer's assessment history

      // Match each purchase to the closest assessment in the preceding 30 days
      Table(PurchaseWithAssessment) purchases_with_assessment = BuildTemporalJoin(purchases, purchase_date,
                                                                                  credit_assessments, assessment_date,
                                                                                  -30, 0
                                                                                  : purchase, assessment);
    };

    Dictionary Purchase(customer_id)
    {
      Categorical customer_id;
      Date purchase_date; // Source temporal variable
      Numerical amount;
    };

    Dictionary CreditAssessment(customer_id)
    {
      Categorical customer_id;
      Date assessment_date; // Historical temporal variable
      Numerical credit_score;
    };

    Dictionary PurchaseWithAssessment
    {
      Unused Entity(Purchase) purchase; // Original purchase
      Unused Entity(CreditAssessment) assessment; // Closest matching history, if any
      Numerical amount = GetValue(purchase, amount);
      Numerical credit_score = GetValue(assessment, credit_score);
      Numerical days_since_assessment = DiffDate(GetValueD(purchase, purchase_date),
                                                 GetValueD(assessment, assessment_date)); // Days from assessment to purchase
    };
    ```
