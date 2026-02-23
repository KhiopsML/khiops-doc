# Basic building rules

## BuildEntity

```kdic-api-docs
Entity (TargetDic) BuildEntity(Type1 sourceValue1, Type2 sourceValue2... 
                               :
                               Type1 targetVar1, Type2 targetVar...)
```

Creation of an entity by explicitly specifying the value of the target variables.

- Each native (non-derived) target variable must be filled by a source value

- The target variable names are specified after the `:` separator in the rule operands.

### Creating a structured schema from raw data

In the following example, all customer-related data is stored in a single file.
Using the `BuildEntity` rule, the main Customer entity is structured more clearly, with address-related fields stored in a secondary instance with a 0-1 relationship.

!!! example

    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Categorical name;
      Numerical age;
      Unused Categorical customer_street;
      Unused Categorical customer_city;
      Unused Categorical customer_zipcode;
      Unused Categorical customer_State;

      // Entity created from the customer values
      // The values of the target variables street, city, zipcode, State are filled
      // from the Customer's related variables.
      Entity(Address) customerAddress = BuildEntity(customer_street, customer_city,
                                                    customer_zipcode, customer_State :
                                                    street, city, zipcode, State);
    };
    
    Dictionary Address
    {
      Categorical street;
      Categorical city;
      Categorical zipcode;
      Categorical State;
    };
    ```

Note that, as usual, the Address target dictionary may contain unused variables or, conversely, new variables derived from others.

### Building a time series table from a list of fields

In the following example, the input data table contains unstructured purchase data represented as a list of fields.
Using the `BuildEntity` rule, this unstructured data is transformed into a structured list of purchase instances, which supports advanced data analysis such as easy aggregation and time series analysis, through automatic feature construction.

!!! example

    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Categorical name;
      Numerical age;
    
      // Monthly purchase fields
      // Add more months as needed
      Unused Numerical purchase_january;
      Unused Numerical purchase_february;
      Unused Numerical purchase_march;

      // Build a Purchase entity for each monthly purchase
      Entity(Purchase) purchaseJanuary = BuildEntity(AsDate("2026-01-01", "YYYY-MM-DD"), purchase_january : date, amount);
      Entity(Purchase) purchaseFebruary = BuildEntity(AsDate("2026-02-01", "YYYY-MM-DD"), purchase_february : date, amount);
      Entity(Purchase) purchaseMarch = BuildEntity(AsDate("2026-03-01", "YYYY-MM-DD"), purchase_march : date, amount);

      // Build a Table from all monthly purchases
      Table(Purchase) purchaseSeries = EntitySet(purchaseJanuary, purchaseFebruary, purchaseMarch);
    };

    Dictionary Purchase
    {
      Date date;
      Numerical amount;
    };
    ```

## BuildCompositeTable

```kdic-api-docs
Table(TargetDic) BuildCompositeTable(Table(SourceDic1) sourceTable1, Table(SourceDic2) sourceTable2, ...
                                     :
                                     Entity(SourceDic1) outputEntity1, Entity(SourceDic2) outputEntity2, ...)
```

Creation of a composite target table from multiple source tables.

- The function takes a list of tables as input.

- It produces a single target table where each row contains corresponding instances from each source table.

- If source input tables have different sizes, missing entries coming from the shortest source tables are handled as missing values.

- The target table can include derived variables that extract specific parts of each source entity, enabling the construction of a comprehensive, conflict-free view.

- This approach allows combining multiple alternative representations (e.g., of a time series) into a single, cohesive table.

!!! example


    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Categorical name;
      Numerical age;
      Table(Sale) sales;

      // Sorted sales table based on purchase date
      Unused Table(Sale) sorted_sales = TableSort(sales, purchase_date);

      // Table of differences in purchase dates
      Table(DiffDateSale) diff_date_sales = BuildDiffTable(sorted_sales, purchase_date : diff_date);

      // Composite table combining sorted sales and diff dates
      Table(InfosSale) info_sales = BuildCompositeTable(sorted_sales, diff_date_sales : sale, diff_date_sale);
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
      Numerical diff_date; // Difference in days from previous purchase
    };

    Dictionary InfosSale
    {
      // Unused entities filled from BuildDiffTable, necessary for computing the derived variables
      Unused Entity(Sale) sale;
      Unused Entity(DiffDateSale) diff_date_sale;

      // Derived variables
      Categorical sale_type = GetValueC(sale, sale_type);
      Numerical cost = GetValue(sale, cost);
      Date purchase_date = GetValueD(sale, purchase_date);
      Numerical diff_date = GetValue(diff_date_sale, diff_date);
    };
    ```