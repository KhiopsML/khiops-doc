# Deployment and Integration

This page centralizes deployment and interoperability questions frequently raised by users.

!!! question "Have a question or request?"
    - **Ask in [GitHub Discussions](https://github.com/orgs/KhiopsML/discussions)**
    - **Report bugs or request product changes in the [Khiops repository issues](https://github.com/KhiopsML/khiops/issues)**

## Index of questions

1. [Model Output PMML](#model-output-pmml)
2. [Can Khiops be deployed on Hadoop?](#can-khiops-be-deployed-on-hadoop)

---

## Model Output PMML

Is it technically feasible to convert the model's end results into SQL scripts or PMML language? This would support model deployment in multiple environments and enhance comprehension of the predictive calculation logic.

Thank you for your question.

Khiops does not provide an export of models to SQL or PMML. The main reason is that a full Khiops model cannot be faithfully represented in these formats.

Khiops relies on a rich dictionary layer and native multi-table modeling (keys, aggregations, derived variables, discretizations, value groups, special-value handling). Standard PMML cannot express many of these operations, and generating equivalent SQL would lead to extremely complex, environment-dependent code that would be difficult to validate and maintain.

For these reasons, the project focuses on end-to-end deployment using dictionaries, through the Khiops engine and the Khiops Native Interface, which guarantee consistent and reliable scoring across environments.

*Source: [discussion #852](https://github.com/orgs/KhiopsML/discussions/852)*

---

## Can Khiops be deployed on Hadoop?

This question is inspired by inquiries we've received via our [contact form](https://khiops.org/contact/) from users interested in deploying Khiops in Hadoop environments.

Yes, Khiops has been used for several years in production on Hadoop using specialized tools we have developed. However, these components are not yet part of its open-source distribution.

**Overview of the technical solution**

We have developed the following components to enable Khiops integration with Hadoop ecosystems:

- HDFS driver for Khiops: A dedicated driver enabling Khiops to read and write directly from HDFS, with full support for multipart files;
- Khiops4Spark: A Spark wrapper that enables Khiops to run on Hadoop clusters through `spark-submit` command;
- Khiops4Yarn: A Yarn wrapper that allows Khiops to operate directly within Hadoop's resource management framework.

Khiops, as a native MPI (Message Passing Interface) program, works exactly the same on a multicore machine or on a multinode cluster. When deployed on multiple machines, Khiops efficiently leverages the CPU, memory, and I/O resources of each allocated node, ensuring optimal performance at scale. The Spark and Yarn wrappers manage the communication with their respective resource managers, which in turn allocate resources that will be used by Khiops.

If you're interested in deploying Khiops in such environments or have specific use cases, please reach out via our [contact form](https://khiops.org/contact/) for further information.

*Source: [discussion #520](https://github.com/orgs/KhiopsML/discussions/520)*
