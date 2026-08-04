---
hide:
  - toc
---

# Q&A

This section highlights the most useful community questions about Khiops, selected for practical use in real projects.

The objective is simple: help users find reliable guidance quickly, from first experiments to production-scale deployments.

!!! question "Have a question or request?"
    - **Ask in [GitHub Discussions](https://github.com/orgs/KhiopsML/discussions)**
    - **Report bugs or request product changes in the [Khiops repository issues](https://github.com/KhiopsML/khiops/issues)**

## Fundamentals of modeling

- [Why is it better to provide raw data to Khiops instead of preprocessed or encoded data?](fundamentals-of-modeling.md#why-is-it-better-to-provide-raw-data-to-khiops-instead-of-preprocessed-or-encoded-data)
- [Since Khiops does not have hyperparameters, how can I manage overfitting?](fundamentals-of-modeling.md#since-khiops-does-not-have-hyperparameters-how-can-i-manage-overfitting)
- [How does Khiops handle datasets with imbalanced classes?](fundamentals-of-modeling.md#how-does-khiops-handle-datasets-with-imbalanced-classes)
- [How does Khiops handle target value grouping, and why is it useful for classification tasks?](fundamentals-of-modeling.md#how-does-khiops-handle-target-value-grouping-and-why-is-it-useful-for-classification-tasks)

## Preprocessing and encoding

- [Does Khiops automatically apply log, square, or other transformations during variable encoding?](preprocessing-and-encoding.md#does-khiops-automatically-apply-log-square-or-other-transformations-during-variable-encoding)
- [Discretization cost and number of interval partitions](preprocessing-and-encoding.md#discretization-cost-and-number-of-interval-partitions)

## Scalability and large datasets

- [How to train a model using very huge initial datasets: methodological advice needed](scalability-and-large-datasets.md#how-to-train-a-model-using-very-huge-initial-datasets-methodological-advice-needed)
- [Allow user to deactivate Khiops memory dimensioning](scalability-and-large-datasets.md#allow-user-to-deactivate-khiops-memory-dimensioning)
- [Elephant instances in multi-table databases](scalability-and-large-datasets.md#elephant-instances-in-multi-table-databases)

## Co-clustering

- [Explaining counter-intuitive Khiops co-clustering results on a simple example](coclustering.md#explaining-counter-intuitive-khiops-co-clustering-results-on-a-simple-example)
- [What is the difference between VxV and Instances x Variables (IxV) coclustering?](coclustering.md#what-is-the-difference-between-vxv-and-instances-x-variables-ixv-coclustering)
- [How do VxV and IxV coclustering compare on simple bivariate patterns?](coclustering.md#how-do-vxv-and-ixv-coclustering-compare-on-simple-bivariate-patterns)
- [Why does VxV coclustering become sparse in higher dimensions, and what protects IxV?](coclustering.md#why-does-vxv-coclustering-become-sparse-in-higher-dimensions-and-what-protects-ixv)
- [What does an IxV coclustering analysis look like on a real dataset (Iris)?](coclustering.md#what-does-an-ixv-coclustering-analysis-look-like-on-a-real-dataset-iris)

## Python API and development

- [How can we build custom features by using the Khiops Python API?](python-api-and-development.md#how-can-we-build-custom-features-by-using-the-khiops-python-api)
- [Add random_state parameter](python-api-and-development.md#add-random_state-parameter)

## Deployment and integration

- [Model Output PMML](deployment-and-integration.md#model-output-pmml)
- [Can Khiops be deployed on Hadoop?](deployment-and-integration.md#can-khiops-be-deployed-on-hadoop)
