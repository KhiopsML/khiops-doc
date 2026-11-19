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

!!! note "When the available data does not match the conceptual schema"
    Real-world data often differs from the clean example shown here. The next page explores how to map between logical and conceptual schemas, with worked examples using Khiops dictionaries.
    [Explore schema mapping](conceptual_schema_mapping.md).

