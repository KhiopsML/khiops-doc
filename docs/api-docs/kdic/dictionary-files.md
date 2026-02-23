## Standard Dictionaries

Khiops dictionaries allow to describe the structure of the database to analyze and to enable the deployment of the data analysis trained models:
see [`Start Using Dictionaries`](../../tutorials/kdic_intro.md).
<!-- probleme : la presentation n'est plus presente a ce lien -->

A **dictionary file** is a text file with extension *.kdic*, containing the definition of one or many dictionaries.

A **dictionary** allows to define the name and type of variables in a data table file, as illustrated in the following minimal example.

!!! example "Example of a dictionary file"
    
    ```kdic
    Dictionary	Iris
    {
        Numerical	SepalLength	;
        Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;
    };
    ```



It also allows define a label, comments, meta-data per variable, to select variables to use or not for analysis, to construct new variables
 by means of derivation rules.


### Type

The types available for native variables, those that can be stored directly in data table files, are:

- Categorical, 

- Text,

- Numerical,

- Date,

- Time,

- Timestamp,

- TimestampTZ.


Advanced types are provided for specialized usages:

- Entity(name): represents a 0-1 relationship in a multi-table schema, referencing the specified dictionary,
  
- Table(name): represents a 0-n relationship in a multi-table schema, referencing the specified dictionary,
  
- TextList: derived from a list of Text variables, mainly to collect Text variable from a multi-table schema,

- Structure(name): used for algorithmic structures that store model parameters (for internal use).

### Name

The names are case sensitive and are limited to 128 characters. 
In the case where they use characters other than alphanumeric characters, 
they must be surrounded by back-quotes.
Back-quotes inside variable names must be doubled.

### Unused variables

A variable can be ignored in the data processing (memory loading, modeling, deployment) if the keyword *Unused* 
is specified before the variable definition. 

Even though, Khiops is still aware of the variable, which allows to construct new variables derived from the ignored variable.

!!! example "Dictionary file with unused variables"
    
    ```kdic
    Dictionary	Iris
    {
    Unused    Numerical	SepalLength	;
    Unused    Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;
    };
    ```

### Comments and labels

Labels and comments are lines that begin with //.

- at the dictionary level:

    - the label is the first commented line before the dictionary definition,
    
    - comments are the next commented lines before the dictionary definition; they can be interspersed with dictionary definition fragments (e.g. key, meta-data),
    
    - internal comments can be added at the end of the dictionary definition, before the closing curly brace `}`,

- at the variable level:

    - the label must appear on the same line, just after the variable definition,

    - multiple comment lines can precede the variable definition.

Empty lines can be inserted anywhere to improve readability.

!!! example "Dictionary file with comment and labels"
    
    ```kdic
    // Iris Flower
    // Definition of an iris flower
    // Illustration with labels and comments
    Dictionary	Iris
    {
        Numerical	SepalLength	    ;   // Length of sepal
        Numerical	SepalWidth		;   // Width of sepal
        Numerical	PetalLength		;   // Length of petal
        Numerical	PetalWidth		;   // Width of petal


        // The Class variable is the target to predict
        // Since its type is Categorical, this is a classification problem
        Categorical	Class	; // Type of Iris flower

        // Note that this sample is quite verbose
    };
    ```

### Meta-data

Meta-data is a list of keys or key value pairs:

- *<key\>* for boolean values,

- *<key=value\>* for numerical values,

- *<key="value"\>* for string values. 

Meta-data is used internally by Khiops to store information related to dictionaries or variables, such as annotations for modeling results.
Additionally, it is used to store the external format of Date, Time, Timestamp, or TimestampTZ variables when a format other than the default is specified.

