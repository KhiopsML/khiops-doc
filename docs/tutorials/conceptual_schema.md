This section introduces the use of Khiops dictionaries for defining conceptual and logical schema.
For full documentation, please refer to the dictionaries [reference page][reference_page].
[reference_page]:../api-docs/kdic/dictionary-files.md


## Conceptual, Logical, and Physical Data Models

### Introduction

A [data model:octicons-link-external-16:][data-model]{:target="_blank"} is an abstract framework that organizes data and their relationships. For example, it might define a customer with properties like name and age, and link the customer to various services with details such as type and amount.

[data-model]: https://en.wikipedia.org/wiki/Data_model "Visit the Wikipedia page"  
[denormalization]: https://en.wikipedia.org/wiki/Denormalization "Visit the Wikipedia page"
[entity-relationship-model]: https://en.wikipedia.org/wiki/Entity-relationship_model "Visit the Wikipedia page"

Data models are widely used for database design.
They can be of three types:

- **Conceptual Data Model**: Describes the semantics of a domain, including entity classes and relationships. It defines the scope and the kinds of facts that can be expressed.

- **Logical Data Model**: Represents the semantics using a specific data manipulation technology, such as tables, columns, classes, or XML tags.

- **Physical Data Model**: Details how data is stored physically, including partitions, CPUs, and tablespaces.

Khiops dictionaries are tailored for data mining tasks, covering data understanding, preparation, modeling, evaluation, and deployment.
They are based on multi-table hierarchical schemas, such as star or snowflake schemas.

While similar to [entity-relationship model:octicons-link-external-16:][entity-relationship-model]{:target="_blank"} 
used for conceptual design, Khiops schemas are hierarchical, with `Entity` representing 0-1 relationships and `Table` representing 0-n relationships.

In a way similar to data models, Khiops dictionaries can be used at different levels:

- **Conceptual Schema**: Description of the data to analyze at a conceptual level, based on domain knowledge.

- **Logical Schema**: Description of the data at a logical level, reflecting the schema of the actually available data.

- **Physical Schema**: Multi-table mapping, with a list of data files per entity of the logical schema.

In a Khiops dictionary, the conceptual schema consists of the subset of variables used for analysis.

The logical schema may differ from the conceptual schema, in the case of [denormalization:octicons-link-external-16:][denormalization]{:target="_blank"} for example.
In a Khiops dictionary, the logical schema includes the subset of variables, potentially unused, necessary to describe the data sources.  

In many cases, the mapping between the logical and the conceptual schema can be described using derivation rules, which allow the construction of a conceptual representation of the data on the fly from the available data at the logical level.

### Example of a Conceptual Schema for a Khiops Dictionary

Let us consider a basic example of a conceptual schema involving a Customer and their services.  
This star schema allows a data analyst to describe their data at a conceptual level, based on domain knowledge.

!!! success "Example: Conceptual schema, with a Customer and its services"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services;
    };

    // Monthly amount per service
    Dictionary Service (customer_id)
    {
        Categorical customer_id;
        Categorical type;
        Date month; // Using a YYYY-MM-DD format, with DD=01
        Numerical amount;
    };
    ```

In this basic example, the logical schema and conceptual schema can be considered the same, and no transformation is necessary.  
The only element that could be considered at the logical level is the `customer_id` key variable in the `Service` dictionary, which is necessary as an implicit join key between the customer and service data table files.

The physical schema consists of the multi-table mapping of the dictionary to actual files, stored either on a local disk or in the [`Cloud`](./storage.md), using the **data path** to specify each sub-part of the hierarchical schema:

- Main table: `MyCustomerFile.txt`

- Secondary table at data path `services`: `MyServiceFile.txt`


## Mapping a Conceptual Schema to a Logical Schema

While in some cases the logical schema and conceptual schema may be identical, raw data often lacks an explicit conceptual structure.  
In such situations, transforming raw data into a well-defined conceptual schema becomes essential, typically using data management tools.

Khiops dictionaries facilitate this transformation by allowing you to specify the raw data in its logical format, retaining unused variables if necessary, and then defining derivation rules to construct the conceptual schema from the logical one.

The following series of examples illustrates this process in detail.


### Large Service Table File with Out-of-Scope Records 

Suppose service records are stored in a large data file containing historical records spanning multiple years.
If the scope of analysis is limited to a specific year, you can select the relevant records using the `TableSelection` rule.

!!! success "Example: Selecting Relevant Secondary Records using TableSelection"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services = TableSelection(rawServices, EQ(Year(month), 2026));

        // Raw services from the logical schema
        Unused Table(Service) rawServices; 
    };

    // Monthly amount per service
    Dictionary Service (customer_id)
    {
        Categorical customer_id;
        Categorical type;
        Date month;
        Numerical amount;
    };
    ```

