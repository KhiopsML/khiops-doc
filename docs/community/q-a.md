# Questions & Answers

Here is a curated selection of frequently asked questions from our users, each accompanied by a concise and rigorous answer.

These Q&As are designed to clarify how Khiops works under the hood and guide you through best practices for using the tool effectively.

💬 Have a question of your own?
Feel free to ask it on our [GitHub Discussions board][github-discussions] — we welcome all contributions, from beginner to expert level.

This section is updated regularly as new questions arise in the community.

[github-discussions]: https://github.com/orgs/KhiopsML/discussions

## Installation 

## Data Preprocessing

??? question "Does Khiops Automatically Apply Log, Square, or Other Transformations During Variable Encoding?"
    No, Khiops does not automatically apply transformations such as logarithm, square, or square root based on skewness or other distributional characteristics. Instead, it relies on a non-parametric, information-theoretic discretization approach based on value ranks, *making explicit variable transformations unnecessary.*

    **Why Are Such Transformations Unnecessary in Khiops?**

    Khiops employs the **MODL (Minimum Optimized Description Length)** discretization method, which ensures:

    **Optimal Binning via Information Theory:** The MODL criterion selects the best discretization scheme with the optimal number of intervals and bounds, without requiring parametric assumptions. It directly adapts to the data’s intrinsic structure.
    **Invariance to Monotonic Transformations:** Khiops encodes numerical variables using value ranks rather than raw values. Thus, monotonic transformations (log, square root, exponential, etc.) have no effect on the discretization outcome.
    **Robustness to Skewness and Outliers:** Unlike parametric approaches, Khiops does not rely on moments (mean, variance, skewness) or density estimation, making it naturally resilient to skewed distributions and outliers.
    **No Need for Normalization or Standardization:** Since Khiops operates on ranks rather than raw values, common preprocessing steps like Z-score normalization (subtracting the mean and dividing by the standard deviation) or standardization to 0-1 range, are unnecessary. Feature scaling does not impact the learning process.

    *Conclusion*

    Transformations aimed at normalizing distributions or correcting skewness are unnecessary in Khiops. Its MODL-based encoding automatically adapts to the data, ensuring optimal variable encoding without manual intervention.

## Model Training & Evaluation

## API, Integration & Deployment

??? question "Can I use Polars instead of Pandas as input format for Khiops?"

    Currently, *Khiops does not support polars.DataFrame* as input for the `khiops.sklearn` Python estimators. 

    However, if you’re concerned about the *performance or scalability limitations* of in-memory structures like Pandas (or Polars), we recommend using the `khiops.core` *API* instead. This low-level interface is designed for *high-throughput, large-scale processing*. It operates directly on raw text files, bypasses in-memory DataFrames entirely, and provides *native access to cloud file systems* (S3, GCS, Azure, HDFS, etc.).

    > The `khiops.core` API is fully documented on our website, with tutorials showing how to train, evaluate, and deploy models efficiently—using only files and command-line workflows.

    Khiops has been developed and refined for over 20 years with a strong focus on *native scalability* and *multi-table processing*—a key requirement at Orange, *where telecom usage logs generate massive amounts of data* across multiple relational tables.

    In production, we routinely process *billions of records* using Khiops. The full modeling pipeline—including *automated feature engineering* with over *10,000 computed aggregates*—can be completed in about *one hour on a single machine*, starting from hundreds of gigabytes across five relational files (user info, calls in/out, SMS in/out). Distributed execution on Kubernetes makes this even faster.

    While adding Polars support remains a possible enhancement for future releases (see issue #292), for serious data workloads we strongly recommend leveraging the `khiops.core` API.

