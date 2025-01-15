

This section introduces the use of dictionaries to easily implement the data-management steps of a typical datascience project, where the training data consists of a single table. For full documentation, please refer to the dictionaries [reference page][reference_page]. 


[reference_page]:../api-docs/kdic/numerical-comparisons.md

## Data Description 

One of the very first steps in data management is to **specify the types of each variable** in the training table, to ensure that they will be processed correctly in the rest of the pipeline. 

In prototyping, the usual practice of data scientists is to first load data into memory (e.g. as a Pandas Dataframe) and check the types automatically inferred. While this approach works for small datasets, it becomes inefficient for large scale datasets in production contexts. This is where Khiops dictionaries offer a much more efficient alternative.

A dictionary is a standalone file that specifies variable types and is read alongside the data during processing. **This eliminates the need to load data into memory upfront and enables advanced features** such as:

- I/O optimization;
- Out-of-core processing for handling datasets that exceed memory limits;
- Distributed processing for scaling across multiple machines.


Additionally, **dictionaries enable robust error handling**. By providing a data specification beforehand, Khiops can:

- **Replace on the fly unreadable values with missing values** (which Khiops can leverage effectively to extract meaningful insights, as shown in this [tutorial][no-data-cleaning]);
- **Ignore records with an incorrect number of fields**, avoiding column shifts and ensuring consistent data.

[no-data-cleaning]: ../tutorials/Notebooks/No_data_Cleaning.ipynb

This approach allows Khiops to process even poor-quality data sources reliably, while preserving the integrity and value of subsequent computations.

Here’s an example of a dictionary for the Iris dataset:

!!! success "Example: A simple dictionary for the Iris dataset"
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

- `Iris` indicates the name of the dictionary; 
- `SepalLength`, `SepalWidth` ... `Class` indicate variable names; 
- The keywords `Numerical` and `Categorical` define the corresponding variable types. 

**Dictionaries also enable advanced and flexible management of time variables**, with support for numerous types (i.e. Date, Time, Timestamp, TimestampTZ, and custom time format). Detailed descriptions of these types are provided on the dictionary [reference page][reference_page]. 

### Programmatic Manipulation with the Core API

Khiops dictionaries can be manipulated programmatically using the Khiops Python library, using the Core API. This includes checking the consistency of a dataset given a dictionary.

!!! example "Example: Checking a database using the Core API"
    ```python
    # Imports
    import os
    from khiops import core as kh

    # Set the file paths
    dictionary_file_path = os.path.join(kh.get_samples_dir(), "Iris", "Iris.kdic")
    data_table_path = os.path.join(kh.get_samples_dir(), "Iris", "Iris.txt")
    log_file = os.path.join("kh_samples", "check_database", "check_database.log")

    # Check the database
    kh.check_database(
    dictionary_file_path,
    "Iris",
    data_table_path,
    log_file_path=log_file,
    max_messages=50,
    )
    ```

Khiops also offers **automatic type extraction** from the training data file, as shown in the following example: 

!!! example "Example: Building a dictionary from a data table"
    ```python
    # Imports
    import os
    from khiops import core as kh

    # Set the file paths
    data_table_path = os.path.join(kh.get_samples_dir(), "Iris", "Iris.txt")
    dictionary_name = "AutoIris"
    dictionary_file_path = os.path.join(
        "kh_samples", "build_dictionary_from_data_table", "AutoIris.kdic"
    )

    # Create the dictionary from the data table
    kh.build_dictionary_from_data_table(
        data_table_path, dictionary_name, dictionary_file_path
    )
    ```



## Filtering out-of-scope variables

Another important step in data management is to define the scope of the analysis. Often, the available data contains variables irrelevant to the task at hand, making it necessary to filter out these out-of-scope variables. In the case of single-table training data, this involves selecting only the variables relevant to the analysis and ignoring the rest.  

Rather than loading the entire dataset into memory and manually dropping unnecessary columns, as is common in small-scale prototyping, dictionaries enable a more efficient approach. Khiops directly filters out unwanted variables during the data reading phase. By specifying these variables as `Unused` in the dictionary, only the relevant columns are loaded into memory, regardless of the dataset size. This avoids excessive RAM usage and simplifies workflows, especially when trial-and-error is needed during data preparation.

Using dictionaries also minimizes storage overhead. Instead of versioning large datasets for each modification, you can simply version the lightweight dictionary file, which encodes all filtering logic. This is particularly cost-effective in cloud environments where storage can be expensive.

The following example shows how the `Unused` keyword can be used in dictionaries to filter irrelevant variables:

!!! success "Example: Using the `Unused` keyword in a dictionary"
    ```kdic
    Dictionary	Iris
    {
    Unused Numerical	SepalLength	;
    Unused Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;	
    };
    ```
In this example, the variables `SepalLength` and `SepalWidth` are marked as `Unused`, meaning they will not be loaded into memory. Only the columns `PetalLength`, `PetalWidth`, and `Class` will be processed.

