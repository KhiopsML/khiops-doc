# Questions & Answers

Here is a curated selection of frequently asked questions from our users, each accompanied by a concise and rigorous answer.

These Q&As are designed to clarify how Khiops works under the hood and guide you through best practices for using the tool effectively.

💬 **Have a question of your own?** Feel free to ask it on our [GitHub Discussions board][github-discussions] — we welcome all contributions, from beginner to expert level.

[github-discussions]: https://github.com/orgs/KhiopsML/discussions

## Installation 

??? quote "How can I install Khiops using pip? Is a pip-only installation officially supported?"

    Yes, *Khiops can be installed using pip*, although it is not the default or recommended method for most users.

    We provide a pip-compatible package to ensure that users who prefer Python-native workflows (e.g. Kaggle, Colab, virtualenv) can still use Khiops. However, there are important caveats:
    
    - The pip package **does not include the Khiops C++ engine**, which must be installed manually as a system-level dependency (via `apt`, `.deb`, or `.rpm` depending on the OS).
    - In addition, *MPI (Message Passing Interface)* must be installed on the system, as it is a dependency of the core Khiops engine. It may not work on certain environments that **restrict admin rights for standard users**;
    - On *macOS*, pip installation is *not supported* at this time (use Conda instead).

    This makes pip installation less straightforward and better suited for advanced users familiar with system administration.

    **Recommended installation (with Conda)**

    We strongly recommend using *Conda*, which automatically installs all required components (Python bindings, C++ engine, MPI). It is the most reliable method, especially for first-time users.

    Conda installation instructions are available here: [Install Khiops][conda]

    **On jupyter environments without conda**

    Kaggle for instance no longer supports Conda natively, but you can install Khiops in such environment using the following steps:

    ```
    # Install khiops-core apt package
    !  wget -O "khiops.deb" "https://github.com/KhiopsML/khiops/releases/download/{{ KHIOPS_VERSION }}/khiops-core-openmpi_{{ KHIOPS_VERSION }}-1-jammy.amd64.deb" 
    ! sudo dpkg -i "khiops.deb" || sudo apt-get -f -y install 

    # Install the khiops python package
    ! pip install "https://github.com/KhiopsML/khiops-python/releases/download/{{ KHIOPS_PYTHON_VERSION }}/khiops-{{ KHIOPS_PYTHON_VERSION }}.tar.gz"
    ```

    [conda]: ../../setup/conda/

<br>

## Data Preprocessing

??? quote "Why is it better to provide raw data to Khiops instead of preprocessed or encoded data?"

    Khiops is specifically designed to work directly with raw data, minimizing the need for manual preprocessing. In fact, **it is strongly recommended to avoid preparing your data** to prevent loss of information, whether it concerns variable encoding, missing values, or data flattening (propositionalization).

    Khiops employs the _MODL_ formalism, based on the MDL (Minimum Description Length) principle, to encode variables optimally:

    - **Categorical** variables: Khiops automatically groups values into clusters based on their correlation with the target variable.
    - **Numerical** variables: Khiops uses discretization to partition values into intervals, ensuring that each interval represents a meaningful range of data relative to the target variable.

    This optimal encoding is inherently tied to the modeling process and adapts dynamically to the data, making manual encoding methods unnecessary (and less effective !).

    **_Example: Why Encoding Isn’t Necessary_**

    Imagine a dataset with a categorical variable "city" containing hundreds of unique values. In a traditional workflow:

    - One-hot encoding "city" would create hundreds of binary columns, resulting in a sparse and computationally expensive matrix.
    - Frequency encoding might lose context, treating "city" as independent from the target variable.

    With Khiops:

    - "City" is automatically grouped into meaningful clusters (e.g., based on correlations with the target variable’s distribution), preserving interpretability and maximizing predictive power.

    Similarly, for a numerical variable "age", Khiops would:

    - Dynamically determine intervals (e.g., [0-18], [19-35], [36-50], [50-97]) based on the correlation between "age" and the target variable.
    - Avoid creating unnecessary intervals, ensuring a balance between simplicity and accuracy.


    **Handling Missing Values**

    Khiops also treats missing values as part of the data, recognizing that they can carry meaningful information. Missing values are not discarded or imputed arbitrarily. Instead, Khiops assigns them to their own group or interval if they are informative for the target variable. This approach ensures that missing data is leveraged effectively, rather than being treated as noise or ignored outright.


    **Scientific Basis**

    Khiops’ preprocessing capabilities are grounded in rigorous statistical principles. The MODL formalism:

    - Automatically balances model complexity and predictive information to prevent overfitting.
    - Dynamically adapts to the structure of the data, selecting groupings or intervals only when they provide significant predictive value.
    - Avoids arbitrary preprocessing decisions by tying encoding directly to the learning objective.


    For more details and examples, see this [notebook tutorial](../../tutorials/Notebooks/No_data_Cleaning/) or read about [Optimal Encoding](../../learn/preprocessing/).

    This approach ensures that manual preprocessing is unnecessary (in fact, it is often counterproductive).