### One Data File per Quarter

Suppose service records are stored in a separate file for each quarter.
You can then use the `TableUnion` rule, as described in the [`Table Concatenation`](.#table-concatenation) section.

!!! success "Example: Merging Several Secondary Data Tables using TableUnion"
    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services	=
          TableUnion(servicesQuarter1, servicesQuarter2, servicesQuarter3, servicesQuarter4);

        // Raw services from the logical schema
        Unused Table(Service) servicesQuarter1;
        Unused Table(Service) servicesQuarter2;
        Unused Table(Service) servicesQuarter3;
        Unused Table(Service) servicesQuarter4;
    };

    // Monthly amount per service
    Dictionary Service (customer_id)
    {
        Categorical customer_id;
        Categorical type;
        Date month;
        Numerical amount;
    };
    ```

### One Partial Data File per Service

Suppose service records are stored in separate files for each service, with no column indicating the service name.

To obtain data according to the conceptual schema, we first need to create new in-memory records from the raw data by adding the service name to each record.
This can be achieved using the `BuildAdvancedView` rule from the [`Instance Building Rules`](../api-docs/kdic/instance-building-rules-introduction.md).

You can then use the `TableUnion` rule to combine all the service tables into a single unified table.

!!! success "Example: Completing and Merging Several Partial Secondary Data Tables"

    In the following example, we illustrate a solution for two types of services: `online` and `retail`.

    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services =
          TableUnion(onlineServices, retailServices);

        // Build tables, ensuring that the type of service is stored in the corresponding target variable
        Unused Table(Service) onlineServices =
          BuildTableAdvancedView(onlineRawServices, "retail" : type);
        Unused Table(Service) retailServices =
          BuildTableAdvancedView(retailRawServices, "online" : type);

        // Raw services from the logical schema
        Unused Table(RawService) onlineRawServices;
        Unused Table(RawService) retailRawServices;
    };

    // Monthly amount per service
    Dictionary Service (customer_id)
    {
        Categorical customer_id;
        Categorical type;
        Date month;
        Numerical amount;
    };

    // Monthly amount for a given type of service, from the logical schema
    Dictionary RawService (customer_id)
    {
        Categorical customer_id;
        Date month;
        Numerical amount;
    };
    ```

### One Single File with Columns Per Service

Suppose that the `amount` values for each service are stored in as many columns as necessary within a single main table, with one column per service and per month.
This situation is common in real-world data marts, where data collected from relational databases has been summarized into a single table using a propositionalization process.
This practice is also frequent in many time series datasets, with one column per value of the series.

To obtain data according to the conceptual schema, we first need to create new in-memory records for each instance of a service.
This can be achieved using the `BuildEntity` rule from the [`Instance Building Rules`](../api-docs/kdic/instance-building-rules-introduction.md).

You can then use the `EntitySet` rule to collect all the built instances into a single table.

Note that in this example, the conceptual schema follows a star schema, while the logical schema is a single table.
The customer_id variable in the secondary table is not necessary, as no join is required to create the secondary instances.