## User-defined Variables

In many cases, raw data stored in databases does not align with business experts’ understanding. This occurs because the data often lacks the transformations needed to reflect domain knowledge. A crucial step in data management is translating this knowledge into manually defined variables calculated from the raw data. For example, in a medical application, a variable such as the body mass index (BMI) can be derived from a patient’s height and weight.    

Typically, data scientists handle this by loading the entire dataset into memory and manually calculating these variables within tools like Pandas. While effective for small-scale prototyping, this approach is resource-intensive, requiring substantial RAM and storage, especially when numerous trial-and-error iterations are performed during feature engineering. Data versioning also becomes cumbersome, as changes must be tracked across multiple files and scripts.

For industrial-scale projects, dictionaries provide an efficient and scalable alternative. User-defined variables are calculated on the fly when the raw data is read, reducing memory overhead and eliminating the need for precomputed transformations. Additionally, since the entire data transformation flow is encoded within the dictionary, versioning is limited to a single text file, which can be managed by `git`.

The following dictionary example shows the calculation of a user-defined variable representing the area of sepals, in the Iris dataset: 

!!! success "Example: Calculating a user-defined variable"
    ```kdic
    Dictionary	Iris
    {
        Numerical	SepalLength	;
        Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Numerical	SepalArea = Product(SepalLength,SepalWidth);
        Categorical	Class	;	
    };
    ```

- As previously, the field `Iris` indicates the name of the dictionary; 
- And the fields `SepalLength`, `SepalWidth` ... `Class` indicate variable names;
- The primitive `Product` is used to calculate the user-defined variable; 
- Finally, `SepalLength`, `SepalWidth` correspond to the operands of the primitive, which can either be variables names, constant values, or results of other primitives.

Khiops offers a highly expressive data transformation language, making it easy to define user-defined variables. An exhaustive list of available primitives is available on the [reference page][reference_page].

For cases requiring numerous user-defined variables, the Core API allows programmatic addition of these variables to a dictionary, as shown in the following example:

!!! example "Add user-defined variables programmatically using the core API"
    ```python
    import os
    from khiops import core as kh

    # Set path to the dictionary
    dictionary_file_path = os.path.join(kh.get_samples_dir(), "Iris", "Iris.kdic")

    # Load the learning dictionary object
    domain = kh.read_dictionary_file(dictionary_file_path)
    dictionary = domain.get_dictionary("Iris")

    # Add 10 unused supplemental numerical variables to the learning dictionary
    number_of_supplemental_variables = 10
    for variable_index in range(1, number_of_supplemental_variables + 1):
        supplemental_variable = kh.Variable()
        supplemental_variable.name = "SupplementalVariable" + str(variable_index)
        supplemental_variable.type = "Numerical"
    supplemental_variable.used = False
    dictionary.add_variable(supplemental_variable)
    ```

## Example Selection 

Another possibility for defining the scope of an analysis involves selecting a subset of training examples (i.e. the rows of the dataset). For instance, when building a model to predict unemployment risk, the training dataset should exclude retirees and minors, focusing only on the working population.

Khiops makes example selection efficient and scalable, even for large datasets. By defining a selection criterion directly in the dictionary, **filtering is done on the fly** during data processing, avoiding the need to load the entire dataset into memory.

For example, in the Iris dataset, rows where the Class is “Iris-setosa” can be excluded by adding a user-defined selection variable to the dictionary:


!!! success "Example: Using a selection variable in a dictionary"
    ```kdic
    Dictionary	iris
    {
        Numerical	SepalLength;
        Numerical	SepalWidth;
        Numerical	PetalLength;
        Numerical	PetalWidth;
    Unused  Numerical Selection = NEQc(Class, "Iris-setosa"); // exclude the "Iris-setosa" class from the training set 
        Categorical	Class;	
    };
    ```

- `Selection` is a user-defined variable calculated with the NEQc (not-equal-to constant) primitive;
- The `Unused` keyword ensures the variable is not part of the analysis but is used only for filtering the examples.

Once defined, this selection variable—containing 0s and 1s—can be exploited programmatically during training with the Khiops Python Core API. The following example demonstrates how to filter examples by retaining only rows where the selection variable equals 1 while training a predictive model:

!!! example "Train a predictive model using the core API"
    ```python
    # Imports
    import os
    from khiops import core as kh

    # Set the file paths
    dictionary_file_path = os.path.join(kh.get_samples_dir(), "Iris", "Iris.kdic")
    data_table_path = os.path.join(kh.get_samples_dir(), "Iris", "Iris.txt")
    results_dir = os.path.join("kh_samples", "train_predictor")

    # Train the predictor
    kh.train_predictor(
        dictionary_file_path,
        "iris",
        data_table_path,
        "Class",
        results_dir,
        max_trees=0,
        selection_variable="Selection",
        selection_value=1
    )   
    ```



