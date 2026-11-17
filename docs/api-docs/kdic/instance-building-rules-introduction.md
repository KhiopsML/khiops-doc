#  Instance building rules

An **instance** is an in-memory representation of an entity described by a dictionary, populated with its variable values and related entities or tables. For details, see [`In-Memory Instances`](dictionary-files.md#in-memory-instances).

In a multi-table schema, instances can be constructed and populated from records in data files.

- The instance is filled with variables of the correct type according to its Khiops dictionary, with each variable mapped to the corresponding file column based on its name.

- The multi-table instances are linked in memory according to the schema, with a 0-1 relationship for Entity variables and a 0-n relationship for Table variables.

Standard table derivation rules enable the creation of new tables in memory by selecting, extracting, or reorganizing existing instances linked to input records.
Examples include rules such as TableSelection, TableExtraction, TableSort, and TableUnion, which are part of the [`Table Management Rules`](../kdic/table-management-rules.md).

Instance building rules go further by allowing you to modify data representations through the creation of new in-memory instances that are **not stored in data files**, by defining a **target dictionary** that specifies the schema. 
For example, this enables creating instances by selecting a subset of variables or exploring new data representations for time series, such as the power spectrum or autocorrelation.


Note that:

- As with any dictionary, target dictionaries may contain unused variables or, conversely, new variables derived from existing ones.

- Unlike instances read from data files, which are retrieved using dictionary keys, instances created by instance-building rules **do not require keys**; any specified key fields are treated like other target fields.

- Target dictionaries cannot be `Root`, as this is reserved for external tables.
    
- Instance creation rules can only be used to define new variables of type Entity or Table, with the target dictionary specified in the variable declaration. These rules cannot be used directly as operands of other rules.