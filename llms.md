# Khiops

> Khiops is an interpretable and scalable data science platform with a Python library, desktop GUI applications, and deployment tools.

This index maps the Khiops documentation and exported KNI examples to their primary tasks or subjects. Start with the overview or a tutorial, then use the API references for detailed syntax and the examples for integration guidance.

## Python development and tutorials

Install the Python library, follow hands-on tutorials, and consult the full Python API reference (Core and scikit-learn).

- [Install with pip](https://khiops.org/markdown/setup/pip.md): Install the Khiops Python library and its runtime dependencies with pip in a virtual environment on Linux, macOS, or Windows.
- [Install with Conda](https://khiops.org/markdown/setup/conda.md): Create a Conda environment and install Khiops from conda-forge, with optional SDKs for remote cloud storage.
- [Getting started with Khiops](https://khiops.org/markdown/tutorials/introduction.md): Get oriented with Khiops, its scikit-learn and Core APIs, and the workflow from data preparation through model training and deployment.
- [Python quickstart](https://khiops.org/markdown/tutorials/quickstart.md): Train a first classification model with `KhiopsClassifier` using the scikit-learn API, then extend it to multi-table auto feature engineering and visualize the analysis report.
- [Single-table scikit-learn tutorial](https://khiops.org/markdown/tutorials/notebooks/single_table_classifier.md): Train a single-table classifier on the Iris data and inspect the basic scikit-learn workflow.
- [Multi-table scikit-learn tutorial](https://khiops.org/markdown/tutorials/notebooks/multi_table_classifier.md): Train on related tables (vehicles, users, and places) with the Accidents data, using the scikit-learn API.
- [No data preparation tutorial](https://khiops.org/markdown/tutorials/notebooks/No_data_Cleaning.md): Test Khiops on raw data containing missing values, label noise, outliers, and class imbalance, and compare it with conventional machine learning workflows.
- [Interpretable variable encoding tutorial](https://khiops.org/markdown/tutorials/notebooks/Optimal_Encoding.md): Compare Khiops target-aware, MODL-based variable encoding with conventional encoders in an interpretable machine-learning pipeline.
- [Auto feature engineering tutorial](https://khiops.org/markdown/tutorials/notebooks/Use_in_any_ML_pipeline.md): Construct features from related tables and combine Khiops auto feature engineering and parsimonious training with another learner.
- [Single-table Core API tutorial](https://khiops.org/markdown/tutorials/notebooks/single_table_classifier_core.md): Define a dictionary, then train, evaluate, and deploy a single-table classifier with the Core API using file-based Iris data.
- [Multi-table Core API tutorial](https://khiops.org/markdown/tutorials/notebooks/multi_table_classifier_core.md): Define related tables in dictionaries, then train, evaluate, and deploy a multi-table classifier with the Core API on the Accidents data.

### Python API reference

- [Multi-table learning primer](https://khiops.org/markdown/api-docs/python-api/multi_table_primer.md): Introduce multi-table learning concepts used throughout the Python API.
- [Notes](https://khiops.org/markdown/api-docs/python-api/notes.md): Additional notes on the Khiops Python API.

#### Core submodule

- [analysis_results](https://khiops.org/markdown/api-docs/python-api/core/analysis_results.md): Classes to access Khiops JSON analysis reports (preparation, modeling, evaluation).
- [api](https://khiops.org/markdown/api-docs/python-api/core/api.md): Core API functions to execute Khiops tasks: train, evaluate, deploy, and more.
- [coclustering_results](https://khiops.org/markdown/api-docs/python-api/core/coclustering_results.md): Classes to access Khiops coclustering JSON report results.
- [dictionary](https://khiops.org/markdown/api-docs/python-api/core/dictionary.md): Classes to manipulate Khiops dictionary files programmatically.
- [exceptions](https://khiops.org/markdown/api-docs/python-api/core/exceptions.md): Khiops Python exception classes.
- [helpers](https://khiops.org/markdown/api-docs/python-api/core/helpers.md): Helper functions for specific and/or advanced treatments.
- [Samples](https://khiops.org/markdown/api-docs/python-api/samples/samples.md): Core API code samples covering single-table, multi-table, and coclustering use cases.
- [utility tools](https://khiops.org/markdown/api-docs/python-api/tools/index.md): Miscellaneous command-line utility tools distributed with the Khiops Python library.

#### sklearn submodule

- [estimators](https://khiops.org/markdown/api-docs/python-api/sklearn/estimators.md): Scikit-learn estimator classes (KhiopsClassifier, KhiopsRegressor, KhiopsEncoder, KhiopsCoclustering).
- [helpers](https://khiops.org/markdown/api-docs/python-api/sklearn/helpers.md): General helper functions for the scikit-learn API.
- [Samples](https://khiops.org/markdown/api-docs/python-api/samples/samples_sklearn.md): Scikit-learn API code samples covering single-table, multi-table, and coclustering use cases.

### Python tutorials

- [Tutorials overview](https://khiops.org/markdown/api-docs/python-api/tutorials/index.md): Index of Python API tutorials for the Core and scikit-learn APIs.
- [Core Basics 1](https://khiops.org/markdown/api-docs/python-api/tutorials/Core%20Basics%201%20-%20Train%2C%20Evaluate%20and%20Deploy%20a%20Classifier.md): Core API tutorial to train, evaluate, and deploy a classifier.
- [Core Basics 2](https://khiops.org/markdown/api-docs/python-api/tutorials/Core%20Basics%202%20-%20Train%20a%20Classifier%20on%20a%20Star%20Multi-Table%20Dataset.md): Core API tutorial to train a classifier on a star-schema multi-table dataset.
- [Core Basics 3](https://khiops.org/markdown/api-docs/python-api/tutorials/Core%20Basics%203%20-%20Train%20a%20Classifier%20on%20a%20Snowflake%20Multi-Table%20Dataset.md): Core API tutorial to train a classifier on a snowflake-schema multi-table dataset.
- [Core Basics 4](https://khiops.org/markdown/api-docs/python-api/tutorials/Core%20Basics%204%20-%20Train%20a%20Coclustering.md): Core API tutorial to train a coclustering model.
- [Sklearn Basics 1](https://khiops.org/markdown/api-docs/python-api/tutorials/Sklearn%20Basics%201%20-%20Train%2C%20Evaluate%20and%20Deploy%20a%20Classifier.md): Scikit-learn API tutorial to train, evaluate, and deploy a classifier.
- [Sklearn Basics 2](https://khiops.org/markdown/api-docs/python-api/tutorials/Sklearn%20Basics%202%20-%20Train%20a%20Classifier%20on%20a%20Star%20Multi-Table%20Dataset.md): Scikit-learn API tutorial to train a classifier on a star-schema multi-table dataset.
- [Sklearn Basics 3](https://khiops.org/markdown/api-docs/python-api/tutorials/Sklearn%20Basics%203%20-%20Train%20a%20Classifier%20on%20a%20Snowflake%20Multi-Table%20Dataset.md): Scikit-learn API tutorial to train a classifier on a snowflake-schema multi-table dataset.
- [Sklearn Basics 4](https://khiops.org/markdown/api-docs/python-api/tutorials/Sklearn%20Basics%204%20-%20Train%20a%20Coclustering.md): Scikit-learn API tutorial to train a coclustering model.

## Data science and foundations

Understand the MODL formalism and the statistical concepts behind Khiops' automated data preparation and modeling.

- [What makes Khiops different](https://khiops.org/markdown/learn/understand.md): Explain Khiops as end-to-end AutoML, covering automated cleaning, encoding, feature engineering, and parsimonious learning through the MODL formalism, plus unsupervised methods such as histograms and coclustering.
- [MODL formalism](https://khiops.org/markdown/learn/modl.md): Learn how MODL uses model selection, empirical risk, and regularization to provide hyperparameter-free and interpretable learning.
- [Optimal encoding](https://khiops.org/markdown/learn/preprocessing.md): Understand supervised numerical discretization and categorical grouping, including the model-selection criteria used to encode variables.
- [Auto feature engineering](https://khiops.org/markdown/learn/autofeature_engineering.md): Learn how Khiops turns multi-table relationships into supervised aggregate features through MODL-based propositionalization, and builds parameter-free MODL decision trees as a further feature-engineering step.
- [Parsimonious training](https://khiops.org/markdown/learn/learning_models.md): Understand how Khiops selects and weights a compact subset of variables or aggregates instead of fitting every available feature.
- [Optimal histograms](https://khiops.org/markdown/learn/histograms.md): Learn how adaptive, multi-scale histograms reveal structure, outliers, and heavy-tailed behavior without fixed-width bins.
- [Coclustering](https://khiops.org/markdown/learn/coclustering.md): Understand how coclustering groups rows and columns together to expose dependencies in contingency tables and other data grids.
- [Coclustering individual variables](https://khiops.org/markdown/learn/coclustering_indi_var.md): Placeholder for future documentation about coclustering individual variables; this page currently contains no detailed guidance.
- [Hardware adaptation](https://khiops.org/markdown/learn/hardware_adaptation.md): Learn how Khiops adapts data-grid algorithms to RAM and CPU limits, including divide-and-conquer and MPI-based distributed execution.
- [Bibliography](https://khiops.org/markdown/references.md): Browse Khiops publications by topic and find citation information for the main scientific work.

## Khiops dictionaries

Learn the dictionary (KDIC) language used to describe data and define derivation rules, from tutorials to the full rule reference.

- [Start using dictionaries](https://khiops.org/markdown/tutorials/kdic_intro.md): Learn how the Core API and Khiops dictionaries describe data, prepare inputs, deploy models, and support scalable processing.
- [Single-table dictionary concepts](https://khiops.org/markdown/tutorials/kdic_single_table.md): Describe a single-table dataset with a dictionary, covering data typing, variable filtering, user-defined variables, and example selection for file-based, out-of-core processing.
- [Multi-table dictionary concepts](https://khiops.org/markdown/tutorials/kdic_multi_table.md): Model relational data with dictionaries, including star and snowflake schemas and Entity and Table relationships.

### Dictionary files and limits

- [Database files](https://khiops.org/markdown/api-docs/kdic/database-files.md): Specify Khiops data-file delimiters, quoting, encoding, missing values, typed formats, the sparse data-file format, and ordering requirements for multi-table data.
- [Dictionary files](https://khiops.org/markdown/api-docs/kdic/dictionary-files.md): Define table schemas, variable types, metadata, derivation rules, and selected variables for analysis or deployment.
- [Dictionary technical limits](https://khiops.org/markdown/api-docs/kdic/limits.md): Record KDIC numeric precision, string lengths, line encoding, character encodings, memory and scalability limits, and known problems.

### Basic expression rules

- [Numerical comparisons](https://khiops.org/markdown/api-docs/kdic/numerical-comparisons.md): Evaluate numerical equality, inequality, and ordering comparisons, including the `#Missing` value.
- [Categorical comparisons](https://khiops.org/markdown/api-docs/kdic/categorical-comparisons.md): Evaluate categorical equality, inequality, and ordering comparisons, returning numerical Boolean results.
- [Logical operators](https://khiops.org/markdown/api-docs/kdic/logical-operators.md): Combine numerical expressions with `And`, `Or`, and `Not`, and branch with typed `If` and `Switch` operators, where zero is false and nonzero or missing is true.
- [Data copy and conversion](https://khiops.org/markdown/api-docs/kdic/data-copy-and-conversion.md): Copy values of any type between variables, convert between numerical and categorical values, and recode missing values.
- [Math rules](https://khiops.org/markdown/api-docs/kdic/math-rules.md): Apply arithmetic, rounding, exponential, logarithmic, trigonometric, and other numerical functions.
- [String rules](https://khiops.org/markdown/api-docs/kdic/string-rules.md): Manipulate categorical and string-like values with length, substring, token, case, search, replace, regular-expression, concatenation, hashing, and encryption rules.
- [Text rules](https://khiops.org/markdown/api-docs/kdic/text-rules.md): Convert, load, and manipulate `Text` values with the text-specific rules supported by the dictionary language.
- [Date rules](https://khiops.org/markdown/api-docs/kdic/date-rules.md): Parse, format, and extract components from `Date` values, including year, month, day, day-of-year, weekday, and decimal year.
- [Time rules](https://khiops.org/markdown/api-docs/kdic/time-rules.md): Parse, format, and extract hours, minutes, seconds, and fractional seconds from `Time` values.
- [Timestamp rules](https://khiops.org/markdown/api-docs/kdic/timestamp-rules.md): Combine date and time operations and convert timestamp values to components such as dates, times, decimal years, or absolute seconds.
- [TimestampTZ rules](https://khiops.org/markdown/api-docs/kdic/timestamp-tz-rules.md): Parse and convert timezone-aware ISO 8601 timestamps, including local-time and UTC representations.

### Multi-table rules

- [Multi-table rules introduction](https://khiops.org/markdown/api-docs/kdic/multi-table-rules-introduction.md): Introduce `Entity` (0-1) and `Table` (0-n) relationships and the rules that extract values from related records.
- [Entity rules](https://khiops.org/markdown/api-docs/kdic/entity-rules.md): Check whether a related entity exists and retrieve fields from a 0-1 related record.
- [Table rules](https://khiops.org/markdown/api-docs/kdic/table-rules.md): Aggregate 0-n related records with count, mean, mode, standard deviation, minimum, maximum, sum, and distinct-count rules.
- [Table management rules](https://khiops.org/markdown/api-docs/kdic/table-management-rules.md): Access, extract, select, sort, and combine (union, intersection, difference) records in related tables before downstream aggregation.
- [Table partition rules](https://khiops.org/markdown/api-docs/kdic/table-partition-rules.md): Create sparse partitions of secondary-table variables and compute statistics for each partition.
- [Table block rules](https://khiops.org/markdown/api-docs/kdic/table-block-rules.md): Aggregate blocks of secondary-table variables with block-level distinct-count, entropy, mode, mean, standard deviation, median, minimum, maximum, and sum rules.
- [TextList rules](https://khiops.org/markdown/api-docs/kdic/text-list-rules.md): Work with lists of `Text` values using construction, sizing, indexing, and concatenation rules, and aggregate text values across secondary tables.

### Structures, preparation, and deployment rules

- [Technical structures](https://khiops.org/markdown/api-docs/kdic/structures-introduction.md): Describe internal deployment structures such as vectors, hash maps, data grids, partitions, statistics, classifiers, regressors, and coclustering models.
- [Vector rules](https://khiops.org/markdown/api-docs/kdic/vector-rules.md): Create and access categorical or numerical vectors, including vectors associated with secondary tables.
- [Hash map rules](https://khiops.org/markdown/api-docs/kdic/hash-map-rules.md): Create and query categorical or numerical key-value maps for efficient recoding.
- [Data preparation rules](https://khiops.org/markdown/api-docs/kdic/data-preparation-rules.md): Represent preparation models with data grids, partitions, frequencies, and grid statistics.
- [Recoding rules](https://khiops.org/markdown/api-docs/kdic/recoding-rules.md): Map values through partitions and groups to obtain cell indexes, identifiers, labels, conditional data-grid statistics, and normalized value ranks.
- [Predictor rules](https://khiops.org/markdown/api-docs/kdic/predictor-rules.md): Deploy Naive Bayes and Selective Naive Bayes classifiers, regressors, and rank regressors, and compute predicted target values, probabilities, and ranks.
- [Interpretation rules](https://khiops.org/markdown/api-docs/kdic/interpretation-rules.md): Compute classifier variable and part contributions for interpreting individual predictions.
- [Reinforcement rules](https://khiops.org/markdown/api-docs/kdic/reinforcement-rules.md): Apply lever variables to reinforce classifier decisions and inspect reinforcement scores.
- [Coclustering rules](https://khiops.org/markdown/api-docs/kdic/coclustering-rules.md): Deploy coclustering grids and retrieve predicted parts, distances, and frequencies.

### Block and sparse-data rules

- [Block and sparse-data introduction](https://khiops.org/markdown/api-docs/kdic/intro-block.md): Introduce sparse data and uniform variable blocks, including integer or categorical variable keys.
- [Basic sparse rules](https://khiops.org/markdown/api-docs/kdic/basic-sparse-rules.md): Copy sparse variable blocks and retrieve values from sparse entities.
- [Text sparse rules](https://khiops.org/markdown/api-docs/kdic/text-sparse-rules.md): Tokenize text and text lists into sparse blocks of words, byte n-grams, or tokens for dictionary processing.
- [Preparation sparse rules](https://khiops.org/markdown/api-docs/kdic/preparation-sparse-rules.md): Apply data-preparation and recoding structures to sparse variable blocks.

## Installation, deployment, and integration

Install Khiops applications and drivers, and run or deploy Khiops in Docker, Kubernetes, batch, or cloud-storage environments.

- [Installation overview](https://khiops.org/markdown/setup/index.md): Compare Khiops installation paths for the Python library, desktop applications, visualization, KNI, and cloud drivers across supported platforms.
- [Install Khiops with pip](https://khiops.org/markdown/setup/pip.md): Install the Khiops Python library and its runtime dependencies with pip in a virtual environment on Linux, macOS, or Windows.
- [Install Khiops with Conda](https://khiops.org/markdown/setup/conda.md): Create a Conda environment and install Khiops from conda-forge, with optional SDKs for remote cloud storage.
- [Khiops application](https://khiops.org/markdown/setup/nocode.md): Install and use the no-code desktop application to explore data and build models without writing Python.
- [Khiops Visualization](https://khiops.org/markdown/setup/visualization.md): Download the desktop visualization tool and open Khiops analysis reports for interactive exploration.
- [Khiops Native Interface setup](https://khiops.org/markdown/setup/kni.md): Install the native integration library for low-latency, in-memory model scoring from C, C++, Java, Python, or Matlab applications.
- [Cloud storage drivers for the Python library](https://khiops.org/markdown/setup/drivers-and-sdk-for-library.md): Install the vendor SDKs required for the Python library to read and write S3, GCS, and Azure resources.
- [Cloud storage drivers for the application](https://khiops.org/markdown/setup/drivers-and-sdk-for-application.md): Install the Linux packages required for the Khiops desktop application to access S3, GCS, and Azure resources.
- [Run Khiops with Docker](https://khiops.org/markdown/tutorials/docker.md): Run Khiops in official Docker images and execute scenarios against data mounted into the container.
- [Distributed execution with Kubernetes](https://khiops.org/markdown/tutorials/k8s.md): Launch distributed Khiops jobs on Kubernetes with the MPI Operator and a Kubernetes job manifest.
- [Khiops Notebook](https://khiops.org/markdown/setup/khiops-notebook.md): Start a pre-built Jupyter environment for Khiops with the `khiopsml/khiops-notebook` Docker image.
- [Cloud storage](https://khiops.org/markdown/tutorials/storage.md): Read and write datasets directly on S3, GCS, or Azure through Khiops cloud-storage drivers and their authentication settings.
- [Scenario-based execution](https://khiops.org/markdown/tutorials/scenario.md): Run Khiops in batch mode with command-line options, recording and replaying text scenario files with optional JSON parameter files.
- [Redirect output to standard streams](https://khiops.org/markdown/tutorials/use_stdout.md): Send Khiops command, log, and progression messages to standard output or standard error in batch workflows.
- [Real-time deployment with KNI](https://khiops.org/markdown/tutorials/kni.md): Integrate Khiops models into information systems for real-time, in-memory scoring through the native interface.


## Khiops Native Interface (KNI)

Build and run the KNI tutorial examples (C, Java, Python) for real-time, in-memory model scoring.

- [KNI tutorial guide](https://khiops.org/markdown/tutorials/kni-tutorial/README.md): Install KNI and build C, Java, and Python examples for single-table and multi-table recoding.
- [KNI API header](https://khiops.org/markdown/tutorials/kni-tutorial/include/KhiopsNativeInterface.h): The C++ header that defines the KNI API.
- [KNI C single-table example](https://khiops.org/markdown/tutorials/kni-tutorial/cpp/KNIRecodeFile.c): With C, compile and run `KNIRecodeFile` to recode a single-table input with a Khiops dictionary.
- [KNI C multi-table example](https://khiops.org/markdown/tutorials/kni-tutorial/cpp/KNIRecodeMTFiles.c): With C, compile and run `KNIRecodeMTFiles` to recode multi-table inputs into one output file.
- [KNI Java interface](https://khiops.org/markdown/tutorials/kni-tutorial/java/KNI.java): JNA bindings that expose the KNI native library to Java.
- [KNI Java example](https://khiops.org/markdown/tutorials/kni-tutorial/java/KNIRecodeFile.java): Build and run a Java single-table recoding application through JNA.
- [KNI Python single-table example](https://khiops.org/markdown/tutorials/kni-tutorial/python/KNIRecodeFile.py): With Python, use the `khiops-kni` package to recode a single-table input.
- [KNI Python multi-table example](https://khiops.org/markdown/tutorials/kni-tutorial/python/KNIRecodeMTFiles.py): With Python, use the `khiops-kni` package to recode multi-table inputs.
- [KNI python API doc](https://khiops.org/markdown/tutorials/kni-tutorial/python/docs/kni.md): Documentation of the package pip khiops-kni

## User interfaces

Use the desktop GUI applications to explore data, build models, and visualize analysis and coclustering reports.

- [Khiops GUI](https://khiops.org/markdown/ui-docs/khiops.md): Use the Khiops desktop application to explore data, build classification, regression, or unsupervised models, define dictionaries, and deploy models on multi-table schemas.
- [Coclustering GUI](https://khiops.org/markdown/ui-docs/coclustering.md): Use the coclustering desktop application to discover hierarchical row and column partitions, or instances-by-variables partitions, and simplify, explore, and deploy the resulting models.
- [Visualization](https://khiops.org/markdown/ui-docs/visualization.md): Explore Khiops `khj` reports through preparation, modeling, evaluation, and other interactive visualization views.
- [Covisualization](https://khiops.org/markdown/ui-docs/covisualization.md): Explore coclustering `khcj` reports, their hierarchical axes and contexts, and the dependency patterns shown in mutual-information views.

## External references

Find the source repositories for Khiops, its Python library, and the KNI tutorial.

- [Khiops source](https://github.com/KhiopsML/khiops): Find the source repository, package information, and development resources for Khiops.
- [Khiops Python package source](https://github.com/KhiopsML/khiops-python): Find the source repository, package information, and development resources for the Khiops Python library.
- [KNI Tutorial](https://github.com/KhiopsML/KNI-tutorial): Find the source repository for the KNI tutorial examples listed in the Khiops Native Interface (KNI) section above.

## Optional

- [Contact](https://khiops.org/markdown/contact.md): Submit an inquiry to the Khiops documentation team through the embedded contact form.
- [Legal matters](https://khiops.org/markdown/legalmatters.md): Read Orange SA legal notices, trademark and license information, and source-code availability terms.

## Excluded

Pages intentionally left out of the generated `llms.txt`. Links here are still checked during the build and kept out of the auto-generated "Others" section, but this section itself is stripped before publishing.

- [Documentation home](https://khiops.org/markdown/index.md)
- [Python API index](https://khiops.org/markdown/api-docs/python-api/index.md)
- [Core index](https://khiops.org/markdown/api-docs/python-api/core/index.md)
- [Scikit-learn index](https://khiops.org/markdown/api-docs/python-api/sklearn/index.md)
- [demo visualization](https://khiops.org/markdown/setup/demovisualization.md)

- [common](https://khiops.org/markdown/api-docs/python-api/internal/common.md): Common utility functions and classes shared across the library.
- [dataset](https://khiops.org/markdown/api-docs/python-api/internal/dataset.md): Classes for handling diverse data tables in the scikit-learn API.
- [filesystems](https://khiops.org/markdown/api-docs/python-api/internal/filesystems.md): Classes to interact with local and remote (S3, GCS, Azure) filesystems.
- [Internal overview](https://khiops.org/markdown/api-docs/python-api/internal/index.md): Overview of the internal (non-public) modules used by the Khiops Python library.
- [io](https://khiops.org/markdown/api-docs/python-api/internal/io.md): Classes to handle Khiops-specific I/O.
- [runner](https://khiops.org/markdown/api-docs/python-api/internal/runner.md): Classes implementing the Khiops Python backend runners.
- [scenario](https://khiops.org/markdown/api-docs/python-api/internal/scenario.md): Classes for creating Khiops scenario files.
- [task](https://khiops.org/markdown/api-docs/python-api/internal/task.md): Core API functions abstractions.
- [types](https://khiops.org/markdown/api-docs/python-api/internal/types.md): Khiops task argument mini-type system.
- [version](https://khiops.org/markdown/api-docs/python-api/internal/version.md): Class to handle Khiops version strings.

