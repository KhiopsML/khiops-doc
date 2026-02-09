#  View rules

## BuildTableView

```kdic-api-docs
Table(TargetDic) BuildTableView(Table(SourceDic) table)
```

Create a view of the source table in a target table, by selecting a subset of the source variables.

Each native (non-derived) variable in the target table must have the same name and type as in the source table. For each instance in the source table, a target instance is created in the target table by copying the corresponding values from the source instances into the target native variable.

This mechanism is similar to that used to create in-memory instances from records in data files, provided that the variable names match the column names.

Note that you can also have native target variables of type Entity or Table, provided that the related variables are available in the source table.

### Building multiple facets of a table

The `BuildTableView` rule can be used to structure a table into multiple facets. 
This is particularly useful when applying automated multi-table feature engineering, allowing for the construction of deeper features per facet, rather than shallow features for the initial table that contains more secondary variables.

!!! example

    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Numerical age;
      Categorical sex;
      Unused Table(Sale) sales;
      Table(SaleCost) sale_costs = BuildTableView(sales); // View focussed on cost
      Table(SaleDate) sale_dates = BuildTableView(sales); // View focussed on purchase date
    };
    
    Dictionary Sale (customer_id)
    {
      Categorical customer_id;
      Categorical product;
      Numerical cost;
      Date purchase_date;
    };
    
    Dictionary SaleCost
    {
      Categorical product;
      Numerical cost;
    };
    
    Dictionary SaleDate
    {
      Categorical product;
      Date purchase_date;
    };
    ```

### Reusing versus building instances

First, note that in the edge case where the target dictionary used is the same as the source dictionary,
the `BuildTableView` rule creates a table of instances that are identical to the source instances.
However, these target instances are new and distinct from the source ones, similar to how duplicate records in source table files are handled.

This contrasts with [`Table Management Rules`](../kdic/table-management-rules.md), such as
[`TableExtraction`](../kdic/table-management-rules.md/#tableextraction), which reference the entities of the source table.

In the following example, both `BuildTableView` and `TableExtraction` produce similar tables, 
except that the instances output by BuildTableView are new instances, whereas those produced by TableExtraction are the original source instances.

This distinction impacts rules like [`TableUnion`](../kdic/table-management-rules.md/#tableunion), which rely on identifying distinct entities.

!!! example

    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Numerical age;
      Categorical sex;
      Table(Sale) sales;
      Numerical sales_count = TableCount(sales);

      // All sales extracted from the initial table
      Table(Sale) extracted_sales = TableExtraction(sales, 1, TableCount(sales));

      // New sales built from the initial table, which are duplicates of existing sales
      Table(Sale) built_sales = BuildTableView(sales);

      // Union of the initial and extracted sales
      // Its count is the same as sales_count, since the instances are identical
      Table(Sale) initial_and_extracted_sales = TableUnion(sales, extracted_sales);
      Numerical initial_and_extracted_sales_count = TableCount(initial_and_extracted_sales);

      // Union of the initial and built sales
      // Its count is twice that of sales_count, since the instances are new
      Table(Sale) initial_and_built_sales = TableUnion(sales, built_sales);
      Numerical initial_and_built_sales_count = TableCount(initial_and_built_sales);
    };
    
    Dictionary Sale (customer_id)
    {
      Categorical customer_id;
      Categorical product;
      Numerical cost;
      Date purchase_date;
    };
    ```

## BuildTableAdvancedView

```kdic-api-docs
Table(TargetDic) BuildTableAdvancedView(Table(SourceDic) table,
                                        Type1 sourceValue1, Type2 sourceValue2... 
                                        : 
                                        Type1 targetVar1, Type2 targetVar...)
```

This rule extends BuildTableView by allowing you to select a subset of target variables and explicitly specify the source values used to populate each one.

Target variable names are specified after the `:` separator in the rule operands, following the same order as the source values.

Each native target variable must be populated either through the view mechanism, by linking it to a source variable with the same name and type, or by assigning a specific value, either selected or computed from the source instance.

### Merging specific tables in one generic table

In the following example, `BuildTableAdvancedView` is used to merge two specific tables, online and retail sales, into a single generic table, while preserving the sales type in a new variable.