!!! success "Example: Building Table Entities From Raw Column Values"

    In the following example, we illustrate a solution for two types of services,  `online` and `retail`, 
    with amount values collected over three months: `01`, `02`, and `03`.

    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services =
          EntitySet(serviceOnline01, serviceRetail01, 
                    serviceOnline02, serviceRetail02, 
                    serviceOnline03, serviceRetail03);

        // Build entities for the services, based on the raw values of amount
        Unused Entity(Service) serviceOnline01 = BuildEntity(customer_id, "online", BuildDate(2026, 1, 1), amountOnline01 :
                                                             customer_id, type, month, amount);
        Unused Entity(Service) serviceRetail01 = BuildEntity(customer_id, "retail", BuildDate(2026, 1, 1), amountRetail01 :
                                                             customer_id, type, month, amount);
        Unused Entity(Service) serviceOnline02 = BuildEntity(customer_id, "online", BuildDate(2026, 2, 1), amountOnline02 :
                                                             customer_id, type, month, amount);
        Unused Entity(Service) serviceRetail02 = BuildEntity(customer_id, "retail", BuildDate(2026, 2, 1), amountRetail02 :
                                                             customer_id, type, month, amount);
        Unused Entity(Service) serviceOnline03 = BuildEntity(customer_id, "online", BuildDate(2026, 3, 1), amountOnline03 :
                                                             customer_id, type, month, amount);
        Unused Entity(Service) serviceRetail03 = BuildEntity(customer_id, "retail", BuildDate(2026, 3, 1), amountRetail03 :
                                                             customer_id, type, month, amount);

        // Raw values of amount, with one variable per service and per months
        Numerical amountOnline01;
        Numerical amountRetail01;
        Numerical amountOnline02;
        Numerical amountRetail02;
        Numerical amountOnline03;
        Numerical amountRetail03;
    };

    // Monthly amount per service
    Dictionary Service (customer_id)
    {
        Categorical customer_id;
        Categorical type;
        Date month;
        Numerical amount;
    };
    ```


### Secondary Data Available in JSON Format

Suppose all data related to services is stored in a single JSON field, a practice becoming increasingly common, for example, in document-oriented databases.

Recoding the raw data according to the conceptual schema is possible using the `BuildTableFromJson` rule from the [`Instance Building Rules`](../api-docs/kdic/instance-building-rules-introduction.md).
This rule leverages a target dictionary that describes the structure of the JSON data and creates a snowflake of in-memory instances from the objects and arrays contained within the JSON.

Note that like in the previous example, the conceptual schema follows a star schema, while the logical schema is a single table.

!!! success "Example: Extracting a table from JSON data"

    In the following example, the dictionary `Service` describes a basic JSON structure, with an array of objects, one per service instance.

    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services = BuildTableFromJson(jsonServicesData);

        // Raw values of services stored in a JSON field
        Text jsonServicesData;
    };

    // Monthly amount per service
    Dictionary Service (customer_id)
    {
        Categorical customer_id;
        Categorical type;
        Date month;
        Numerical amount;
    };
    ```

    If the `jsonServicesData variable` contains the following JSON value (beautified for clarity),
    the `services` Table built using the `BuildTableFromJson` rule will consist of 6 entities, one per object in the JSON array.

    ```json
    {"services":[{"customer_id":"Id0000","name":"online","month":"2026-01-01","amount":1500},{"customer_id":"Id0000","name":"retail","month":"2026-01-01","amount":2000},{"customer_id":"Id0000","name":"online","month":"2026-02-01","amount":1600},{"customer_id":"Id0000","name":"retail","month":"2026-02-01","amount":2100},{"customer_id":"Id0000","name":"online","month":"2026-03-01","amount":1700},{"customer_id":"Id0000","name":"retail","month":"2026-03-01","amount":2200}]}
    ```

    ```json
    {
      "services": [
        {
          "customer_id": "Id0000",
          "name": "online",
          "month": "2026-01-01",
          "amount": 1500
        },
        {
          "customer_id": "Id0000",
          "name": "retail",
          "month": "2026-01-01",
          "amount": 2000
        },
        {
          "customer_id": "Id0000",
          "name": "online",
          "month": "2026-02-01",
          "amount": 1600
        },
        {
          "customer_id": "Id0000",
          "name": "retail",
          "month": "2026-02-01",
          "amount": 2100
        },
        {
          "customer_id": "Id0000",
          "name": "online",
          "month": "2026-03-01",
          "amount": 1700
        },
        {
          "customer_id": "Id0000",
          "name": "retail",
          "month": "2026-03-01",
          "amount": 2200
        }
      ]
    }
    ```

