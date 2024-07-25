

This section introduces the use of dictionaries to easily implement the data-management steps of a typical datascience project, where the training data consists of a single table. For full documentation, please refer to the dictionaries [reference page][reference_page]. 


[reference_page]:../api-docs/kdic/numerical-comparisons.md

## Data Description 

One of the very first steps in data management is to specify the types of each variable in the training table, to ensure that they will be processed correctly in the rest of the pipeline. 

For the purposes of prototyping, the usual practice of data scientists is to first load the data into memory, in a Pandas Dataframe or equivalent. Then, they check the types that have been extracted automatically.  

In a production context, dictionaries offer a much more efficient alternative, since there's no need to load data into memory. The dictionary itself is a file specifying types. It is read by Khiops at the same time as the training data, with strategies for managing very large volumes of data, including I/O optimization, out-of-core processing and distributed processing. 

In addition, an advanced algorithm for detecting data formatting errors takes advantage of the dictionary, as it provides the data specification beforehand. Thus, unreadable values are replaced by missing values on the fly, and records with an incorrect number of fields are ignored (there are no column shifts). Thanks to dictionaries, Khiops is able to read poor-quality data sources, while guaranteeing the correct execution of the processing that follows.    

Here's an example of a dictionary used to specify the types of variables in the Iris dataset. Dictionary syntax is very compact, with the meaning of each attribute depending on its position.    

!!! success "First example of dictionary file"
    ```kdic
    Dictionary	iris
    {
        Numerical	SepalLength	;
        Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;	
    };
    ```

- The field "*iris*" indicates the name of the dictionary; 
- Fields at "*SepalLength, SepalWidth ... Class*" indicate variable names; 
- The keywords "*Numerical*" and "*Categorical*" indicate the corresponding variable types. 

Dictionaries also enable advanced and flexible management of time data, with support for numerous types *(i.e. Date, Time, Timestamp, TimestampTZ, and custom time format)*. Detailed descriptions of these types are provided on the dictionary [reference page][reference_page]. 

Khiops dictionaries can be manipulated programmatically through the Python language, using the Core API. The following example shows how the matching of a data table and the dictionary that describes it can be verified: 

!!! example "Check database using the Core API"
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

Khiops also offers automatic type extraction from the training data file, as shown in the following example: 

!!! example "Build dictionary from data table using the core API"
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



## Filtering Out-of-scope Variables

Another important step in data management is to define the scope of the analysis to be carried out. Frequently, the data available is too extensive, and only part of it is relevant to the analysis. In the very simple case of single-table training data discussed here, this step takes the form of filtering out variables that fall outside the scope of the analysis.  

As before, the usual practice of datascientists is to load the entire data set into memory, then eliminate unwanted variables. This practice assumes that the data is not too large with regard to the available RAM memory, and with regard to the maximum size managed by the Pandas Dataframe (or equilavent). In addition, the data scientist often needs to make several trial/error runs for this filtering, and may be tempted to record different versions of the data. This practice has the effect of overloading storage space, and can be very costly in cloud environments.  

In an industrial context, where volumes of data can be very large and storage space needs to be carefully managed, dictionaries are an excellent way of filtering out unwanted variables on the fly. Basically, only useful columns from the input file are loaded into memory by Khiops. In addition, dictionaries are very light to be versioned, which is much more economical than versioning data. 

The following example shows how the **Unused** keyword can be used in dictionaries to filter out unwanted variables:

!!! success "The Unused keyword"
    ```kdic
    Dictionary	iris
    {
    Unused Numerical	SepalLength	;
    Unused Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;	
    };
    ```

And the following example shows how this dictionary can be used via the Core API to learn a predictive model (in this case, a classifier) without Python even needing to load the data into memory: 

!!! example "Train a predictor model using the core API"
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
        "Iris",
        data_table_path,
        "Class",
        results_dir,
        max_trees=0,
    )
    ```

## User-defined Variables

In many situations, data stored in databases is difficult for business experts to understand. This raw data does not always accurately reflect their business knowledge. An important step in data management is to express the experts' knowledge by manually defining new variables calculated from the raw data. For example, in a medical application, the body mass index can be calculated from the patient's height and weight.       

Once again, the common practice of datascientists is to load the entire data set into memory, then calculate the new variables transcribing the business knowledge and add them to the Pandas Dataframe (or equivalent) stored in memory. This practice is very costly, as it involves intensive use of RAM and storage space, especially if the user makes a large number of trial-error runs during the feature engineering stage. Data versioning becomes a big deal.  

When industrializing datascience projects, it is recommended to use dictionaries to add user-defined variables to the raw data. These new variables are calculated on the fly when the data file is read. Versioning is always limited to the dictionary itself, since it encodes the entire data transformation flow, from raw data to trained model predictions.  

The following dictionary example shows the calculation of a user-defined variable representing the area of sepals, in the Iris dataset: 

!!! success "User-defined variable"
    ```kdic
    Dictionary	iris
    {
        Numerical	SepalLength	;
        Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Numerical	SepalArea = Product(SepalLength,SepalWidth);
        Categorical	Class	;	
    };
    ```

- As previously, the field "*iris*" indicates the name of the dictionary; 
- And the fields "*SepalLength, SepalWidth ... Class*" indicate variable names;
- The primitive "*Product*" is used to calculate the user-defined variable; 
- Finally, "*SepalLength, SepalWidth*" correspond to the operands of the primitive, which can either be variable names, or results of others primitive.     

Khiops implements a highly expressive data transformation language, for easy construction of user-defined variables. An exhaustive description of available primitives is provided on the [reference page][reference_page]. 
In cases where numerous user-defined variables need to be specified, it is possible to use the Core API to add them to a dictionary programmatically, as shown in the following example:   

**TODO Vladimir**

## Example Selection 

Another possibility for defining the scope of an analysis is to select a certain part of the training examples (i.e. the rows of the training dataset). For instance, a model designed to predict the risk of unemployment must be trained on the working population, excluding retirees and miners. 

As mentioned above, the usual practices of datascientists are very costly in the case of large amounts of data. The pitfall to avoid is always the same: loading the entire data set into RAM, before eliminating unwanted training examples... 

In an industrial context, and in the face of big data, the selection of examples must be carried out on the fly using a dictionary. The first step is to add a user-defined variable to serve as a selection variable, and then run Khiops to actually perform the selection. 

Here's an example of a dictionary used to select examples from the iris dataset, which do not belong to the *Iris-Setosa* class.

!!! success "User-defined Selection Variable"
    ```kdic
    Dictionary	iris
    {
        Numerical	SepalLength;
        Numerical	SepalWidth;
        Numerical	PetalLength;
        Numerical	PetalWidth;
    Unused  Numerical Selection = NEQc(Class, "Iris-setosa"); // discade the setosa class from the training set 
        Categorical	Class;	
    };
    ```

Note that the new selection variable is not actually employed in the analysis, which explains the presence of the *Unused* keyword. You'll also notice that the selection variable simply takes the form of a user-defined variable.

The following example shows how the Core API can be used to run Khiops for actual example selection:

!!! example "Train a predictor model using the core API"
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



