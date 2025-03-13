# Getting Started with Khiops

Welcome to the practical guide to using Khiops. Whether you are exploring its capabilities for the first time or preparing for industrial-scale deployments, this section will help you understand **how Khiops streamlines and enhances your data science workflows**.

Unlike traditional machine learning libraries, Khiops is built on **a unique formalism and advanced automation capabilities** that fundamentally reshape the data science process. By automating tedious, repetitive and technically complex steps, Khiops allows users to **focus on the core objectives of data science**: understanding their data and solving meaningful business problems.

At the same time, this singular approach may feel unfamiliar to those accustomed to standard tools and libraries. This section provides a comprehensive introduction to Khiops, enabling you to make the most of its strengths and integrate it into your projects with confidence.

Here's what you'll find in this page:

- How Khiops [**accelerates your workflow**][crisp-dm]: Learn how Khiops transforms the traditional data science pipeline by simplifying complex processes and letting you focus on high-value tasks.
- Choosing [**the right API**][two-apis]: The **Scikit-learn-like** API is ideal for rapid experimentation and prototyping, while the **core** API excels in production-scale applications. Determine which best suits your needs.

[crisp-dm]: #how-khiops-fits-into-the-data-science-workflow
[two-apis]: #two-apis-for-different-needs

This introduction will guide you through the foundational points and help you navigate the tutorials that follow. Here's an overview of the sections:

- **Scikit-learn-like API tutorials**: Learn the basics of Khiops with examples on quickstarts, single- and multi-table examples, and hands-on notebooks that showcase Khiops' technical advantages, such as automated data preparation and multi-table processing.
- **Core API & dictionaries**: Dive deeper into advanced capabilities, including dictionary usage for scalable, production-ready workflows.
- **Deployment & Integration**: Learn how to deploy Khiops models efficiently in real-world environments, with support for cloud storage, containerized execution, and real-time inference.

Whether you’re exploring Khiops for rapid prototyping or integrating it into large-scale industrial workflows, this section will provide you with the necessary guidance to leverage its full potential.

!!! info    
    Questions about deploying Khiops in specific environments (e.g. Hadoop, Openshift, K8s) can be addressed in our [Q&A section][discussions] or through our [contact form][contact-form].

[contact-form]: ../contact.md
[discussions]: https://github.com/orgs/KhiopsML/discussions

## How Khiops Fits into the Data Science Workflow

Khiops introduces a streamlined and effective approach to data science, **simplifying every stage of the process** while providing advanced automation and a robust formalism. Unlike traditional tools, Khiops enables you **to focus on what truly matters**: understanding your data, interpreting insights (the story your data tells), solving business problems, and deploying reliable models. Here's how you can leverage Khiops' unique features step by step:


- **Skip Data Cleaning and Preparation**: Forget about spending hours on cleaning and formatting your data. Khiops reads raw data directly and handles common issues like missing values, inconsistent formats, or noisy inputs. For example, if your dataset contains missing values, Khiops automatically treats them as meaningful signals when training models. It also removes the need for transformations like log scaling or standardization, as its value rank-based encoding is inherently invariant to monotonic transformations.

    !!! example "Follow the [**No Need for Data Preparation**][no_data_cleaning] tutorial to see this in action."

[no_data_cleaning]: ./Notebooks/No_data_Cleaning.ipynb

- **Skip Variable Encoding**: Before using variables in a machine learning model, they often need to be transformed into a format the algorithm can process (e.g. categorical variables must be converted into numerical representations). Khiops eliminates this complexity with its MODL formalism, which automatically encodes categorical and numerical variables into statistically optimal groups or intervals.

    For example, instead of manually binning a variable like `age`, Khiops will determine ranges like [0, 18], ]18, 35], ]35, 50], etc. These intervals are not arbitrary but are optimally chosen according to the target variable, indeed building a univariate classifier.

    !!! example "Explore the [**Optimal Encoding**][optimal_encoding] tutorial and learn more about the concept on the [**Optimal Encoding**][encoding_foundations] foundations page."

[optimal_encoding]: ./Notebooks/Optimal_Encoding.ipynb
[encoding_foundations]: ../learn/preprocessing.md

- **Skip Feature Engineering**: When working with multi-table datasets (arguably the most common scenario in real-world business use cases), feature engineering often becomes one of the most labor-intensive stages. Traditionally, it requires significant domain expertise and trial-and-error to create meaningful features. Khiops automates this process entirely, saving you time and delivering optimal results.

    Khiops performs feature engineering in a supervised manner, ensuring that new features are relevant to the target variable, with quasilinear complexity that enables scaling efficiently to large datasets. By balancing model complexity with statistical significance, Khiops avoids overfitting while generating informative aggregates.

    For example, Khiops can automatically calculate metrics like "total purchases per customer" or "average transaction amount per week" when working with a sales dataset. 

    !!! example "Explore the [**Auto Feature Engineering**][autofeature_tuto] tutorial and learn about the methodology in the [dedicated][autofeature] foundations section."