## Transforming Data to Conceptual Schema

Data used for data mining come from a wide variety of sources and formats :

- Databases: hierarchical, network, relational, object-oriented, document-oriented, cloud-based, etc.

- Data warehouses

- Flat files

- The World Wide Web

- Application-specific data

- And others

Khiops employs hierarchical schemas to improve scalability.
Because each table in the schema shares the same key variable as the main tables, all data tables, sorted by key, can be read at the same time.
This enables quick and efficient reconstruction of the in-memory snowflake schema of each main instance, one at a time.

Describing the available data at a conceptual level using Khiops dictionaries is sometimes straightforward, 
as illustrated with the following entity-relationship model.

!!! success "Example: Customer and Services - Basic Entity-Relationship Model"

    In our previous Customer and Service example, there is a good match between Khiops' hierarchical conceptual schema and the conceptual data model of a relational database consisting of two tables:
    ```
    +--------------------+             +--------------------+
    |   Customer         |             |   Service          |
    +--------------------+             +--------------------+
    | - customer_id (PK) |<----------- | - customer_id (FK) |
    | - name             |             | - type             |
    | - age              |             | - month            |
    +--------------------+             | - amount           |
                                       +--------------------+
    ```

However, this is not always the case, and data management may be necessary to ensure Khiops receives data that complies with its hierarchical requirements.

Below, we present basic examples with data originating from a relational database, which involves entity-relationship models incompatible with Khiops' hierarchical requirements.

