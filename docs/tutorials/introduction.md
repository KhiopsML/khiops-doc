# How to use Khiops

Welcome to the hands-on section of the Khiops documentation! This guide will help you master Khiops and make the most of its powerful features, whether you’re just starting out or preparing for large-scale, production-ready deployments.

Here’s what this page covers:

- [**Accelerating your workflow**][crisp-dm]: Discover how Khiops simplifies and speeds up the entire data science process, enabling you to focus on what truly matters - understanding your data and solving business problems.
- [**Choosing the right API**][two-apis]: Learn the differences between Khiops’ two APIs —sklearn-like for quick prototyping and core for industrial-scale applications—and find the best fit for your needs.

[crisp-dm]: #how-khiops-fits-into-the-data-science-workflow
[two-apis]: #two-apis-for-different-needs

!!! info
    Some components around Khiops are not documented yet, so this “How To” section is still in progress. For example, a documentation on deploying Khiops natively on Kubernetes is coming soon. 
    
    Questions about deploying Khiops in specific environments (e.g. HDFS) can be addressed in our [Q&A section][discussions] or through our [contact form][contact-form].

[contact-form]: contact.md
[discussions]: https://github.com/orgs/KhiopsML/discussions

## How Khiops fits into the data science workflow

Khiops simplifies the data science pipeline, enabling you to focus on the most impactful aspects of your projects. By automating the tedious stages of workflow, Khiops removes the need for time-consuming manual tasks and complex tooling. Finally, Khiops empowers you to:

- Focus on understanding your data, and verifying it aligns with the problem you’re solving.
- Ensure the data doesn’t suffer from issues like data leaks or biaises.

Below, we illustrate how Khiops enhances the stages of the well-known CRISP-DM process:

- **Data Preparation**: Khiops works directly with raw data whether it is from a single table or a relational dataset with several tables. The feature engineering and variable encoding steps are automated and our singular formalism guarantee we do not loss information (which happens when it is done manually).
- **Modeling**: Khiops is based on a singular formalism applied end-to-end, no hyperparameter tuning is needed.
- **Deployment**: Khiops models are production-ready. The platform’s efficient handling of large datasets ensures scalability, whether for batch processing or real-time applications.

By saving a lot of time on the steps above, you can spend more on the value-added one:

- **Business and data understanding**: Khiops accelerates data exploration by providing interpretable univariate analyses (i.e. correlation of each variable with the target) or insights into missing values, outliers, or variable importance. In addition to the explicit and interpretal models, it bridges the gap between technical work and business needs.
- **Evaluation**: Comprehensive evaluation reports (including metrics like ROC curves, confusion matrices) help you quickly validate your model’s performance. Plus, the interpretability of the model gives you a clear picture of its behavior.

## Two APIs for different needs

Khiops offers two APIs tailored to different use cases: the sklearn-like API and the core API. While both leverage Khiops’ unique strengths, they are optimized for distinct stages of the data science workflow and scaling requirements.

### Sklearn-like API: Quick prototyping and integration

The sklearn-like API is ideal for data scientists familiar with Python and the sklearn ecosystem. It provides an accessible entry point for experimenting with Khiops’ key features, including multi-table support and automated feature engineering.

**Advantages**:

- Familiar syntax: Designed for immediate use with standard sklearn workflows, making onboarding effortless;
- Ecosystem integration: Acts as a standard sklearn estimator, enabling easy integration with others tools (e.g. in some notebooks tutorials we integrate Khiops in the pyCaret library for benchmarking)
- Feature Testing: Lets you explore Khiops’ multi-table capabilities and auto feature engineering, supporting star or snowflake schemas (with some limitations);

**Limitations**:

- High I/O requirements: Data loading and processing rely on Python and Pandas, which can be memory-intensive ;
- Scalability constraints: Consequently to the previous point, this is not optimized for large-scale datasets as it does not support the Khiops out-of-core processing.

### Core API: Production-ready and scalability

The core API unleashes the full power of Khiops, offering unmatched scalability and flexibility for industrial-scale projects. Its rich dictionary-based formalism supports complex multi-table databases and facilitates streamlined data management for production use.

**Advantages**:

- Rich data description: The dictionary formalism provides a structured, detailed way to describe the data and especially the multi-table data relationships, enabling efficient data processing on the fly;
- Advanced data management: Automates business-level transformations, such as aggregate creation, variable selection, and example filtering, all within the API. It can also act as a highly efficient ETL tool;
- Facilitated Versioning: Dictionaries serve as centralized, versionable configurations for data transformations and model definitions, ensuring traceability;
- Seamless Production Deployment: Models trained with the core API are ready for deployment (through the output dictionary file), ensuring robust integration into production workflows;
- Out-of-Core Processing: Optimized for hardware resource usage, handling datasets that exceed memory limits efficiently.

**Limitations**:

- Learning Curve: The dictionary formalism introduces new concepts, requiring users to invest some time in learning its syntax and structure.

## Conclusion

Choosing the Right API:

- Start with the sklearn-like API if you’re exploring Khiops’ capabilities on small datasets or need a quick, familiar way to test models within the Python ecosystem;
- Move to the core API for production-grade scalability, complex data management needs, or when working with large, multi-table datasets.
