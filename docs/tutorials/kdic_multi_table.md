This section introduces the use of Khiops dictionaries for **managing data preparation with multi-table datasets**, a frequent scenario in real-world business applications. Khiops eliminates the need for labor-intensive preprocessing and manual handling of relationships between tables, offering a scalable and automated solution for relational data. For full documentation, please refer to the dictionaries [reference page][reference_page]. 

[reference_page]:../api-docs/kdic/numerical-comparisons.md


## Relational Data Description 

When working with relational (multi-table) data, a key step is defining relationships between tables and their respective variables. Traditional libraries require manual table joins, ad hoc data management, and domain expertise to prepare data for analysis. This is time-consuming, prone to errors, and becomes infeasible for large scale datasets (which occurs more rapidly with such multi-table datasets).

Khiops uses a dictionary-based language that **naturally describes the relational schema** without flattening the data. Relationships between tables are encoded directly in the dictionary, enabling efficient and interpretable processing. Key benefits include:

- **Scalability**: Process large datasets without loading tables into memory, leveraging I/O optimizations, out-of-core and distributed processing.
- **Streamlined Versioning**: End-to-end data transformations are recorded in the dictionary, eliminating the need for versioning large intermediary datasets.

### Simple Star Relational Schema

Let's start by a example of a star schema describing a company’s customers, their addresses, and the services they use:

```
    Customer
    |
    |-- Address 
    |
    |-- Services 
```
`Customer` designates the data type of the main statistical units studied, `Address` and `Services` correspond to the types of their secondary records. 

The corresponding Khiops dictionary will be:
 
!!! success "Example: Dictionary for a star schema"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Entity(Address) customerAddress; // 0-1 relationship
        Table(Services) customerServices;               // 0-N relationship
    };

    Dictionary Address (customer_id)
    {
        Categorical customer_id;
        Categorical streetNumber;
        Categorical streetName;
        Categorical city;
        Categorical zipcode;
        Categorical State;
    };

    Dictionary Services (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical cost;
        Date purchaseDate;
    };
    ```

In this example:

- Each `Dictionary` corresponds to a user-defined data structure (`Customer`, `Address`, `Services`), effectively serving as a data type; 
- The categorical variable `customer_id` acts as the key, uniquely identifying the statistical units in the main table (i.e., `Customer`) and linking their associated records in the secondary tables (i.e., `Services` and `Address`). 
- `Entity(Address)` designates a 0-1 relationship (e.g., each customer has **one** address **or none**).   
- `Table(Services)` designates a 0-N relationship (e.g., each customer can have multiple services). Each statistical unit in the main table `Customer` refers to a table of records in the secondary table `Services`.  


### Snowflake Relational Schema

This example extends the previous star schema by introducing a snowflake relational schema, where secondary tables are expanded with additional hierarchical levels. In this case, the schema includes a new `Usages` table, which describes how customers use specific `Services`.

 
```
    Customer
    |
    |-- Address
    |
    |-- Services
        |
        |-- Usages
``` 

Note that a customer can use each service several times (relation 0-N). This additional complexity reflects real-world scenarios, such as tracking multiple transactions or interactions linked to a single entity.

Here's the dictionary file describing this relational data:

!!! success "Example: Dictionary file of a snowflake relational schema"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Entity(Address) customerAddress; // 0-1 relationship
        Table(Services) customerServices;               // 0-N relationship
    };

    Dictionary Address (customer_id)
    {
        Categorical customer_id;
        Categorical streetNumber;
        Categorical streetName;
        Categorical city;
        Categorical zipcode;
        Categorical State;
    };

    Dictionary	Services	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;	
        Categorical name;	
        Numerical cost;
        Date purchaseDate;	
        Table(Usages)	serviceUsages;	      // 0-n relationship
    };

    Dictionary	Usages	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;
        Categorical usageType;	
        Date	date;	
        Time	time;	
        Numerical	duration;	
    };
    ```

The only new syntax feature in this example is the use of **a multiple-field key** in the `Services` and `Usages` dictionaries. These keys allow Khiops to efficiently associate multiple levels of data, such as linking usage records to specific services used by specific customers. As the number of table levels increases in a snowflake schema, the identification key becomes longer, consisting of a concatenation of multiple identifier variables (e.g., customer_id and service_id).

This structure enables **hierarchical feature engineering**. For example, Khiops can calculate aggregates like “Total usage duration per customer” by traversing multiple levels. 

### Snowflake Schema with External Tables 

This example introduces the concept of an external table. **External tables** are used to enrich descriptive variables in other tables without duplicating information. Unlike standard secondary tables, external tables are not directly linked to the main statistical units (e.g., `customer_id`) but instead provide additional descriptive information for a specific variable. 

For instance, the `City` table in the following schema adds information such as the city name, country, and time zone to the `Address` table, without repeating the same city details across multiple rows. Instead, the `Address` table references the `City` table using the `zipcode` key. This approach ensures efficiency and consistency, especially in large scale datasets.