[autofeature_tuto]: ./Notebooks/Use_in_any_ML_pipeline.ipynb
[autofeature]: ../learn/autofeature_engineering.md

- **Skip Hyperparameter Tuning and Questioning About Overfitting**: Traditional machine learning libraries often require time-consuming hyperparameter tuning (learning rates or regularization coefficients) to optimize model performance, and careful regularization to prevent overfitting. Khiops eliminates both concerns thanks to its unique MODL formalism rooted in information theory. It operates without hyperparameters and naturally balances model complexity and information gain (only significant patterns are captured).

    !!! example "Explore the [**MODL formalism**][MODL] and its [**parsimonious training**][parsimonious_training] principles."

[MODL]: ../learn/modl.md
[parsimonious_training]: ../learn/learning_models.md

- **Evaluate Models with Confidence**: Khiops enables you to assess your models with clarity and trust. Thanks to its unique formalism, every transformation (variable encoding or feature engineering) is explicit and interpretable by design. The resulting models are parsimonious, allowing you to understand the precise contribution of each feature to the predictions.

    Khiops is also robust by nature. If your data lacks meaningful information for the target variable, Khiops won't generate a model, ensuring you can trust the output. This gives you confidence that issues in performance stem from the data, not the modeling process itself.

    For easy model evaluation, Khiops includes a native visualization tool that helps you interpret your results. With this tool, you can explore lift curves, confusion matrices, and variable importance, gaining clear insights into your model's behavior and reliability.

    !!! example "Try the [**Visualization Tool demo**][demo_viz] and set it up with [**these instructions**][setup_viz]."

[demo_viz]: ../setup/demovisualization.md
[setup_viz]: ../setup/visualization.md

With Khiops simplifying every stage of the data science workflow, the next step is choosing the right API for your needs. Whether you're exploring datasets or preparing for industrial-scale deployments, Khiops offers two powerful options: the Scikit-learn-like API and the core API. Let's dive into their differences and find the best fit for your projects.

## Two APIs for different needs

Khiops offers two APIs tailored to different use cases: the Scikit-learn-like API and the core API. While both leverage Khiops' unique strengths, they are optimized for distinct stages of the data science workflow and scaling requirements.

### Scikit-learn-like API: For quick prototyping and integration

The scikit-learn-like API is ideal for data scientists familiar with Python and the Scikit-learn ecosystem. It provides an accessible entry point for experimenting with Khiops' key features, including multi-table support and automated feature engineering.

| :white_check_mark: **Advantages** | :red_square: **Limitations**   |
|-----|-----------------|
| **Familiar syntax**: Designed for immediate use with standard Scikit-learn workflows, making onboarding effortless.  | **High I/O requirements**: Data loading and processing rely on Python and Pandas, which can be memory-intensive.     |
| **Ecosystem integration**: Acts as standard Scikit-learn estimators, enabling easy integration with other tools (e.g. pyCaret for benchmarking). | **Scalability constraints**: Not optimized for large-scale datasets as it does not support Khiops out-of-core processing. |
| **Feature testing**: Lets you explore Khiops' multi-table capabilities and auto feature engineering, supporting star or snowflake schemas (with some limitations). |  **Limited support for key Khiops features**: limited expressiveness of multi-table schemas and data management capabilities.                                                                                                               |

### Core API: Production-ready and scalable

The core API unleashes the full power of Khiops, offering unmatched scalability and flexibility for industrial-scale projects. Its rich dictionary-based formalism supports complex multi-table databases and facilitates streamlined data management for production use.

| :white_check_mark: **Advantages**                                                                 | :red_square: **Limitations**                                                                                   |
|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| **Rich data description**: The dictionary formalism provides a structured, detailed way to describe data and especially multi-table relationships, enabling efficient data processing on the fly. | **Learning Curve**: The dictionary formalism introduces new concepts, requiring users to invest time in learning its syntax and structure. |
| **Advanced data management**: Automates business-level transformations such as aggregate creation, variable selection, and example filtering, all within the API. It can also act as a highly efficient ETL tool. | **Learning Curve**: The core API is tailored to Khiops and thus provides a different experience as compared to Scikit-learn APIs. |
| **Facilitated versioning**: Dictionaries serve as centralized, versionable configurations for data transformations and model definitions, ensuring traceability. |                                                                                                  |
| **Seamless production deployment**: Models trained with the core API are ready for deployment (via the output dictionary file), ensuring robust integration into production workflows. |                                                                                                  |
| **Out-of-core processing**: Optimized for hardware resource usage, handling datasets that exceed memory limits efficiently. |                                                                                                  |

## Conclusion

Choosing the Right API:

- Start with the Scikit-learn-like API if you're exploring Khiops' capabilities on small datasets or need a quick, familiar way to test models within the Python ecosystem.
- Move to the core API for production-grade scalability, complex data management needs, or when working with large, multi-table datasets.