!!! example

    ```kdic
    Root Dictionary Customer (customer_id)
    {
      Categorical customer_id;
      Numerical age;
      Categorical sex;

      // Initial specific tables
      Unused Table(Sale) online_sales; // Online sale from e-commerce
      Unused Table(Sale) retail_sales; // Retail sales from in-stores

      // Build tables, keeping the origin of each instance in the new variable sale_type
      Unused Table(TypedSale) typed_online_sales = BuildTableAdvancedView(online_sales, "online" : sale_type);
      Unused Table(TypedSale) typed_retail_sales = BuildTableAdvancedView(retail_sales, "retail" : sale_type);

      // Resulting generic table, suitable for deeper join analysis
      Table(TypedSale) all_sales = TableUnion(typed_online_sales, typed_retail_sales); // All sales with their type
    };
    
    Dictionary Sale (customer_id)
    {
      Categorical customer_id;
      Categorical product;
      Numerical cost;
      Date purchase_date;
    };
    
    Dictionary TypedSale
    {
      Categorical sale_type; // online or retail
      Categorical product;
      Numerical cost;
      Date purchase_date;
    };
    ```

### Renaming variables using views

The following examples demonstrate different approaches to renaming variables from a source table (in French) to English in the target table.

- Using `BuildTableAdvancedView` to rename variables

- Renaming variables in the source table

- Renaming variables in the target table

!!! example

    === "Using BuildTableAdvancedView to rename variables"
        In this example, each source variable is directly renamed by specifying the target variables in English and populating them from the corresponding French variables.
 
        ```kdic
        Root Dictionary Customer (customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
    
          // Initial table with variables in French
          Unused Table(Vente) sales_in_french;
    
          // New tables with variables in English
          // Each initial variable is renamed using the BuildTableAdvancedView rule
          Table(Sale) sales = BuildTableAdvancedView(sales_in_french,
                                                     customer_id, produit, cout, date_achat:
                                                     customer_id, product, cost, purchase_date);
        };
        
        Dictionary Sale (customer_id)
        {
          Categorical customer_id;
          Categorical product;
          Numerical cost;
          Date purchase_date;
        };
    
        Dictionary Vente (customer_id)
        {
          Categorical customer_id;
          Categorical produit;
          Numerical cout;
          Date date_achat;
        };
        ```

    === "Renaming variables in the source table"
        In this approach, renaming is managed in the source table, and `BuildTableView` selects the renamed variables.
 
        ```kdic
        Root Dictionary Customer (customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
    
          // Initial table with variables in French
          Unused Table(Vente) sales_in_french;
    
          // New tables with variables in English
          // Each variable is renamed in the source table using CopyC, CopyD, etc.
          Table(Sale) sales = BuildTableView(sales_in_french);
        };
        
        Dictionary Sale (customer_id)
        {
          Categorical customer_id;
          Categorical product;
          Numerical cost;
          Date purchase_date;
        };
    
        Dictionary Vente (customer_id)
        {
          Categorical customer_id;
          Categorical produit;
          Numerical cout;
          Date date_achat;

          // Variables are renamed in English
          Categorical product = CopyC(produit);
          Numerical cost = Copy(cout);
          Date purchase_date = CopyD(date_achat);
        };
        ```
    
    === "Renaming variables in the target table"
        Here, the initial variables are selected as unused, and renaming is handled in the target table.
 
        ```kdic
        Root Dictionary Customer (customer_id)
        {
          Categorical customer_id;
          Numerical age;
          Categorical sex;
    
          // Initial table with variables in French
          Unused Table(Vente) sales_in_french;
    
          // New tables with variables in English
          // Each variable is renamed in the target table using CopyC, CopyD, etc.
          Table(Sale) sales = BuildTableView(sales_in_french);
        };
        
        Dictionary Sale (customer_id)
        {
          Categorical customer_id;

          // Renamed variables
          Categorical product = CopyC(produit);
          Numerical cost = Copy(cout);
          Date purchase_date = CopyD(date_achat);
          
          // Variables to retrieve from source table
          Unused Categorical produit;
          Unused Numerical cout;
          Unused Date date_achat;
        };
    
        Dictionary Vente (customer_id)
        {
          Categorical customer_id;
          Categorical produit;
          Numerical cout;
          Date date_achat;
        };
        ```

## BuildEntityView

```kdic-api-docs
Entity(TargetDic) BuildEntityView(Entity(SourceDic) entity)
```

Create a view of the source entity in a target entity, by selecting a subset of the source variables.

This rule is the same as the BuildTableView for a single entity.

## BuildEntityAdvancedView

```kdic-api-docs
Entity (TargetDic) BuildEntityAdvancedView(Entity (SourceDic) table,
                                           Type1 sourceValue1, Type2 sourceValue2...
                                           :
                                           Type1 targetVar1, Type2 targetVar...)
```

This rule extends the BuildEntityView rule by selecting a subset of source variables and explicitly specifying the value of specific target variables.

This rule is the same as the BuildTableAdvancedView for a single entity.

