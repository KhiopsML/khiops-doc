# Khiops

> Khiops is an interpretable and scalable data science platform with a Python library, dictionary APIs, and deployment tools.

This is a curated map of the Khiops documentation. Choose the section that matches the task, then follow the most specific guide or reference page.

## Python development

- [Install with pip](https://khiops.org/markdown/setup/pip.md): Install the Khiops Python library and its dependencies with pip.
- [Install with Conda](https://khiops.org/markdown/setup/conda.md): Install the Khiops Python library in a Conda environment.
- [Python quickstart](https://khiops.org/markdown/tutorials/quickstart.md): Train a first Khiops model through the scikit-learn API.
- [Single-table scikit-learn tutorial](https://khiops.org/markdown/tutorials/notebooks/single_table_classifier.md): Build a classifier from a single-table dataset.
- [Multi-table scikit-learn tutorial](https://khiops.org/markdown/tutorials/notebooks/multi_table_classifier.md): Build a classifier from related tables.
- [No data preparation tutorial](https://khiops.org/markdown/tutorials/notebooks/No_data_Cleaning.md): Use Khiops when raw data still needs substantial preparation.
- [Auto feature engineering tutorial](https://khiops.org/markdown/tutorials/notebooks/Use_in_any_ML_pipeline.md): Use Khiops feature engineering inside a broader machine-learning pipeline.
- [Python API reference](https://khiops.org/api-docs/python-api/): Reference documentation for the Khiops Python modules, classes, and functions.
- [Python cloud storage](https://khiops.org/markdown/setup/drivers-and-sdk-for-library.md): Configure S3, GCS, or Azure storage for the Khiops Python library.

## Data science and foundations

- [What makes Khiops different](https://khiops.org/markdown/learn/understand.md): Understand the main principles and practical positioning of Khiops.
- [MODL formalism](https://khiops.org/markdown/learn/modl.md): Learn the formalism behind Khiops model selection and interpretability.
- [Optimal encoding](https://khiops.org/markdown/learn/preprocessing.md): Understand Khiops preprocessing and variable encoding.
- [Auto feature engineering](https://khiops.org/markdown/learn/autofeature_engineering.md): Understand Khiops multi-table feature construction.
- [Parsimonious training](https://khiops.org/markdown/learn/learning_models.md): Understand model selection and variable weighting in Khiops.
- [Optimal histograms](https://khiops.org/markdown/learn/histograms.md): Learn how Khiops constructs optimal histograms.
- [Coclustering](https://khiops.org/markdown/learn/coclustering.md): Understand Khiops coclustering and its use cases.
- [Hardware adaptation](https://khiops.org/markdown/learn/hardware_adaptation.md): Understand how Khiops adapts execution to available hardware.

## Dictionaries and core API

- [Start using dictionaries](https://khiops.org/markdown/tutorials/kdic_intro.md): Introduction to the Khiops Core API and dictionary-based data management.
- [Single-table dictionary concepts](https://khiops.org/markdown/tutorials/kdic_single_table.md): Manage a single-table data workflow with Khiops dictionaries.
- [Multi-table dictionary concepts](https://khiops.org/markdown/tutorials/kdic_multi_table.md): Manage related tables and entities with Khiops dictionaries.
- [Database files](https://khiops.org/markdown/api-docs/kdic/database-files.md): Reference for Khiops database file format.
- [Dictionary files](https://khiops.org/markdown/api-docs/kdic/dictionary-files.md): Reference for defining Khiops dictionaries.
- [Basic dictionary rules](https://khiops.org/markdown/api-docs/kdic/numerical-comparisons.md): Numerical and categorical comparison rules for dictionary expressions.
- [Multi-table rules](https://khiops.org/markdown/api-docs/kdic/multi-table-rules-introduction.md): Rules for extracting and aggregating values across related tables.
- [Data preparation rules](https://khiops.org/markdown/api-docs/kdic/data-preparation-rules.md): Dictionary structures and rules used for data preparation.
- [Predictor rules](https://khiops.org/markdown/api-docs/kdic/predictor-rules.md): Dictionary structures and rules used to deploy predictors.
- [Dictionary technical limits](https://khiops.org/markdown/api-docs/kdic/limits.md): Technical limits and numerical precision of the dictionary language.

## Installation and deployment

- [Installation overview](https://khiops.org/markdown/setup/index.md): Choose an installation method and find the main setup instructions.
- [Khiops Notebook](https://khiops.org/markdown/setup/khiops-notebook.md): Run Khiops from the pre-built notebook environment.
- [Run Khiops with Docker](https://khiops.org/markdown/tutorials/docker.md): Run Khiops in a reproducible container environment.
- [Distributed execution with Kubernetes](https://khiops.org/markdown/tutorials/k8s.md): Run Khiops in a distributed Kubernetes deployment.
- [Scenario-based execution](https://khiops.org/markdown/tutorials/scenario.md): Run Khiops in batch mode and integrate it into an execution scenario.
- [Cloud storage](https://khiops.org/markdown/tutorials/storage.md): Read and write datasets stored in cloud services.
- [Real-time deployment with KNI](https://khiops.org/markdown/tutorials/kni.md): Integrate Khiops models into an information system through the native interface.
- [Redirect output to standard streams](https://khiops.org/markdown/tutorials/use_stdout.md): Control where Khiops trace and log messages are written.
- [Khiops application](https://khiops.org/markdown/setup/nocode.md): Use the standalone Khiops application without writing Python code.

## User interfaces

- [Khiops GUI](https://khiops.org/markdown/ui-docs/khiops.md): Use the Khiops desktop application.
- [Coclustering GUI](https://khiops.org/markdown/ui-docs/coclustering.md): Use the Khiops Coclustering desktop application.
- [Visualization](https://khiops.org/markdown/ui-docs/visualization.md): Explore Khiops analysis results with Khiops Visualization Desktop.
- [Covisualization](https://khiops.org/markdown/ui-docs/covisualization.md): Explore coclustering results with Khiops Visualization Desktop.

## Reference

- [Khiops documentation home](https://khiops.org/markdown/index.md): General entry point for the Khiops documentation.
- [Khiops Python package documentation](https://github.com/KhiopsML/khiops-python): Source repository and package information for the Khiops Python library.
- [Khiops bibliography](https://khiops.org/markdown/references.md): Publications and references related to Khiops.
