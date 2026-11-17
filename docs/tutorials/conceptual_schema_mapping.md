# Mapping and Transforming Schemas

While in some cases the logical schema and conceptual schema may be identical, raw data often lacks an explicit conceptual structure.  
In such situations, transforming raw data into a well-defined conceptual schema becomes essential, typically using data management tools.

Khiops dictionaries facilitate this transformation by allowing you to specify the raw data in its logical format, retaining unused variables if necessary, and then defining derivation rules to construct the conceptual schema from the logical one.

The examples below use a conceptual schema with customers and their monthly services, each described by a type, month and amount. For the basic schema, see [Conceptual, Logical, and Physical Data Models](conceptual_logical_physical_data_models.md).

The first examples reshape different input formats into this same conceptual schema. The later relational examples show distinct hierarchy mismatches and how to resolve them.

## Mapping a Conceptual Schema to a Logical Schema

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
You can then use the [`TableUnion`](../api-docs/kdic/table-management-rules.md#tableunion) rule.

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

Suppose service records are stored in separate files for each service type, with no column indicating the type.

To obtain data according to the conceptual schema, we first need to create new in-memory instances from the raw data, adding the service type to each instance.
This can be achieved using the `BuildTableAdvancedView` rule from the [`Instance Building Rules`](../api-docs/kdic/instance-building-rules-introduction.md).

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
          BuildTableAdvancedView(onlineRawServices, "online" : type);
        Unused Table(Service) retailServices =
          BuildTableAdvancedView(retailRawServices, "retail" : type);

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

To obtain data according to the conceptual schema, we first need to create an in-memory instance for each service and month.
This can be achieved using the `BuildEntity` rule from the [`Instance Building Rules`](../api-docs/kdic/instance-building-rules-introduction.md).

You can then use the `EntitySet` rule to collect all the built instances into a single table.

Note that in this example, the conceptual schema follows a star schema, while the logical schema is a single table.
The `Service` key is not needed to create these in-memory instances; it is retained to match the conceptual schema.

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

        // Raw values of amount, with one variable per service and per month
        Unused Numerical amountOnline01;
        Unused Numerical amountRetail01;
        Unused Numerical amountOnline02;
        Unused Numerical amountRetail02;
        Unused Numerical amountOnline03;
        Unused Numerical amountRetail03;
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
The target dictionary maps JSON to Khiops: an object provides values for an instance, an object assigned to an `Entity` variable describes a related instance, and an array assigned to a `Table` variable creates one instance per element.

Note that, as in the previous example, the conceptual schema follows a star schema, while the logical schema is a single table.

!!! success "Example: Building a table from JSON data"

    In the following example, `jsonServicesData` contains a JSON array of objects. The `Service` dictionary describes each object's fields, and `BuildTableFromJson` creates one `Service` instance for each object.

    ```kdic
    Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Categorical name;
        Numerical age;
        Table(Service) services = BuildTableFromJson(jsonServicesData);

        // Raw values of services stored in a JSON field
        Unused Text jsonServicesData;
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

    If `jsonServicesData` contains the following JSON array, the `services` Table contains six `Service` instances, one for each object in the array.

    ```json
    [{"customer_id":"Id0000","type":"online","month":"2026-01-01","amount":1500},{"customer_id":"Id0000","type":"retail","month":"2026-01-01","amount":2000},{"customer_id":"Id0000","type":"online","month":"2026-02-01","amount":1600},{"customer_id":"Id0000","type":"retail","month":"2026-02-01","amount":2100},{"customer_id":"Id0000","type":"online","month":"2026-03-01","amount":1700},{"customer_id":"Id0000","type":"retail","month":"2026-03-01","amount":2200}]
    ```

    The same array is formatted below for clarity:

    ```json
    [
      {
        "customer_id": "Id0000",
        "type": "online",
        "month": "2026-01-01",
        "amount": 1500
      },
      {
        "customer_id": "Id0000",
        "type": "retail",
        "month": "2026-01-01",
        "amount": 2000
      },
      {
        "customer_id": "Id0000",
        "type": "online",
        "month": "2026-02-01",
        "amount": 1600
      },
      {
        "customer_id": "Id0000",
        "type": "retail",
        "month": "2026-02-01",
        "amount": 2100
      },
      {
        "customer_id": "Id0000",
        "type": "online",
        "month": "2026-03-01",
        "amount": 1700
      },
      {
        "customer_id": "Id0000",
        "type": "retail",
        "month": "2026-03-01",
        "amount": 2200
      }
    ]
    ```

### Customer and Services in One JSON Field

Unlike the previous example, where only the services array is stored as JSON, here each input record contains a single field, `jsonData`. Its JSON value is an object containing the customer ID, customer attributes, and services. Since the ID is inside this JSON value rather than a separate input field, the input dictionary has no key. The JSON value is parsed with [`BuildEntityFromJson`](../api-docs/kdic/json-extraction-rules.md#buildentityfromjson), and the conceptual customer variables and service table are then derived using [entity rules](../api-docs/kdic/entity-rules.md).

!!! success "Example: Mapping a Customer and Services from One JSON Field"

    ```kdic
    Dictionary Customer
    {
        Categorical customer_id = GetValueC(jsonCustomer, customer_id);
        Categorical name = GetValueC(jsonCustomer, name);
        Numerical age = GetValue(jsonCustomer, age);
        Table(Service) services = GetTable(jsonCustomer, services);

        // Raw customer and services stored in a JSON field
        Unused Text jsonData;

        // Intermediate entity built from the JSON object
        Unused Entity(JsonCustomer) jsonCustomer = BuildEntityFromJson(jsonData);
    };

    // Structure matching the JSON object in jsonData
    Dictionary JsonCustomer
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
        Date month;
        Numerical amount;
    };
    ```

    The `Service` key matches the conceptual dictionary, but is not needed to create or link these in-memory instances. Each service's `customer_id` is read from its JSON object, not copied from the customer.

    For example, the single `jsonData` field of an input record could contain the following JSON object, formatted here for readability:

    ```json
    {
      "customer_id": "Id0000",
      "name": "Alex Smith",
      "age": 42,
      "services": [
        {"customer_id": "Id0000", "type": "online", "month": "2026-01-01", "amount": 1500},
        {"customer_id": "Id0000", "type": "retail", "month": "2026-01-01", "amount": 2000}
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
Each native secondary table's key begins with its parent table's key, so data table files sorted by their keys can be read together.
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

### Relational Database with a Many-to-Many Relationship

The Customer and Service data can be modeled using a **many-to-many** relationship, where each Customer can use multiple Services and each Service can be used by multiple Customers.
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


### Relational Databases with Non-Hierarchical Relationships

Unlike the preceding many-to-many example, this schema has a one-to-many relationship: each Customer can have multiple service usages, and each usage belongs to one Customer. Here, each row in `ServiceUsage` describes one customer's use of a service, rather than a service type. The **CustomerService** table links each usage to its customer, but the resulting keys do not meet Khiops' hierarchical requirements.

!!! success "Example: Customer and Service Usages - Non-Hierarchical Schema"

    ```
    +--------------------+             +-------------------------+
    |   Customer         |             |   CustomerService       |
    +--------------------+             +-------------------------+
    | - customer_id (PK) |<------------| - customer_id (FK)      |
    +--------------------+             | - service_usage_id (FK) |
                                       +-------------------------+
                                              |
                                              |
                                              v
                                       +---------------------------+
                                       |   ServiceUsage            |
                                       +---------------------------+
                                       | - service_usage_id (PK)   |
                                       | - type                    |
                                       | - month                   |
                                       | - amount                  |
                                       +---------------------------+
    ```

This data must be transformed into a hierarchical schema compatible with Khiops. Data management is usually needed, although Khiops itself can also perform part of the transformation, as shown below.

!!! success "Example: Transforming Service Usage Data to a Hierarchical Schema"

    Let us first focus on building the `ServiceUsage` data table file according to the hierarchical schema requirements.

    We describe the `ServiceUsage` and `CustomerService` tables using a Khiops dictionary with a star schema, featuring a 0-1 relationship between each service usage and its customer.

    ```kdic
    // Temporary dictionary used to derive customer_id for each service usage
    Dictionary ServiceUsage (service_usage_id)
    {
        Categorical service_usage_id;
        // Get customer_id from the related CustomerService
        Categorical customer_id = GetValueC(customerService, customer_id); 
        Categorical type;
        Date month;
        Numerical amount;

        // Customer associated with this service usage
        Unused Entity(CustomerService) customerService;
    };

    // Temporary dictionary used to link service usages with their customers
    Dictionary CustomerService (service_usage_id)
    {
        Categorical service_usage_id;
        Categorical customer_id; 
    };
    ```
    We then process the data through the following steps:

    - Sort the `ServiceUsage` and `CustomerService` data tables by their `service_usage_id` key.

    - Deploy `ServiceUsage` to create a new data table containing the derived `customer_id`.

    - Sort the resulting data table by `customer_id`.

    The resulting table can be used with the conceptual `Service` dictionary keyed by `customer_id`, making it compatible with the Customer hierarchy.

### Telecommunications: Organizing Call Records by Customer

This example illustrates a different key-hierarchy mismatch from the service-usage example above. The relationships form a tree: each phone line belongs to a customer, and each call belongs to a phone line. However, call records identify the phone line through `phone_number`, not the customer through `customer_id`.

!!! success "Example: Relational Schema for Customers, Phone Lines, and Calls"

    For this example, assume that `PhoneLine` contains one record per phone number, identifying its customer during the period being analyzed.

    ```
    +--------------------+           +------------------------+
    |    Customer        |           |    PhoneLine           |
    +--------------------+           +------------------------+
    | - customer_id (PK) |<----------| - customer_id (FK)     |
    +--------------------+           | - phone_number (PK)    |
                                     +------------------------+
                                              |
                                              |
                                              v
                                    +--------------------------+
                                    | Call Detail Record (CDR) |
                                    +--------------------------+
                                    | - phone_number (FK)      |
                                    | - call_start             |
                                    | - call_duration          |
                                    +--------------------------+
    ```

To organize calls under each customer in Khiops, this example adds the customer ID to each call record. `PhoneLine` is used as an external table to look up the customer by phone number. Its file must be sorted by `phone_number`; the CDR file may contain multiple records for the same phone number.

!!! success "Example: Transforming Call Detail Records for Khiops"

    The temporary dictionary for the input CDR table derives `customer_id` through the external-table lookup:

    ```kdic
    Dictionary RawCall (phone_number)
    {
        Categorical phone_number;
        Timestamp call_start;
        Categorical customer_id = GetValueC(phoneLine, customer_id);
        Numerical call_duration;
        Unused Entity(PhoneLine) phoneLine[phone_number];
    };

    Root Dictionary PhoneLine (phone_number)
    {
        Categorical phone_number;
        Categorical customer_id;
    };
    ```

    We deploy `RawCall` to add `customer_id` to each call record, then sort the resulting table by `customer_id`. The table can then be used with the following dictionaries. Since `Call` is a leaf, its key need not extend the parent's key:

    ```kdic
    Root Dictionary Customer (customer_id)
    {
        Categorical customer_id;
        Table(Call) calls;
    };

    Dictionary Call (customer_id)
    {
        Categorical customer_id;
        Categorical phone_number;
        Timestamp call_start;
        Numerical call_duration;
    };
    ```

    Unlike the service-usage example, which derives the customer ID from a junction table, this example looks it up using the phone number.