The relational schema is structured as follows:
```
    Customer
    |
    |-- Address
    |   |
    |   |-- City
    |
    |-- Services
        |
        |-- Usages
``` 

Here’s the dictionary file that defines this relational schema:

!!! success "Example: Dictionary file for a snowflake schema with an external table"
    ```kdic
    Root Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Entity(Address) customerAddress;    // 0-1 relationship
        Table(Services) services;            // 0-n relationship
    };

    Dictionary Address (customer_id)
    {
        Categorical customer_id;
        Categorical streetNumber;
        Categorical streetName;
        Categorical zipcode;
        Entity(City) city[zipcode];	
    };

    Root	Dictionary	City	(zipcode)
    {
	    Categorical	zipcode;	
	    Categorical	name;	
	    Categorical	country;	
	    Categorical timeZone;	
    };

    Dictionary	Services	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;	
        Categorical name;	
        Numerical cost;
        Date purchaseDate;	
        Table(Usage)	Usages;	 // 0-n relationship
    };

    Dictionary	Usage	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;
        Categorical usageType;	
        Date	date;	
        Time	time;	
        Numerical	duration;	
    };
    ```

An external table **behaves like an Entity**, creating a 0-1 relationship. The syntax starts with `Entity(City)`. And because it provides additional information for a specific descriptive variable rather than statistical units, square brackets `[zipcode]` are used to specify the linking key.

The `Root` keyword is required for external tables, as it indicates that the key variable (e.g., zipcode) uniquely identifies the records in that table.

## Filtering Out-of-scope Tables and Variables

In data management, defining the scope of an analysis is crucial to focus on the most relevant information while avoiding the overhead of processing unnecessary data. For multi-table datasets, this involves filtering out tables and variables that do not contribute to the analysis.

With conventional tools, data scientists often load entire datasets into memory before manually discarding irrelevant variables or tables. This approach is manageable for small datasets but becomes inefficient and costly for larger, multi-table datasets. It can also lead to excessive trial-and-error runs, creating versioning challenges and increasing storage costs, especially in cloud environments.

Khiops dictionaries provide a more efficient solution by enabling on-the-fly filtering. Only the relevant columns and tables are loaded into memory during processing. This eliminates unnecessary overhead and makes dictionaries lightweight and easy to version, offering a scalable alternative for industrial use cases.

The `Unused` keyword in Khiops dictionaries allows you to specify variables and tables that should be excluded from analysis. Here’s an example:
 