!!! example "Example of four predefined meta-data keys : DateFormat, TimeFormat, TimestampFormat and TimestampTZFormat"
    
    ```kdic
    Date MyDate ; <DateFormat="DD/MM/YYYY">
    Time MyTime ; <TimeFormat="HH.MM">
    Timestamp MyTimestamp ; <TimestampFormat="YYYY-MM-DD_HH:MM:SS">
    TimestampTZ MyTimestampTZ ; <TimestampTZFormat="YYYY-MM-DD_HH:MM:SS.zzzzz">
    ```

### Derivation rules

*Derivation rules* enable the construction of new variables within a dictionary. 
Operands in a derivation can be existing variables (by name), numerical or string constants, or the result of other derivation rules, allowing recursive definitions.

String constants can be used for Categorical or Text operands. They must be enclosed in double quotes, with internal double quotes doubled. 
If a value is too long, it can be split into sub-values concatenated with '+' characters.

Numerical constants can be expressed in scientific notation (e.g., 1.3E7), using a dot as the decimal separator. 
The special value *#Missing* indicates a missing numerical value.

Date, Time, Timestamp or TimestampTZ constants are not directly supported but can be generated via conversion rules
(see [`Date Rules`](date-rules.md): e.g. AsDate("2014-01-15", "YYYY-MM-DD")).

A complete list of derivation rules is provided in the [`Dictionary Rules`](numerical-comparisons.md) section.

!!! example "Example of a dictionary file with a constructed variable PetalArea"

    ```kdic
    Dictionary Iris
    {
        Unused Numerical SepalLength;
        Numerical SepalWidth;
        Numerical PetalLength;
        Numerical PetalWidth;
        Numerical PetalArea = Product(PetalLength, PetalWidth);
        Categorical Class; // Class variable
    };
    ```

### Grammar

We present a formal grammar summarizing all features of the dictionary.

Dictionary grammar:

- it is defined by a name, a list of variables, and an optional label,

- the structure is enclosed within braces `{}` and terminated with a semicolon `;`,

- label and comments:

    - label: the first comment line before the dictionary declaration, serving as a title,

    - comments: all comment lines appearing before the opening brace '{' of the dictionary block 
      (for concision purpose, the grammar indicates only the first position where comments can appear),

    - internal comments: comments lines that follow the last variable and appear before the closing brace '}',