??? quote "Does Khiops Automatically Apply Log, Square, or Other Transformations During Variable Encoding?"
    No, Khiops does not automatically apply transformations such as logarithm, square, or square root based on skewness or other distributional characteristics. Instead, it relies on a non-parametric, information-theoretic discretization approach based on value ranks, *making explicit variable transformations unnecessary.*

    **Why Are Such Transformations Unnecessary in Khiops?**

    Khiops employs the **MODL (Minimum Optimized Description Length)** discretization method, which ensures:

    **Optimal Binning via Information Theory:** The MODL criterion selects the best discretization scheme with the optimal number of intervals and bounds, without requiring parametric assumptions. It directly adapts to the data’s intrinsic structure.
    **Invariance to Monotonic Transformations:** Khiops encodes numerical variables using value ranks rather than raw values. Thus, monotonic transformations (log, square root, exponential, etc.) have no effect on the discretization outcome.
    **Robustness to Skewness and Outliers:** Unlike parametric approaches, Khiops does not rely on moments (mean, variance, skewness) or density estimation, making it naturally resilient to skewed distributions and outliers.
    **No Need for Normalization or Standardization:** Since Khiops operates on ranks rather than raw values, common preprocessing steps like Z-score normalization (subtracting the mean and dividing by the standard deviation) or standardization to 0-1 range, are unnecessary. Feature scaling does not impact the learning process.

    *Conclusion*

    Transformations aimed at normalizing distributions or correcting skewness are unnecessary in Khiops. Its MODL-based encoding automatically adapts to the data, ensuring optimal variable encoding without manual intervention.

<br>

## Model Training & Evaluation