!!! success "Example: Filtering with the Unused keyword"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
    Unused    Entity(Address) customerAddress; // Unused entity
        Table(Services) customerServices;               
    };    

    Dictionary Address (customer_id)
    {
        Categorical customer_id;
        Categorical streetNumber;
        Categorical streetName;
        Categorical city;
        Categorical zipcode;
        Categorical State;
    };

    Dictionary Services (customer_id)
    {
        Categorical customer_id;
        Categorical name;
    Unused    Numerical cost; // Unused variable
        Date purchaseDate;
    };
    ```

## User-defined Relational Schema

In many cases, databases are designed with technical constraints in mind (e.g., optimizing query speed or storage efficiency), often at the expense of usability for business experts. As a result, the stored data can be difficult to interpret or align with the experts’ knowledge of the problem. Reorganizing this data to better reflect the business context is a critical step in data management.

Traditionally, this process involves manually coding project-specific data management workflows—a time-consuming and error-prone task, compounded by the challenges of versioning multiple scripts and iterations.

Khiops dictionaries offer a powerful alternative. By using their built-in data manipulation language (see the [reference page][reference_page]), you can streamline this process and encode business knowledge directly into a reusable, versionable format. This not only simplifies data management but also ensures alignment between technical implementation and business understanding.
 
The next three subsections illustrate how dictionaries can facilitate data manipulation through:

- Redefining the scope of statistical units;
- Concatenating tables;
- Advanced selection of training examples.

### Redefining the scope of statistical units

In many real-world applications, the statistical units of interest are not directly stored in the database and need to be derived from raw data. For instance, it may be necessary to eliminate noisy or insignificant records to focus on meaningful information. This process is essential for reducing complexity, saving computational resources, and ensuring the analysis is targeted.

Khiops makes this process seamless using the `TableSelection` function, which allows you to filter secondary records based on specified criteria, directly within the dictionary. This eliminates the need for pre-processing steps in Python or SQL, enabling scalable and efficient data management.

**Example 1: Filter by Duration of Use**
 
The following example redefines the scope of statistical units by selecting only the records in the `Usage` table where the duration exceeds ten minutes `(GE(duration,10))`:

!!! success "The TableSelection function applied to secondary records"
    ```kdic
    Root Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Table(Services) services;            
    };

    Dictionary	Services	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;	
        Categorical name;	
        Numerical cost;
        Date purchaseDate;	
    Unused    Table(Usage)	allServiceUsages;	

        // selection of usages > 10 minutes
        Table(Usage)	studiedUsages = TableSelection(allServiceUsages, GE(duration,10));	 
    };

    Dictionary	Usage	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;
        Categorical usageType;	
        Date	date;	
        Time	time;	
        Numerical	duration;	
    };
    ```

This command identifies and retains only the relevant records from the Usage table, streamlining the analysis process by discarding unnecessary data.

Notice that in the rule `TableSelection(.,.)`, the first operand designates the name of a table and the second operand is a selection rule applied in the scope of this table. 

**Example 2: Filter by Time Relative to a Parent Variable**

In more advanced scenarios, filtering may require conditions that depend on variables from a parent table. For instance, the following example filters records from the `Usage` table to include only those occurring within 30 days of the `purchaseDate` from the `Services` table:  

!!! success "The . scope operator"
    ```kdic
    Root Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Table(Services) services;            
    };

    Dictionary	Services	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;	
        Categorical name;	
        Numerical cost;
        Date purchaseDate;	
    Unused    Table(Usage)	allServiceUsages;

        // selection of usages within 30 days after subscription
        Table(Usage)	studiedUsages = TableSelection(allServiceUsages, LE(DiffDate(date, .purchaseDate),30));	 
    };

    Dictionary	Usage	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;
        Categorical usageType;	
        Date	date;	
        Time	time;	
        Numerical	duration;	
    };
    ```

In this example, the second operand in the rule `LE(DiffDate(date, .purchaseDate), 30)` operates within the scope of the `Usage` dictionary, where it directly uses the `date` variable. It also accesses the `purchaseDate` variable from the parent `Services` dictionary using the `.` scope operator to establish the relationship between the two tables.

### Table concatenation

In many production environments, large data tables are often divided into multiple chunks for easier storage and management. This is especially common for secondary tables with a high volume of records, such as log data or transactional details. While this practice improves storage efficiency and system performance, it introduces the challenge of reconstructing the original table for analysis or model training.

Khiops provides an efficient solution for this scenario through the `TableUnion` rule, which allows you to seamlessly concatenate these chunks. In the example below, `Usage` table is divided into quarterly chunks (`usagesQuarter1`, `usagesQuarter2`, etc.). These chunks are unified into a single table using `TableUnion`. To prevent duplicates during analysis, the `Unused` keyword is applied to each chunk sub-table, as the concatenated table already contains all the records.

!!! success "The TableUnion function"
    ```kdic
    Root Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Table(Services) services;            
    };

    Dictionary	Services	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;	
        Categorical name;	
        Numerical cost;
        Date purchaseDate;	
    Unused    Table(Usage)	usagesQuarter1; 
    Unused    Table(Usage)	usagesQuarter2;
    Unused    Table(Usage)	usagesQuarter3;
    Unused    Table(Usage)	usagesQuarter4;	  

        // concatenation of 4 files, divided for volume purposes
    Unused Table(Usage)	allUsages = TableUnion(usagesQuarter1, usagesQuarter2, usagesQuarter3, usagesQuarter4);	 
    
        // selection of usages > 10 minutes
        Table(Usage)	studiedUsages = TableSelection(allServiceUsages, GE(duration,10));	 
    };

    Dictionary	Usage	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;
        Categorical usageType;	
        Date	date;	
        Time	time;	
        Numerical	duration;	
    };
    ```

## Advanced Example Selection 

The selection of training examples is an important step in data management, enabling the scope of the analysis to be defined. In the case of multi-table data, this step can become complex, requiring laborious manual work and coding. Here again, dictionaries offer an effective alternative, and greatly facilitate versioning. 

The following example shows the selection of a particular marketing segment consisting of housewives under 50 who have used the VOD service at least 10 times. As this selection criterion is complex, it is written on several lines:

- **line 1:** selection of customers < 50 years old  
- **line 2:** selection of women
- **line 3:** selection of services that are both (i) VOD and (ii) with more than 10 uses

For full documentation on dictionary language, please refer to the [reference page][reference_page]. 

!!! success "Complex criteria for selecting examples"
    ```kdic
    Root Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Table(Services) services;            

        // Selection of housewives under 50 who have used VOD at least 10 times.
        // This complex selection criterion is written on several lines:
        // - line 1: selection of customers < 50 years old  
        // - line 2: selection of women
        // - line 3: selection of services that are both 
        // -- VOD
        // -- and with more than 10 uses

    Unused Numerical selectionVariable = And(LE(age,50),   
                                            EQc(sex,"F"),
                                            EQ(TableCount(TableSelection(services, 
                                                                            And(EQc(name,"VOD"), 
                                                                                GE(TableCount(allServiceUsages),10))))
                                                ,1)
                                            );     
    };

    Dictionary	Services	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;	
        Categorical name;	
        Numerical cost;
        Date purchaseDate;	
        Table(Usage)	allServiceUsages;	         
    };

    Dictionary	Usage	(customer_id, service_id)
    {
        Categorical	customer_id;	
        Categorical	service_id;
        Categorical usageType;	
        Date	date;	
        Time	time;	
        Numerical	duration;	
    };
    ```