!!! success "Data transformation using derivation rules"

    Note that Khiops derivation rules are a powerful feature that enable a wide range of transformations,
    allowing for expressive and detailed conceptual descriptions, including complex structures such as
    [`double-link lists`](../api-docs/kdic/list-and-graph-rules.md#buildlist) or 
    [`graphs`](../api-docs/kdic/list-and-graph-rules.md#buildgraph).

    Nonetheless, data management remains essential for preprocessing data from unconventional or non-standard sources to ensure compatibility with Khiops requirements.

### Relational Database with Many-to-Many Relationalship

The Customer and Service data can be modeled using a **many-to-many** relationship, where each Customer can use multiple Services.  
The junction table called **CustomerService** stores information about a specific use of the service by that customer.

!!! success "Example: Customer and Services, Using a Many-to-Many Relationship"
   
    ```
    +--------------------+             +--------------------+
    |   Customer         |             |   CustomerService  |
    +--------------------+             +--------------------+
    | - customer_id (PK) |<------------| - customer_id (FK) |
    +--------------------+             | - service_id (FK)  |
                                       | - month            |
                                       | - amount           |
                                       +--------------------+
                                              |
                                              |
                                              v
                                       +-------------------+
                                       |   Service         |
                                       +-------------------+
                                       | - service_id (PK) |
                                       | - type            |
                                       +-------------------+
    ```

In this case, a Khiops dictionary involving an external table can be used to easily obtain data that meets Khiops' hierarchical requirements.

The external table contains data fully loaded into memory, enabling efficient access when the keys are unrelated to the hierarchical keys of the main entity being analyzed.  
See [`external tables`](../api-docs/kdic/dictionary-files.md#interest-of-external-tables) for more information.

!!! success "Example: Customer and Services - Using an external table"

    In this example, the two dictionaries, `Customer` and `Service`, are still used to describe the data at a conceptual level.  
    The data related to services is described in an external table represented by the `ServiceData` dictionary.  
    One external `ServiceData` entity is retrieved for each service using the `service_id` key to obtain the `type` of service.

    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services;
    };

    // Monthly amount per service
    Dictionary Service (customer_id)
    {
        Categorical customer_id;
        Categorical type = GetValueC(serviceData, type);  // Information retrieved from external data
        Date month;
        Numerical amount;

        // Raw services from the logical schema
        Unused Categorical service_id; // Key to external table ServiceData
        Unused Entity(ServiceData) serviceData[service_id]; // Unique in-memory entity from the external table
    };

    // Dictionary for external table ServiceData, containing data specific to each service
    Root Dictionary ServiceData (service_id)
    {
        Categorical service_id;
        Categorical type;
    };
    ```


### Relational Database with Non-Hierarchical Relationalships

Non-hierarchical schemas are commonly used in relational database modeling, as illustrated by the following example from the telecommunications domain.

!!! success "Example: Example from the Telecommunication Domain"

    In the telecommunications domain, each customer has a unique identifier, and each of their phone devices is identified by a phone number. 
    Call Detail Records (CDRs) are linked to their respective phone numbers in the database, and the relationship between the CDRs and the customer is established through an additional table.

    ```
    +--------------------+           +------------------------+
    |    Customer        |           |    PhoneDevice         |
    +--------------------+           +------------------------+
    | - customer_id (PK) |<----------| - customer_id (FK)     |
    +--------------------+           | - phone_number (FK)    |
                                     +------------------------+
                                              |
                                              |
                                              v
                                    +--------------------------+
                                    | Call Detail Record (CDR) |
                                    +--------------------------+
                                    | - phone_number (PK)      |
                                    | - call_duration          |
                                    | - timestamp              |
                                    +--------------------------+
    ```

In our previous Customer and Service example, we show below how the data could also be stored using a non-hierarchical schema:

!!! success "Example: Customer and Services - From Hierarchical to Non-Hierarchical Schema"

    The Customer and Service data can be modeled using a **one-to-many** relationship, where each Customer may have multiple Services.  
    Each Service, however, is associated with only one Customer through a junction table called **CustomerService**, which stores information about a specific use of the service by that customer.
    
    ```
    +--------------------+             +-------------------------+
    |   Customer         |             |   CustomerService       |
    +--------------------+             +-------------------------+
    | - customer_id (PK) |<------------| - customer_id (FK)      |
    +--------------------+             | - used_service_id (FK)  |
                                       +-------------------------+
                                              |
                                              |
                                              v
                                       +------------------------+
                                       |   Service              |
                                       +------------------------+
                                       | - used_service_id (PK) |
                                       | - type                 |
                                       | - month                |
                                       | - amount               |
                                       +------------------------+
    ```

In this case, the data need to be transformed into a hierarchical schema compatible with Khiops requirements using data management.
Note that, in some cases, the Khiops tool itself can be used for such data management tasks, as described below for our previous Customer and Service example.

!!! success "Example: Customer and Services - Data Management to Transform Data to a Hierarchical Schema"

    Let us first focus on building the Service data table file according to the hierarchical schema requirements.

    We describe the two tables, Service and CustomerService, using a Khiops dictionary with a star schema, featuring a 0-1 relationship between the service and its customer.

    ```kdic
    // Temporary dictionary used to transform the available data into the Service format of the conceptual schema
    Dictionary Service (used_service_id)
    {
        Categorical used_service_id;
        // Get customer_id from the related CustomerService
        Categorical customer_id = GetValueC(customerService, customer_id); 
        Categorical type;
        Date month;
        Numerical amount;

        // Customer service related to the service
        // Only one customer is linked to the service
        Unused Entity(CustomerService) customerService;
    };

    // Temporary dictionary used to link services with their customers
    Dictionary CustomerService (used_service_id)
    {
        Categorical used_service_id;
        Categorical customer_id; 
    };
    ```
    We then process the data through the following steps:

    - Sort the `Service` and `CustomerService` data tables by their `used_service_id` key.
    
    - Deploy `Service` to create a new Service data table with `customer_id` as the key, instead of `used_service_id`.
    
    - Sort the resulting data table by `customer_id`.

    This process yields a Service data table that complies with the hierarchical schema requirements of Khiops.
