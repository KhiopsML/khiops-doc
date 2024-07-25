
This section introduces the use of dictionaries to easily implement the data-management steps of a typical datascience project, where the training set consists of a multi-table data. For full documentation, please refer to the dictionaries [reference page][reference_page]. 

[reference_page]:../api-docs/kdic/numerical-comparisons.md


## Data Description 

The first data management step in a datascience project handling relational (or multi-table) data is to describe the different tables and how they are linked together. The types of variables in each table must also be described.  

When using the conventional tools, data scientists load each data table in memory into a Pandas Dataframe or equivalent, and then model the links between tables by specific code. For each project, the user must perform ad hoc data-management (e.g. table joins) ahead of the feature engineering step, which requires time and expertise. 

Compared with single-table data, multi-table data is much more complex, since it contains detailed information (e.g. call reports from a cell phone operator's customers). In an industrial context, multi-table data is often extremely large, making in-memory processing almost impossible with conventional tools. The costs are prohibitive, in terms of engineering, development time and hardware resources. 

Khiops offers a truly scalable alternative which avoids the loading of tables into memory. The dictionary exhaustively describes the multi-table data, as well as the data transformation steps required by the user. Data is then processed as it is read from the hard disk, with strategies for managing very large volumes of data, including I/O optimization, out-of-core processing and distributed processing.

Thanks to Khiops, the usually high cost of data management disappears, and versioning is greatly facilitated. In fact, dictionaries encode end-to-end data transformation flows, from user data description, through Auto Feature Engineering, to final target modeling.

The following sections introduce the syntax required to describe multi-table data in a disctionary file. Simple relational shemas are introduced first, and the examples shown become progressively richer.   

### Simple Star Relational Schema

This first example shows a star schema describing a company's customers. 
`Customer` designates the data type of the main statistical units studied, `Address` and `Services` correspond to the types of their secondary records. 
```
    Customer
    |
    |-- Address 
    |
    |-- Services 
```

Note that a customer has only one address, which may be missing (relation 0:1), and has zero or several services (relation 0:n).
Here's the dictionnary file describing this relational data:
 
!!! success "Dictionary file of a star schema"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Entity(Address) customerAddress; // 0-1 relationship
        Table(Services) customerServices;               // 0-n relationship
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

The important syntax elements for understanding this dictionary file are as follows: 

- Each `Dictionary` corresponds to a user-defined data structure (i.e. Customer, Address, Services) which can be considered as a data type. 
- The categorical variable `customer_id` takes on the role of a key identifying both the statistical units in the main table (i.e. customers) and the records in the secondary tables associated with each statistical unit (i.e. a customer's services and address). 
- `Entity(dictionaryName)` designates a 0-1 relationship between the table where it is used (i.e. Customer) and the records of a secondary table whose structure is described by the `dictionaryName` dictionary. In the case of a 0-N relationship, each statistical unit in the origin table (i.e. Customer) links to a single record in the secondary table (i.e. customerAddress).  
- `Table(dictionaryName)` designates a 0-N relationship between the statistical units of the table where it is used (i.e. Customer) and the records of a secondary table whose structure is described by the `dictionaryName` dictionary. In the case of a 0-N relationship, each statistical unit in the origin table (i.e. Customer) refers a table of records in the secondary table (i.e. customerServices).  


### Snowfalke Relational Schema

This second example presents a snowflake relational schema, which unlike star schemas, has several levels of secondary tables. This example is very similar to the previous one, with the additional type `Usages` describing each customer's use of a particular service:   
```
    Customer
    |
    |-- Address
    |
    |-- Services
        |
        |-- Usages
``` 

Note that a customer can use the same service several times (relation 0:n). 
Here's the dictionnary file describing this relational data:

!!! success "Dictionary file of a snowfalke relational schema"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Numerical age;
        Categorical sex;
        Categorical marketingSegment;
        Entity(Address) customerAddress; // 0-1 relationship
        Table(Services) customerServices;               // 0-n relationship
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

The only new syntax feature is that **several keys** are used in the `Services` and `Usages` dictionaries, in order to identify the usage array linked to a particular service that is used by a particular customer. Finally, as the number of secondary table levels increases in a snowflake schema, the identification key becomes longer and is made up of the concatenation of multiple identifier variables (i.e. customer_id and service_id). 

### Snowfalke Schema with External Tables 

This third example, similar to the previous one, adds an external table whose type is `City`, allowing the `Adress` type to be completed with information specific to the city (e.g. the time zone). The relational schema considered is represented as follows:   
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

As this is an external table, cities can appear in multiple customer addresses. The information contained in an external table does not relate to the main statistical units (i.e. customers) but completes a descriptive variable (i.e. cities). Finally, the customer addresses refer the city information based on the zip-code, without the need to duplicate the information describing the cities. Here's the dictionnary file describing this relational data: 

!!! success "Snowfalke schemal with external table"
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

Here, the new syntax feature is the **declaration of an external table** which is a kind of `Entity`, since it implies a 0-1 relation. This declaration takes the following form: `Entity(dictionaryName) variableName[id_variable]`. Where the identifier variable is added in square brackets juste after the name of the created variable. In our example, `zipcode` is a variable of type `Address` which takes on the role of the city identifier key. Finally, the declaration in our example is `Entity(City) city[zipcode]`. 

The `ROOT` keyword is also needed to declare an external table, as it indicates that the key variable (i.e. zipcode) **uniquely** identifies the records.
It is also advisable to add this keyword to the main table, in order to specify that statistical units must be unique, and thus force this check upstream.  

## Filtering Out-of-scope Tables and Variables

Defining the scope of the analysis is an important step in data management, and aims to select useful information from the often too extensive available data. In the case of the multi-table training data, this step takes the form of filtering out tables and variables that do not fall within the scope of the analysis.

As with single-table data, the usual practice is to load selected tables into memory, then discard unwanted variables. This practice assumes that the data is not too large in relation to available RAM memory and the maximum size managed by Pandas Dataframe (or equivalent). In addition, it is often necessary to carry out several trial-and-error operations for this selection of tables and variables. This raises the question of versioning these trials and the associated specific code. This practice tends to overload storage space and can prove very costly in cloud environments. 

In an industrial context, where multi-table data can be very large and complex, dictionaries are an excellent way of filtering out unwanted tables and variables on the fly. Basically, only useful columns from selected files are loaded into memory by Khiops. In addition, dictionaries are very light to be versioned, which is much more economical than versioning data and the associated specific data management codes. 

The following example shows how the **Unused** keyword can be used in dictionaries to filter out unwanted tables and variables:
 
!!! success "The Unused keyword applied to tables and variables"
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

Most of the time, databases are organized according to technical constraints (e.g. processing speed of the most frequent queries). Data is stored in a form that is difficult to understand for business experts. It is therefore necessary to reorganize the data, so that it accurately reflects their knowledge of the problem at hand. This is an important step in data management, which involves expressing the experts' knowledge by manually redefining the relational schema.

Usually, this is a laborious, manual job of coding project-specific data-management steps, with the same versioning problems already mentioned. 
Dictionaries offer a much more efficient and economical alternative, thanks to their data manipulation language (see the [reference page][reference_page]). 
The next three subsections provide examples of data manipulation, with (i) redefining the scope of statistical units; (ii) concatenating tables; (iii) advanced selection of training examples. 

### Redefining the scope of statistical units

In many applications, the statistical units under study are not initially stored in the database and need to be defined from the raw data. For example, it may be necessary to clean noisy data containing a large number of insignificant secondary records.     
The following example dictionary file redefines the scope of statistical units by selecting only the secondary records in the `Usage` table corresponding to durations of use greater than ten minutes (i.e. `GE(duration,10)`).  
 

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

Notice that in the command `TableSelection(.,.)`, the first argument designates the name of a table and the second argument is a selection rule applied in the scope of this table. Alternatively, variables from the origin table can be handled using the **"`.`"** operator (which can even be repeated several times). The following dictionary file example selects secondary records from the `Usage` table that are less than one month old after the subscription date. As the `purchaseDate` variable belongs to the origin table, the point is used in the function `TableSelection(allServiceUsages, LE(DiffDate(date, .purchaseDate),30))`.  

!!! success "The point operator"
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

### Table concatenation

In practice, large data tables are sometimes split into several sub-tables for easier storage. This is often the case for secondary tables containing a large number of records (e.g. Log data). In this case, one of the necessary data management steps is to rebuild the secondary table by concatenating the sub-tables. 
The following dictionary file gives an example of usage sub-tables divided up according to time of year (i.e. usagesQuater1, usagesQuater2, usagesQuater3, usagesQuater4). These sub-tables are concatenated using the `TableUnion` function and the `Unused` keyword is placed before every sub-table to be ignored during analysis.
Dictionaries offer great flexibility, especially when it comes to updating models as new sub-tables become available during the year.

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
    Unused    Table(Usage)	usagesQuater1; 
    Unused    Table(Usage)	usagesQuater2;
    Unused    Table(Usage)	usagesQuater3;
    Unused    Table(Usage)	usagesQuater4;	  

        // concatenation of 4 files, divided for volume purposes
    Unused Table(Usage)	allUsages = TableUnion(usagesQuater1, usagesQuater2, usagesQuater3, usagesQuater4);	 
    
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

The following example shows the selection of a particular marketing segment consisting of housewives under 50 who have used the VOD service at least 10 times. 
This selection criterion is complex so it is written on several lines:

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

