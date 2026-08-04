# Scalability and Large Datasets

This page centralizes practical questions related to industrial-scale usage of Khiops.

!!! question "Have a question or request?"
    - **Ask in [GitHub Discussions](https://github.com/orgs/KhiopsML/discussions)**
    - **Report bugs or request product changes in the [Khiops repository issues](https://github.com/KhiopsML/khiops/issues)**

## Index of questions

1. [How to train a model using very huge initial datasets: methodological advice needed](#how-to-train-a-model-using-very-huge-initial-datasets-methodological-advice-needed)
2. [Allow user to deactivate Khiops memory dimensioning](#allow-user-to-deactivate-khiops-memory-dimensioning)
3. [Elephant instances in multi-table databases](#elephant-instances-in-multi-table-databases)

---

## How to train a model using very huge initial datasets: methodological advice needed

Users who have a lot of data (hundreds of giga bytes) often struggle when training a model. They need a how to in order to sample the input data to avoid using the whole dataset at the first stages. A tutorial is welcome to guide step by step the user. An important demand is to respect the initial data distribution especially if it is highly unbalanced.

**Training a Model with a Huge Database**

**Context of Big Data**

When dealing with a real data mining problem, you may have a huge database, potentially containing terabytes of data. This is likely to happen in the case of a multi-table database, where your main analyzed instances are described with detailed records stored in secondary tables.

For example, if your entity is a customer, you may have many logs per customer:

- Purchase details in marketing
- Call detail records in telecommunications
- Web navigation logs
- ...

At Orange telecommunications, there are tens of millions of customers in France, each with thousands of logs in secondary tables, amounting to tens of billions of logs at terabyte scale.

**Objective**

The objective is to train a model efficiently.

You need to build a flat analysis dataset, with instances in rows and variables in columns, to train your model. Given the multi-table database, you have to construct features per instance from the secondary records to obtain your flat analysis dataset.

Processing the whole database while constructing many features is not an option, given the prohibitive computational resources required.

!!! note
    For example, if you have a database of 10 million customers, with 100 logs per customer, and want to construct 100,000 features per customer, you need:

    - 8 TB of disk space to store your analysis dataset: 10 million × 100,000 features = 1,000 billion values, at approximately 8 bytes per value
    - 100,000 billion read and computation operations from log values, as each constructed value is computed from 100 logs on average

    This type of analysis is possible with Khiops, but it will require very large computational resources (disk, RAM, CPU).

**Methodology for Training and Deploying a Model**

You need to extract an analysis dataset from the whole database to perform your data mining study efficiently.

Three steps are necessary:

- Extract an analysis dataset from the whole database
- Perform your data mining study on the analysis dataset, to evaluate different modeling scenarios and choose the best one
- Deploy the best model on the whole database, to get predictions for all instances

The first and last steps are data-intensive, as they involve scanning the whole database, while the second step is computationally intensive, as it involves many tests and trials of modeling scenarios.

**Analysis Dataset**

The analysis dataset needs to be:

- Representative of the data under study
- Large enough to reduce the variance of the results
- A reasonable size, to enable fast analysis times

**Representative**

Your dataset must fall within the same perimeter as your study. For example, if the business objective is a marketing campaign targeting young customers in big cities, your analysis dataset must be within the same perimeter.

Within this perimeter, your instances must be chosen at random. For example, if you need an analysis dataset containing 100,000 instances, do not take the first 100,000 instances from your database, or those with the first 100,000 identifiers. You really need a random sample.

**Large Enough**

Your analysis dataset must be large enough to provide reliable results, in order to determine whether the business objectives are fulfilled with good confidence.

As a rule of thumb, the standard deviation of an evaluation criterion (e.g. accuracy) is around \(1/\sqrt{n}\) for a sample of size n.

For example, in a political poll involving tens of millions of voters, samples are usually taken of size n=1,000, implying a margin of error of around 3% (\(1/\sqrt{1000} \approx 0.03\)).

The following table indicates error margins for several sample sizes:

| Sample size | Error margin |
|---|---|
| 100 | 10% |
| 1,000 | 3% |
| 10,000 | 1% |
| 100,000 | 0.3% |
| 1,000,000 | 0.1% |

Choosing a sample size of between 1,000 and 10,000 looks like a good trade-off, as it provides good confidence in the evaluation criteria, with a small error margin, while remaining fast to process during the data mining study.

!!! note
    If your dataset involves categorical variables with many values (e.g. first name or city zip code), a larger sample may be necessary to capture enough occurrences of each value and potentially extract more information from these variables.

**Case of Unbalanced Datasets**

The rule of thumb applies to balanced datasets: see Q&A [discussion #474](https://github.com/orgs/KhiopsML/discussions/474).

In the case of unbalanced datasets with a rare minority class (e.g. churner), you should ensure the requested sample size is met for the rare class. For example, in a churn study with around 1% churners in your database, to have between 1,000 and 10,000 churners in your sample, as recommended, you need a sample of size between 100,000 and 1,000,000.

In this case, it might be a good idea to extract an enriched analysis dataset from the analysis dataset, containing all instances of the rare class and a subset of the frequent ones. As a rule of thumb, a sample of approximately 10 times the number of rare instances is a good trade-off. The quality of your model will be roughly the same, while being far faster to train.

!!! note
    Using an enriched analysis dataset can speed up training, but the evaluation criteria will be biased, as the proportion of churners will differ from that in the whole database. To obtain a correct evaluation, you can use the whole analysis dataset, with the correct proportion of churners, to evaluate the model trained on the enriched analysis dataset.

!!! note
    For example, in a churn study involving an analysis dataset of size 100,000 with 1,000 churners, you can extract an enriched analysis sub-dataset containing all 1,000 churners and around 10,000 non-churners. You obtain a sub-dataset about 10 times smaller, which is far faster to process than the whole analysis dataset.

**Reasonable Size**

A data mining study involves many tests and trials using your analysis dataset.

You must first divide your analysis dataset into:

- Train dataset: to train the model
- Test dataset: to obtain a fair evaluation of the model's performance on the whole database

The training phase involves several scans of the data, for data preparation, modeling, and evaluation. This process must be repeated to evaluate different modeling scenarios, with varying numbers of constructed features in the multi-table setting, varying numbers of trees, etc. To be able to evaluate many modeling scenarios rapidly, you should adopt a fail-fast strategy and allow train-test round trips to complete as quickly as possible.

Note that the requirements in time, energy, and cloud costs are at least proportional to the sample size.

!!! note
    For example, with a training database of 10 million instances, the training time with a sample of size 100,000 will be at least 100 times smaller than with the whole database.

You need to extract the analysis dataset once and for all, to avoid scanning the whole database each time you evaluate a new modeling scenario.

**Using Khiops for the Whole Process**

**Extraction of the Analysis Dataset**

When you extract an analysis dataset from the whole database, you need to extract a representative sample of your analyzed instances, together with their secondary records for each secondary table of the multi-table schema.

With Khiops, you simply perform a Deploy model applied to the whole database to extract your analysis dataset:

- In the data dictionary (`.kdic`), use all native variables (not derived) and do not use any derived variables, in order to obtain tables with exactly the same structure
- Define the perimeter of your study using a selection variable that describes the instances to collect
    - e.g. to select customers under 40 years old, use a derivation rule such as:
```
Unused Numerical InPerimeter = LE(age, 40);
```
- Use a sampling percentage to obtain an analysis dataset of the desired size

In the case of a multi-table database, you simply specify one file per secondary table to obtain the secondary records for the selected instances.

**Training a Model on the Analysis Dataset**

With your analysis dataset, you can perform your data mining study, evaluate different modeling scenarios, and choose the best one.

With Khiops, use Train model with the default 70% train-test split, and evaluate training scenarios by increasing complexity, starting with few constructed features (e.g. 1,000 constructed features and no trees), up to at most 100,000 features and 1,000 trees.

In the case of an unbalanced dataset, you can extract an enriched analysis dataset to speed up training. For example, to extract all churners and 10% of the other instances, use a selection variable such as:
```
// Return 1 if the class is "Churner", 1 otherwise if Random() is less than or equal to 0.1, 0 otherwise
Unused Numerical InEnrichedSample = If(EQc(Class, "Churner"), 1, LE(Random(), 0.1));
```

In the case of a huge dataset with highly unbalanced classes, even the analysis dataset may be too large to process efficiently. In this case, you can directly extract the enriched analysis dataset by combining a selection variable and a sampling percentage within the same Deploy model run.

Choose the best modeling scenario with the best evaluation criteria, and verify that the business objectives are fulfilled.

!!! tip
    Do not spend too much time refining the trained model if you already obtain a good enough evaluation criterion. Improving test accuracy by 0.2% may not be worthwhile if it is well below the error margin related to the size of your dataset. Do not forget all the business objectives of your study, such as interpretability, deployment time, and costs, which may be more important than a small improvement in accuracy.

!!! note
    Remember that the scoring process is just one step within a project, which may involve subsequent steps with large variance. For example, the effectiveness of a marketing campaign is likely to vary considerably depending on the quality of the messages sent to customers.

**Deploying the Model on the Whole Database**

With Khiops, you simply perform a Deploy model applied to the whole database to build a score for all customers within your perimeter.

!!! tip
    A simpler model will be faster and cheaper to deploy on the whole database, and may be sufficient for your business objectives.

*Source: [discussion #1006](https://github.com/orgs/KhiopsML/discussions/1006)*

---

## Allow user to deactivate Khiops memory dimensioning

Khiops sometimes prevents the execution of a data mining workflow, citing a lack of memory based on a rough estimate of the required memory. After using a machine with significantly more available RAM, we often notice that far less memory was actually used during the process. Allowing Khiops to run the task regardless of the available resources would be more convenient. After all, if I know my data well, Khiops simply prevents me from analyzing it in a too conservative manner. And if the program crashes, well, that's what can happen with all alternative methods, such as Scikit-Learn: why bother?

**Khiops Policy Regarding Resource Management**

**Main Objective: Never Crash**

- Khiops is an AutoML solution designed to be as simple and robust as possible to use.
    - The only user parameters concern the specification of the data analysis problem or business constraints, such as modeling speed, accuracy, or interpretability.
    - Technical parameters are never exposed to the user.
- The tool is intended for use in an industrial context.
    - It should never crash, regardless of the scale or complexity of the data to analyze, or the available resources.
    - Business constraints and deadlines for delivering scores are of key importance.
- Importance
    - A crash is likely to be highly costly for an operational team.
    - It is impossible to determine whether the crash originates from a bug or a lack of resources.
    - Testing and trials by running a task under different resource configurations (number of machines, cores, available disk, RAM) are not compatible with industrial constraints.

**Khiops Policy Regarding Resources**

- Khiops exploits available resources as much as possible to maximize the speed of task execution.
- How:
    - Each internal algorithm evaluates the minimum necessary resources to run the task.
    - Given that, Khiops uses as many cores as possible, provided sufficient RAM is globally available.
    - If all data cannot fit into memory, Khiops splits the data:
        - Into chunks of instances for algorithms that can be decomposed on instances (e.g., deployment).
        - Into chunks of variables for algorithms that can be decomposed on variables (e.g., preprocessing).
    - If there is not enough memory even after applying the splitting strategy:
        - The user is provided with an estimate of the minimum additional memory required.
- This allows for out-of-core processing:
    - For example, analyzing a 9 GB dataset using one core and 512 MB RAM.
    - See [Khiops Hardware Adaptation](https://khiops.org/learn/hardware_adaptation/#lets-run-an-experiment).

**Why It Sometimes Fails**

- Estimating the necessary resources in advance is challenging due to many unknown data characteristics:
    - Number of selected instances in case of a selection criterion.
    - Number of missing values.
    - Data sparsity (e.g., texts).
    - Number of distinct values for numerical or categorical variables.
    - Length of categorical values.
    - Number of informative variables.
    - Number of secondary records per main record.
    - Etc.
- The principle for these evaluations is to iteratively gather information about the data after each analysis pass:
    - Basic statistics for the number of main instances and target variable values.
    - Descriptive statistics.
    - Preprocessing metrics.
    - Etc.
- Although Khiops can manage very large datasets using its out-of-core strategy, the number of main instances may still be too large.
    - Example: If there are 100 million instances in the main table:
        - Needs 100 million values simultaneously for univariate preprocessing: at least 800 MB.
        - Requires provisioning enough RAM for complex algorithms used in data preprocessing.
        - Example: around 100 bytes per value for double-linked lists, including value, criterion contribution, merging structures.
        - Total requirement: approximately 10 GB.
- If a numerical variable is actually a boolean with only two distinct values, the resource requirement may be excessively high.
    - Conversely, if a variable is truly continuous with as many distinct values as instances, the resource needs are different.
    - This can happen with a single variable added to a Khiops dictionary (e.g., using the Random rule) or generated automatically (e.g., variance of a secondary variable).

**How to Improve This**

- Estimating required resources remains a challenge; please report extreme cases where this estimation is clearly too conservative.
- This issue is most likely to occur when a huge number of instances are kept for analysis.
    - Use sampling or instance selection to reduce the data volume.
    - Remember that increasing the number of instances may improve results but with diminishing returns:
        - 10,000 to 100,000 instances: likely beneficial.
        - 100,000 to 1,000,000: may be relevant in some cases.
        - 1,000,000 to 10,000,000: will significantly increase processing time and cost, with unlikely improvements.

*Source: [discussion #934](https://github.com/orgs/KhiopsML/discussions/934)*

---

## Elephant instances in multi-table databases

**Definition**

In multi-table databases, a main entity (for example, a customer) is described by many records in one or more secondary tables (for example, purchase logs).

"Elephant instances" are entities with so many secondary records that loading them into memory is impractical or impossible. Common examples are telecommunication subscribers with massive call detail records (CDRs) and users whose navigation or event logs on a website or app grow extremely large. This most often occurs in B2B contexts where a few entities produce far more records than typical.

**Problems caused by elephant instances**

Feature engineering usually computes variables for each main entity by loading the entity together with all its secondary records and summarizing them (e.g., number of logs, number of distinct products, total amount, per-day or per-category aggregates).

This process can fail for two main reasons:
- insufficient memory to store all secondary records;
- insufficient spare (working) memory for the computations themselves.

When frameworks cannot handle these cases they may crash or stop processing, which is unacceptable for production pipelines and critical scoring systems.

**How Khiops handles elephant instances**

Khiops is designed to process multi-table data robustly and to avoid crashes or pipeline interruptions when elephant instances occur. It applies different strategies depending on the situation.

**Instances too large to load into memory**

Native variables are fields stored on the main entity record (e.g., customer attributes) and do not require loading secondary tables.

If an instance cannot be loaded, Khiops keeps only the native variables from the main entity; all engineered features are marked missing because they could not be computed.

Khiops emits a warning with detailed information regarding lack of memory to load elephant instances.
```
warning : Database ./customer_dataset.txt : Record 340 : Single instance [USER_000340] requires too much memory (more than 812.0 MB of RAM)
after reading 4,915,210 secondary records out of 5,105,000 : only the native variables are kept, the others are defined as missing values
```

**Instances that fit but lack working memory for computation**

If the instance can be loaded but there is not enough spare memory to compute features, Khiops may skip feature computation for that instance and keep only native variables (engineered features set to missing).

Khiops emits a warning with detailed information regarding lack of memory to process elephant instances.
```
warning : Database ./customer_dataset.txt : Record 550 : Single instance [USER_000550] requires too much memory (more than 967.0 MB of RAM)
after reading 4,105,000 secondary records and calculating the values of 35 variables out of at least 3353 : 
only the native variables are kept, the others are defined as missing values
```

**Instances handled by multiple passes (time trade-off)**

When memory is tight but recoverable, Khiops will free memory periodically and compute features iteratively across several passes. All derived variables can be computed at the cost of additional computation time.

Khiops notifies the user that computation completed using multiple passes to save RAM.
```
warning : Database ./customer_dataset.txt : Record 730 : Single instance [USER_000730] containing 3,507,000 secondary records : 
all derived variables have been computed using RAM sparingly at the expense of computation time (6 additional passes)        
```

**Instances that should be noticed**

When an instance is large but handled normally, Khiops still emits a warning so the data miner is informed.

Khiops issues a notice to highlight unusually large instances for review.
```
warning : Database ./customer_dataset.txt : Record 890 : Single instance [USER_000890] containing 397,620 secondary records
```

**Recommendations**

To reduce the occurrence or impact of elephant instances consider:
- Increase available RAM where possible.
- Reduce parallelism (fewer workers/cores) to increase RAM per worker.
- Pre-aggregate by time window or sample older/less relevant records.
- Use approximate algorithms (HyperLogLog, Count-Min Sketch) for large-cardinality or heavy-hitter estimates.

*Source: [discussion #1104](https://github.com/orgs/KhiopsML/discussions/1104)*