??? quote "Since Khiops does not have hyperparameters, how can I manage overfitting?"

    Khiops avoids overfitting through its core design, which is based on the MDL (Minimum Description Length) principle. This formalism balances the complexity of a model with its ability to explain the data, making Khiops particularly robust.

    **Here’s why Khiops excels at avoiding overfitting:**

    - **Statistically significant patterns only**: Khiops selects only patterns supported by sufficient data, automatically rejecting noise.
    - **No arbitrary parameters**: By avoiding user-defined hyperparameters, Khiops streamlines workflows and reduces the risk of overfitting caused by over-tuning.

    **How Khiops achieves this:**

    Unlike standard models that rely on regularization parameters to control the trade-off between complexity and generalization, **Khiops achieves this balance intrinsically through a mechanism rooted in information theory**. [Our original formalism][modl] penalizes unnecessary complexity by favoring models that explain the data as simply as possible.

    [modl]: ../../learn/modl/

    This ensures that every variable, interval, or aggregate is justified by the amount of information it provides, without requiring external tuning. For instance:

    - A complex derived feature from multi-table data is included only if it significantly improves the model.
    - Similarly, for the encoding of a variable, an interval or a group will only be added if it provides sufficient information to justify its inclusion.

    **Khiops naturally handles noisy datasets by ignoring irrelevant patterns:**

    - When enough meaningful data is present, noise doesn’t affect the model (even if highly present).
    - If the dataset contains too much noise and insufficient data, Khiops will prudently return one single interval.

    While this cautious behavior is a key advantage, it also means that **Khiops performs better and better with more data** (building powerful models requires enough data to justify more complex constructs).

    **Illustration**

    The graph below shows how Khiops’ MODL approach handles the discretization of the “crenel pattern” Class = Sign(Sinus(100πx)), with 10% misclassified instances (as described in [Boulle, 2006, Figure 18][boulle-paperML06]). The x-axis represents the number of instances available in the dataset, while the y-axis shows the number of intervals created by the discretization process. This example is particularly illustrative because it demonstrates how MODL balances complexity and informativity, even in the presence of noise, while avoiding overfitting.

    [boulle-paperML06]: ../../assets/papers/BoulleML06.pdf

    - **Insufficient or noisy data:** When there are too few instances or excessive noise, Khiops keeps only one interval, avoiding unnecessary complexity (such numerical variables will be ignored in the final model as they are considered uninformative).
    - **Optimal intervals:** As more data becomes available, Khiops adjusts dynamically, creating an optimal number of intervals to reflect the data’s structure.
    - **No overfitting:** The number of intervals does not grow indefinitely. In this example, Khiops concludes that 100 intervals are sufficient. Adding more data does not produce spurious intervals, which prevents overfitting

    <picture>
    <img style="max-width:500px;width: -webkit-fill-available" src="../../assets/images/discretization-crenel-pattern.png" alt="discretization of the “crenel pattern" loading="lazy"> 
    </picture>

??? quote "How does Khiops handle datasets with imbalanced classes?"

    **Khiops is robust to class imbalance**, so rebalancing techniques are generally not required.

    However, class imbalance often necessitates collecting large amounts of data to gather sufficient information about the minority class. This can result in very large datasets with billions of records and significantly longer training times. In such cases, rebalancing the dataset can be beneficial.

    The standard approach is **to retain all examples from the minority class and undersample the majority class**. This strategy reduces computation time while preserving critical information. **Never oversample** the minority class, as duplicate instances lead to significant overfitting.

    **Best practices for rebalancing:**

    - Retain all individuals in the minority class.
    - Undersample the majority class only as much as necessary to fit within the available computational resources, ensuring sufficient information is retained for training. In most cases, having up to 100 times more examples than the minority class is sufficient.
    
    **Impact on model performance and scores:**

    - Score ranking: The ranking of scores (used for ranking or thresholding) on a non-rebalanced test set remains consistent. Metrics such as ROC curves and AUC are minimally impacted.
    - Predicted probabilities are completely skewed and unusable because the training set has an artificially higher representation of the minority class. This is typically not an issue, as most applications prioritize score rankings over probabilities.
    - Calibration: If accurate probability estimates are required, apply a calibration method to adjust the predicted probabilities.