- for multi-table schemas, an optional 'Root' tag and key fields can be included (see [`Multi-table dictionary`](dictionary-files.md#multi-table-dictionary)).

```kdic
['//' <label> <EOL>]
['//' <comment> <EOL>]* 
'Root'? 'Dictionary' <name> [ '(' <key-fields> ')' ]
'{'
    [ <variable> ]*
    ['//' <comment> <EOL>]* 
'}' ';'
```

Variable grammar:

- it is defined by a name, with optional 'Unused' tag, derivation, meta-data, and label,

- label and comments:

    - label: an end-of-line comment positioned at the end of the variable declaration,

    - comments: any line comments appearing before the variable declaration.
     

```kdic
['//' <comment> <EOL>]* 
'Unused'? <type> <name> [ '=' <derivation> ] ';' [ <meta-data> ] [ '//' <label> <EOL> ]
```

Variables within a dictionary can also be organized into *variables blocks*. 
This advanced feature, used internally by Khiops for the management of sparse data, is detailed [`here`](intro-block.md). 

## Multi-table dictionary

Whereas most data mining tools work on instances * variables flat tables, real data often have a structure coming from databases. 
Khiops allows to analyse *multi-table* databases, where the data come from several tables, with zero to one or zero to many relation between the tables.

To analyse multi-table databases, Khiops relies on:

- an extension of the dictionaries, to describe multi-tables schemas, (this section)

- databases that are stored in one data file per table in a multi-table schema (cf. [`Train database`](../../ui-docs/khiops.md#train-database)),

- automatic feature construction to build a flat analysis table (cf. [`Variable construction parameters`](../../ui-docs/khiops.md#advanced-predictor-parameters)).

In this section, we present star schemas, snowflake schemas, external tables, then give a summary.

### Star schema

For each dictionary, one or multiple *key fields* must be specified on the first line of the definition, enclosed in parentheses 
(e.g. *Dictionary Customer (id\_customer)*). 

- when multiple key fields are used, they should be separated by commas (e.g. *Dictionary Customer (id\_country, id\_customer)*),

- key fields must be selected from categorical variables and must not be derived from rules.

One dictionary must be designated as the main dictionary, representing the entities to analyze:

- this can be indicated using the optional *Root* tag (e.g. *Root Dictionary Customer (id\_customer)*),

- the Root tag also signifies that entities must be unique according to their key, even in the case of a single-table schema.


The relation between the dictionaries has to be specified by creating new Entity or Table relational variables

- e.g. in *Dictionary Customer*, an *Entity(Address) Address* variable for a 0-1 relationship between a customer and its address (where *Address* is the dictionary of the sub-entity).

- e.g. in *Dictionary Customer*, a *Table(Usage) Usages* variable for a 0-n relationship between a customer and its usages (where *Usage* is the dictionary of the sub-entity).

The keys in the dictionaries of the sub-entities must have at least the same number of fields as in the main dictionary,
but these key fields do not need to have the same names.

There must be one table file per table used in the schema. 
All tables must be sorted by key, and as for the main table, each record must have a unique key.

<!--- TODO les fichers image30/31/32.emf ont ete convertis en .png : est ce un probleme pour la perte de definition des images ? --->

![Customer3tables.png](../../assets/images-khiops-guides/khiops/image30.png)

!!! example "Example of a multi-table dictionary file"

    A dictionary file with a main dictionary *Customer*, a 0-1 relation with *Address* and a 0-n relation with *Usages* 
    A multi-table database related to this multi-table dictionary consists of three data table files, sorted by their key fields.

    ```kdic
    Root Dictionary Customer(id_customer)
    {
        Categorical id_customer;
        Categorical Name;
        Entity(Address) Address; // 0-1 relationship
        Table(Usage) Usages; // 0-n relationship
    };

    Dictionary Address(id_customer)
    {
        Categorical id_customer;
        Numerical StreetNumber;
        Categorical StreetName;
        Categorical City;
    };

    Dictionary Usage(id_customer)
    {
        Categorical id_customer;
        Categorical Product;
        Timestamp Time;
        Numerical Duration;
    };
    ```

### Snowflake schema

The example in the preceding section illustrates the case of a star schema, with the customer in a main table and its address and usages in secondary tables. Secondary tables can themselves be in relation to sub-entities, leading to a snowflake schema. 
In this case, the number of key fields must increase with the depth of the schema (but not necessarily at the last depth).

![CustomerSF4tables.png](../../assets/images-khiops-guides/khiops/image31.png)

### External tables

External tables can also be used, to share common tables accros multiple analysis entities.

In the following schema, the products can be referenced from the services of a customer.

![CustomerSFE5tables.png](../../assets/images-khiops-guides/khiops/image32.png)

Whereas the sub-entities of the main entity Customer, such as address, services, and usages per service, 
are all ***included*** within the customer ***folder***, products are ***referenced*** by the services.

The dictionary defining an external table must include the *Root* tag,
indicating that its records can be uniquely identified and referenced by key.

The related table file will be fully loaded in memory for efficient direct access,
whereas the entities of each folder can be loaded one at a time, for scalability reasons.

Whereas the joins between the tables of the same folder are implicit, on the basis of the table keys,
the join with an external table must be explicit in the dictionary, using a key (into brackets) from the referencing entity.
Note that this key can be derived using derivation rules if necessary.

!!! example

    ```kdic
    Dictionary Service (id_customer, id_product)
    { 
        Categorical id_customer;
        Categorical id_product;
        Entity(Product) Product [id_product]; // External table with the join key 'id_product'
        Table(Usage) Usages;
    };

    Root Dictionary Product (id_product)
    {
        Categorical id_product;
        Categorical Name;
        Numerical Price;
    };
    ```

Examples of datasets with multi-table schemas and external tables are given in the "samples" directory of the Khiops package (%PUBLIC%\\khiops\_data\\samples in Windows, $HOME/khiops\_data/samples in Linux) .

### Data path

A multi-table schema is a hierarchical schema, with a **main dictionary** and relations to secondary dictionaries using `Entity` variables for 0-1 relationships and `Table` variables for 0-n relationships.

Each entity can be uniquely identified by its **data path**, which is the sequence of relation variable names leading to the entity, separated by slashes (/):

- The main entity has an empty data path.

- In a star schema, the data paths are the names of Table or Entity variables for each secondary entity.

- In a snowflake schema, data paths consist of a list of variable names separated by '/'.

- External tables begin with a data root prefixed with '/', which refers to the name of the referenced root dictionary.

**Note:** If an element of a data path contains the '/' character or the back-quote character, it must be surrounded by back-quotes, with internal back-quotes doubled, like for variable [`names`](#name).

!!! example
    In the snowflake example [`External tables`](#external-tables), if the Customer is chosen as the main entity to analyze, the data paths are:

    - empty data path for the main entity Customer

    - `Address`: for the Address secondary entity in a 0-1 relationship

    - `Services`: for the Service secondary entities in a 0-n relationship

    - `Services/Usages`: for the Usage secondary entities in a 0-n relationship, from the services

    - `/Product`: for the Product entity used as an external table

To build entities from data files, multi-table databases utilize a set of data table files, one per data path related to native (non-derived) entities within a schema.

### Summary

Khiops allows to analyse multi-table databases, from standard mono-table to complex schema.

|   | Database format  |
| -----| ----------|
| ![](../../assets/images-khiops-guides/khiops/image33.png) | Mono-table : <br>  - standard representation <br> Fields types : <br>  - Numerical, Categorical <br> - Text <br> - Date, Time, Timestamps, TimestampsTZ |
| ![](../../assets/images-khiops-guides/khiops/image34.png) | Star schema standard representation : <br> - Multi-table extension <br> - Each table must have a key <br> - The main table can be tagged as *Root* <br> Additional fields types in the main table : <br> - Entity: 0-1 relationship <br> - Table : 0-n relationship|
| ![](../../assets/images-khiops-guides/khiops/image35.png) | Snowflake schema : <br> - Extended star schema <br> - Each table must have a key <br> - The main table can be tagged as *Root* <br> Additional fields types in *any* table of the schema : <br> - Entity: 0-1 relationship <br> - Table : 0-n relationship|
| ![](../../assets/images-khiops-guides/khiops/image36.png) | External tables : <br> - External tables allow to reuse common tables referenced by all entities <br> - Must be root tables <br> - Must be referenced explicitely, using keys from the referencing entities | 



### Derivation rules for multi-table schemas

Derivation rules can be used to extract information from other tables in a multi-table schema. 
In this case, they use variables of different scopes:

- First operand of type Entity or Table, in the current dictionary scope (ex: DNA),

- Next operands, in the scope of the secondary table (ex: Pos, Char).

!!! example

    The "MeanPos" and "MostFrequentChar" extract information from a DNA sequence in the secondary table. 
    The derivation rules (TableMean and TableMode) have a first operand that is a Table variable in the scope of SpliceJunction, 
    while their second operand is in the scope of SpliceJunctionDNA.

    ```kdic
    Root Dictionary SpliceJunction(SampleId)
    {
        Categorical SampleId;
        Categorical Class;
        Table(SpliceJunctionDNA) DNA;
        Numerical MeanPos = TableMean(DNA, Pos); // Mean position in the DNA sequence
        Categorical MostFrequentChar = TableMode(DNA, Char); // Most frequent char in the DNA sequence
    };

    Dictionary SpliceJunctionDNA(SampleId)
    {
        Categorical SampleId;
        Numerical Pos;
        Categorical Char;
    };
    ```

### Derivation rules with multiple scope operands

For operands in the scope of a secondary table, it is possible to use variables from the scope of the current dictionary, 
which is in the "upper" scope of the secondary table. In this case, the scope operator '.' must be used.

!!! example

    The "FrequentDNA" selects the record of the "DNA" table, where the Char variable (in secondary table) is equal to the "MostFrequentChar" variable 
    (with the scope operator '.'), as it in the scope of the current dictionary. 
    The "MostFrequentCharFrequency" computes the frequency of this selected sub-table.

    ```kdic
    Root Dictionary SpliceJunction(SampleId)
    {
        Categorical SampleId;
        Categorical Class;
        Table(SpliceJunctionDNA) DNA;
        Categorical MostFrequentChar = TableMode(DNA, Char);
        Table(SpliceJunctionDNA) FrequentDNA = TableSelection(DNA, EQc(Char, .MostFrequentChar));
        Numerical MostFrequentCharFrequency = TableCount(FrequentDNA);
    };
    ```

    Note that the resulting "MostFrequentCharFrequency" could be computed using one single formula:
    ```kdic
    Numerical MostFrequentCharFrequency = TableCount(TableSelection(DNA, EQc(Char,.TableMode(DNA, Char))));
    ```

### Derivation Rules to Build New Entities

In a multi-table schema, each memory instance is constructed and populated from a record in a data file.

Rules such as `TableSelection` allow referencing existing entities.

Other rules, such as `BuildEntity`, enable the creation of new entities.

These rules:

- Have a name prefixed by `Build`.

- Are used to create and populate a variable of type `Entity` or `Table` for a specific **target dictionary**.

- Can include additional specific output parameters, specified after the ':' separator in the list of rule parameters, to define the value of target variables.

For more details, see [`Instance building rules`](../kdic/instance-building-rules-introduction.md).

Note that all built entities in a multi-table schema can be identified by their [`data path`](#data-path), whether they are created from records or through instance building rules.


## Deeper Insights 


### In-Memory Instances

In the **Customer** snowflake example above, the main entity is the *Customer*, with its main variables,
along with relational variables that encode the hierarchical structure of a customer:


- `Customer`: the main instance

    - `Address`: a secondary instance
  
    - `Services`: an array of secondary instances associated with the customer
  
        - `Usages`: an array of secondary instances, one per service

In memory, this hierarchical structure closely resembles objects in programming languages,
which can be composed of sub-objects or arrays of sub-objects. 
Khiops dictionaries provide a language that allows us to describe and formalize this structure concisely and in an expressive manner.


### Reading Instances from Flat Files

In the context of Khiops, **keys** are introduced within each dictionary solely to facilitate reading data from files
and constructing hierarchical in-memory instances. 
These keys are organized hierarchically according to the Khiops dictionary schema: the key fields of a parent entity are
a subset of the key fields of its sub-entities.

The mapping between in-memory instances and data stored on disk is managed using one tabular file per node in the hierarchical schema, 
with each file sorted by its key. During data loading and processing, all data files are read simultaneously. 
For each segment of the files where the key values start with the current main entity's key, an in-memory entity is
reconstructed, processed, and then discarded from memory to make room for the next instance.

This organization ensures scalable analysis, even with very large flat files that far exceed available RAM, 
by enabling efficient sequential access and hierarchical reconstruction of data.


### Interest of External Tables

Beyond their role in representing the conceptual data model, such as for example separating **customer** management and purchase **logs** 
from referenced **products**, external tables provide important resource optimization benefits:

- **In-Memory Loading for Speed:**  
  External tables are fully loaded into memory to enable rapid access and sharing within each process.  
    - Random disk access is impractical due to high latency, especially when dealing with millions of *customers* and billions of *logs*, each requiring *product* lookups among hundreds of thousands.  
    - Pre-joining external data with main entity *logs* to avoid repeated disk access is highly costly in terms of storage space.

- **Shared Data and Computations:**  
  Loading external tables into memory allows for shared access to data and derived variables, which are computed once and reused within each process.  
    - However, processing external tables is resource-intensive: it is not parallelized and must be performed separately for each process, unlike standard tables, which are processed in parallel with each process handling a subset of the table.
    - This approach is unsuitable for very large external tables.  
    - To maximize efficiency, external instances should be reused:  
        - **Unfavorable case:** When there are more external instances than main instances, pre-filtering relevant external data can be beneficial.  
        - **Favorable case:** When external instances are few and highly reused by main instances.

## Relation with Other Data Modeling Concepts

A **Khiops dictionary** is a formal schema that allows data analysts to describe data at a conceptual level based on domain knowledge. It specifies variables, types, labels, metadata, and derivation rules, supporting hierarchical multi-table schemas to represent complex data structures. 

It guides data loading, transformation, and interpretation, enabling efficient, end-to-end model deployment, including feature engineering, preprocessing, and modeling.

Many concepts used in Khiops dictionaries are similar to existing data modeling concepts.  
However, while these analogies can be helpful for data analysts familiar with such concepts, they may also be misleading.  
This section aims to clarify the similarities and differences to ensure a better understanding.

[data-dictionary]: https://en.wikipedia.org/wiki/Data_dictionary "Visit the Wikipedia page"  
[entity-relationship-model]: https://en.wikipedia.org/wiki/Entity-relationship_model "Visit the Wikipedia page"  
[data-model]: https://en.wikipedia.org/wiki/Data_model "Visit the Wikipedia page"  
[database]: https://en.wikipedia.org/wiki/Database "Visit the Wikipedia page"  
[hierarchical-database]: https://en.wikipedia.org/wiki/Hierarchical_database_model "Visit the Wikipedia page"  
[nosql-database]: https://en.wikipedia.org/wiki/NoSQL "Visit the Wikipedia page"  
[relational-database]: https://en.wikipedia.org/wiki/Relational_database "Visit the Wikipedia page"  
[object-database]: https://en.wikipedia.org/wiki/Object_database "Visit the Wikipedia page"  
[document-database]: https://en.wikipedia.org/wiki/Document-oriented_database "Visit the Wikipedia page"  
[programming-language]: https://en.wikipedia.org/wiki/Programming_language "Visit the Wikipedia page"  
[declarative-language]: https://en.wikipedia.org/wiki/Declarative_programming "Visit the Wikipedia page"  

### Data Dictionary

A **[data dictionary:octicons-link-external-16:][data-dictionary]{:target="_blank"}** 
is an abstract framework that organizes data and their relationships. For example, it might define a customer with properties like name and age, and link the customer to various services with details such as type and amount.

A **data dictionary** is a centralized repository that defines and describes the structure, contents, and format of data within a database or data system. It includes metadata such as variable names, types, labels, and relationships. 

**In Khiops**, dictionaries serve a similar purpose: they define the data structure, specify variable types, and include metadata, labels and derivation rules.  
However, they are specifically designed to facilitate the automation of the data mining process.
They act as a formal schema that guides data loading, transformation, and analysis, ensuring consistency and efficiency throughout the workflow.

### Entity-Relationship Model

The **[entity-relationship model:octicons-link-external-16:][entity-relationship-model]{:target="_blank"}** 
is a conceptual framework for representing data entities and their relationships, often used in database design.

**In Khiops**, data is modeled using a **hierarchical schema**.  
There is a main entity, with secondary entities described through `Entity` variables for 0-1 relationships and `Table` variables for 0-n relationships.
All variables within a dictionary describe either the content of the related entity, using basic type variables (e.g., Numerical, Categorical, Date, Text), or its structure, using relation variables (`Entity` and `Table`).  
This approach provides a clear, formal description of complex data schemas, supporting multi-table analysis and feature engineering.
It also ensures efficiency and scalability, enabling the processing of data that cannot fit entirely into memory.

### Data Modeling

A **[data model:octicons-link-external-16:][data-model]{:target="_blank"}** involves creating abstract representations of data structures, relationships, and constraints within a system. It provides a blueprint for designing databases and data schemas.
Data models can be of three types:

- **Conceptual Model:** Abstract, high-level description of data entities and relationships (e.g., ER model).  

- **Logical Model:** Detailed schema defining tables, columns, and relationships, often platform-independent.  

- **Physical Model:** Implementation-specific schema optimized for storage and retrieval, including indexing and denormalization.

**In Khiops**, hierarchical schemas are used to describe entities for analysis, similar to folders, enriching traditional flat data tables with relation variables that capture more complex details.  
Another key goal is scalability, enabling the processing of large datasets that cannot fit entirely into memory.  
Similarly to data models, Khiops dictionaries can be used at different levels:  

- **Conceptual level:** To describe data using domain knowledge.  

- **Logical level:** To specify data sources and their structure, while maintaining the mapping between conceptual and logiucal representations.  

- **Physical level:** To manage actual data files stored locally or in the cloud.

See [`Conceptual, Logical, and Physical Data Models`](../../tutorials/conceptual_schema.md) for more details,
including numerous examples of mapping between conceptual and logical schemas using Khiops dictionaries,
as well as cases where data management is necessary to preprocess data according to Khiops requirements.

### Databases

A **[database:octicons-link-external-16:][database]{:target="_blank"}** is an organized collection of data stored and managed electronically.
It enables efficient data retrieval, manipulation, and management through various database management systems (DBMS).

Database technologies cover a broad spectrum of schema types, each suited to specific needs: simple storage, hierarchical, relational, object-oriented, document-oriented, columnar, in-memory, or distributed.
The choice depends on performance, data structure, scalability, and use cases such as transactional processing, analytics, or big data.

**In Khiops**, the traditional **single-table data schema** used in data mining is extended to support **hierarchical schemas**.
This allows **domain knowledge encoding, automated feature engineering, and predictive modeling**, bridging the gap between raw relational data and machine learning workflows.  

With Khiops dictionaries, data analysts can describe data at both the conceptual level, using domain knowledge, and at the logical level, to specify data sources and the mapping between the conceptual and logical schemas (see [`Conceptual, Logical, and Physical Data Models`](../../tutorials/conceptual_schema.md)).

The logical schemas definied using Khiops dictionaries share clear similarities with existing database technologies:

- **[Hierarchical data base:octicons-link-external-16:][hierarchical-database]{:target="_blank"}:**  
  Khiops logical schemas are hierarchical, but conceptual schemas can be non-hierarchical, supporting complex structures like double-link lists or graphs (see [`List and Graph Rules`](list-and-graph-rules.md)).

- **[Relational data base:octicons-link-external-16:][relational-database]{:target="_blank"}:**  
  Khiops dictionaries involved in multi-table schemas have keys similar to relational tables, but with notable differences:  
  
    - The schema is hierarchical, with keys organized along the hierarchy, increasing in length with depth but sharing prefixes.  
  
    - A single dictionary can describe multiple data tables, e.g., separate tables for retail and online services, using the same dictionary.  
  
    - References to external tables resemble foreign keys but can be dynamically computed via derivation rules rather than fixed variables.

- **[Object-oriented data base:octicons-link-external-16:][object-database]{:target="_blank"}:**  
  There is an analogy between Khiops dictionaries (considered as classes) and in-memory entities (similar to objects).
  However, while object-oriented databases focus on complex data representation with database constraints, Khiops dictionaries are specifically designed for data mining, prioritizing efficiency, scalability, and the integration of domain knowledge.

- **[NoSql data base:octicons-link-external-16:][nosql-database]{:target="_blank"}:**  
  NoSQL systems ("Not only SQL" or "non-relational") store data differently from traditional relational tables.
  In Khiops, mapping a multi-table schema to sorted data files based on consistent keys resembles a NoSQL-like processing approach.
  This method enables sequential reading of files synchronized by entity keys, allowing structured entities
  to be built incrementally, with related information stored contiguously for efficient access.

- **[Document-oriented data base:octicons-link-external-16:][document-database]{:target="_blank"}:**  
  These encode all information about an entity in formats like JSON or XML, enabling efficient access to complex structures.
  Khiops offers partial support for this approach through derivation rules such as
  [`BuildEntityFromJson`](json-extraction-rules.md#buildentityfromjson), which allows constructing hierarchical
  in-memory entities from a JSON string.

!!! note

    Khiops cannot directly connect to relational databases.
    Instead, data must be prepared as one sorted file per entity within a hierarchical schema after transforming from the [`logical to conceptual schema`](../../tutorials/conceptual_schema.md).  
    While this data preparation step is necessary, it is much simpler than traditional feature engineering, which often involves converting complex structured data into a single-table format for analysis.

### Programming Languages

Khiops dictionaries are a specialized programming language designed for data mining tasks:

- **First step: Data analyst's exploitation of Khiops dictionaries**

    - **At the conceptual level**: describe the data based on domain knowledge.
  
    - **At the logical level**: describe data sources and establish the mapping between the conceptual and logical levels.

- **Second step: automatic extension by the Khiops tool**  
  The Khiops tool automatically extends this initial dictionary to enable end-to-end data processing, from data access to score production:

    - **Feature engineering**: build a flat representation from a multi-table schema, extract tokens from text, and construct trees.
  
    - **Preprocessing**: obtain efficient univariate or bivariate density estimators through supervised discretization or value grouping.
  
    - **Feature selection**: select a sparse representation of the available data.
  
    - **Modeling**: generate prediction scores.

Their syntax is similar to familiar languages such as `struct` in C or `class` in C++ and Java, making it intuitive for developers.
A dictionary can be viewed as a class, in-memory instances as objects, variables of type `Entity` as sub-objects, and variables of type `Table` as arrays of sub-objects.

!!! example "Khiops Iris dictionary"

    ```kdic
    Dictionary Iris
    {
        Numerical SepalLength;
        Numerical SepalWidth;
        Numerical PetalLength;
        Numerical PetalWidth;
        Categorical Class;
    };
    ```

!!! example "C++ class for defining Iris objects"

    ```cpp
    class Iris {
        double SepalLength;
        double SepalWidth;
        double PetalLength;
        double PetalWidth;
        std::string Class;
    };
    ```

We present key features of Khiops dictionaries as a specialized programming language for data mining:

- **Domain-specific language**: Designed explicitly for efficient, tailored data mining workflows.

- **Intuitive syntax**: Similar to familiar languages like `struct` in C or `class` in C++/Java, facilitating learning and use.

- **Hierarchical schemas**: Supports defining complex, nested data structures to accurately model real-world data.

- **Declarative approach**: Focuses on specifying *what* to achieve, not *how*, simplifying workflow design.

- **Strongly typed**: Variables have explicit types checked at compile time for correctness and optimization.

- **Automatic memory management**: Efficiently handles memory using `strong pointers` for core hierarchical schema and `weak pointers` for references to existing entitie, inspired by modern languages, reducing manual effort.

- **Automatic propagation of missing values**: Derived variables from missing data are automatically marked as missing, ensuring data integrity.

- **Parallel processing**: Leverages available resources (cores, machines, RAM, disk) to maximize processing speed.

- **Optimized for data mining**: Analyzes each dictionary to access only necessary data, parse relevant columns, and compute derivations on demand.

- **Robust**: Handles large datasets gracefully, issuing warnings rather than crashing, in case of minor inconsistencies or massive instances.

- **Portable**: Supports deployment across various environments and platforms, ensuring flexibility.

- **Meta-programming**: Via the Khiops Python API, dictionaries can be programmatically read, created, or updated, enabling automation of complex tasks.