??? quote "How does Khiops handle target value grouping, and why is it useful for classification tasks?"

    Khiops’ target value grouping functionality is designed to address challenges when dealing with a large number of target classes. When the number of classes is high, it can be difficult to discriminate between all classes, especially with insufficient number of instances (i.e. with sparse input data).

    To address this, Khiops reduces data sparsity by grouping target classes. In practice: 

    1. **Univariate Preprocessing**: Target class groupings occur during the preprocessing step. Khiops determines the optimal grouping of target values for each variable based on the correlations between the data. The grouped classes are treated as distinguishable from other groups, but classes within the same group are considered indistinguishable.
    2. **Class-level predictions**: The Selective Naive Bayes (SNB) predictor uses the univariate preparations to make precise, class-by-class predictions. While groupings simplify univariate preprocessing, the final model still predicts probabilities for individual classes, not groups.


    **Example: Grouped Target Probabilities**

    In the following example, the explanatory variable x has two distinct values {v1, v2}, and the target variable y has eight classes {A, B, C, D, E, F, G, H}, which are clustered into three groups during preprocessing.

    For x = v1:
    ```
    - P(y ∈ {A, B} | x = v1) = 0.1  
    - P(y ∈ {C, D, E, F} | x = v1) = 0.75 
    - P(y ∈ {G, H} | x = v1) = 0.15
    ```

    For x = v2:
    ```
    P(y ∈ {A, B} | x = v2) = 0.6  
    P(y ∈ {C, D, E, F} | x = v2) = 0.1
    P(y ∈ {G, H} | x = v2) = 0.3
    ```

    In this example, the classifier identifies that distinguishing between groups ({A, B}, {C, D, E, F}, {G, H}) is feasible, but it cannot reliably separate classes within the same group during univariate preparation.

    Because this grouping is done independently for each explanatory variable, a different grouping could occur for another explanatory variable z. For example:

    For z = v0:
    ```
    P(y ∈ {A, D, H} | z = v0) = 0.6  
    P(y ∈ {B, C, E, F, G} | z = v0) = 0.4
    ```
    The SNB predictor later uses this variable-specific grouped information from all explanatory variables to make precise, individual class predictions.

    **Additional Insights**

    In some cases, it may be beneficial to globally reduce the number of target classes for the entire problem. The univariate preparation reports generated by Khiops can help data miners identify frequently occurring groupings, guiding decisions about merging or removing target classes altogether.

<br>

## API, Integration & Deployment

??? quote "Can Khiops be deployed on Hadoop?"

    Yes, Khiops has been used for several years in production on Hadoop using specialized tools we have developed. However, these components are not yet part of its open-source distribution.

    **Overview of the technical solution**

    We have developed the following components to enable Khiops integration with Hadoop ecosystems:

    - **HDFS driver for Khiops**: A dedicated driver enabling Khiops to read and write directly from HDFS, with full support for multipart files;
    - **Khiops4Spark**: A Spark wrapper that enables Khiops to run on Hadoop clusters through `spark-submit` command;
    - **Khiops4Yarn**: A Yarn wrapper that allows Khiops to operate directly within Hadoop’s resource management framework.

    Khiops, as a native MPI (Message Passing Interface) program, works exactly the same on a multicore machine or on a multinode cluster. When deployed on multiple machines, Khiops efficiently leverages the CPU, memory, and I/O resources of each allocated node, ensuring optimal performance at scale. The Spark and Yarn wrappers manage the communication with their respective resource managers, which in turn allocate resources that will be used by Khiops.

    If you’re interested in deploying Khiops in such environments or have specific use cases, please reach out via our [contact form](../contact/) for further information.

??? quote "Can I use Polars instead of Pandas as input format for Khiops?"

    Currently, *Khiops does not support polars.DataFrame* as input for the `khiops.sklearn` Python estimators. 

    However, if you’re concerned about the *performance or scalability limitations* of in-memory structures like Pandas (or Polars), we recommend using the `khiops.core` *API* instead. This low-level interface is designed for *high-throughput, large-scale processing*. It operates directly on raw text files, bypasses in-memory DataFrames entirely, and provides *native access to cloud file systems* (S3, GCS, Azure, HDFS, etc.).

    > The `khiops.core` API is fully documented on our website, with tutorials showing how to train, evaluate, and deploy models efficiently—using only files and command-line workflows.

    Khiops has been developed and refined for over 20 years with a strong focus on *native scalability* and *multi-table processing*—a key requirement at Orange, *where telecom usage logs generate massive amounts of data* across multiple relational tables.

    In production, we routinely process *billions of records* using Khiops. The full modeling pipeline—including *automated feature engineering* with over *10,000 computed aggregates*—can be completed in about *one hour on a single machine*, starting from hundreds of gigabytes across five relational files (user info, calls in/out, SMS in/out). Distributed execution on Kubernetes makes this even faster.

    While adding Polars support remains a possible enhancement for future releases (see issue #292), for serious data workloads we strongly recommend leveraging the `khiops.core` API.

