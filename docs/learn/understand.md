# What makes Khiops different

Khiops is an end-to-end solution for **Automated Machine Learning** (AutoML), natively and effortlessly handling intricate Data Science time-consuming tasks. These include feature engineering (A), data cleaning and encoding (B), and the training of parsimonious models (C).

<picture>
  <source srcset="/assets/images/auto-ml-pipeline.webp" type="image/webp">
  <img style="max-width:945px;width: -webkit-fill-available;" src="/assets/images/auto-ml-pipeline.png" alt="auto-ml-pipeline"> 
</picture>


The Auto-ML capability allows Khiops to expertly process tabular data, regardless of whether it comes in single-table format, or in the form of **relational data sets**, including those with complex "snowflake" schemas. This becomes a distinctive asset in various situations, particularly when addressing use-cases with multiple records per statistical individual (such as calls, transactions, or production logs). Khiops handles these scenarios seamlessly and automatically, **making it an invaluable tool for extracting rich insights from complex datasets**.

The distinctiveness of Khiops lies in its departure from typical AutoML solutions that often run an expensive range of complex algorithms over putative sets of parameters in a grid search manner. Instead, Khiops employs **an original formalism** called [MODL][publications] (which is hyperparameter-free), enabling it to push boundaries by enhancing automation levels. As a result, it can build high-performance models that retain simplicity for **ease of interpretation**. Moreover, this approach supports impressive **scalability**, setting a new benchmark in machine learning.


<picture>
  <source srcset="/assets/images/Khiops-advantages.webp" type="image/webp">
  <img style="max-width:400px;width: -webkit-fill-available;margin-top:30px" src="/assets/images/Khiops-advantages.png" alt="Khiops-advantages" loading="lazy"> 
</picture>


## Advanced Automation 

Khiops significantly enhances the productivity of data scientists by seamlessly automating numerous time-intensive tasks. Key benefits include:

- **Automated Data Cleaning**: Khiops alleviates the need for manual data cleaning, and the training of models remains unaffected by outliers. It minimizes the need for intricate preprocessing and outlier detection, saving valuable time.
- **Native Processing of Variables**: Khiops adeptly manages all data types without requiring manual encoding. Categorical variables are naturally grouped, and numerical variables are cleverly divided into intervals, making it easier for the models to find patterns and relationships. 
- **Auto Feature Engineering**: Khiops automatically calculates and selects the summarizing 'features' or 'aggregates' from temporal and relational datasets (in a unique way thanks to the MODL approach), providing a concise, informative snapshot that can be readily used for modeling. This saves considerable time and effort while ensuring that essential data patterns are not overlooked.
- **Efficient Variable Selection Algorithms**: Khiops employs two sophisticated variable selection techniques. Firstly, during the optimal encoding phase (B), it weeds out variables that lack correlation with the target using Compression Gain. Secondly, during the parsimonious learning step (C), it handpicks a compact subset of the most informative and mutually independent variables.

The remainder of the section introduces the **auto-features engineering** step.

!!! info "This section only introduces the concept. For technical details, please refer to the :orange_book: [Auto features engineering][auto_features_enginnering] section."
 [auto_features_enginnering]: autofeature_engineering.md

**Relational data structures are common in many professional environments**, encompassing data on users (e.g., call or payment logs) or production data where each step generates its records. In such contexts, we deal with a primary table of statistical individuals (potentially the targets for supervised learning) and secondary tables that contain the related logs.

**Mining insights from these datasets is definitely more intricate than working with straightforward, single-table datasets often utilized in tutorials**. The crux of this complexity lies in the fact that each individual can be linked to multiple records in the secondary tables, and it's not feasible to uniformly assign these records to the individual class. In other words, handling relational data for predictive modeling calls for a specialized approach, which is where Khiops comes in.

Consider a brief example: the goal is to identify call spammers using call log data. The primary table contains the list of customers along with the target attribute (*is a fraudster or not*). Complementing this, secondary tables detail 'in' and 'out' calls for each customer, some having more than thousands of rows.

<figure markdown>
<picture>
  <source srcset="/assets/images/wrong_relation_data_pipeline.webp" type="image/webp">
  <img style="width:100%;" src="/assets/images/wrong_relation_data_pipeline.png" alt="wrong_relation_data_pipeline" loading="lazy"> 
</picture>
  <figcaption>The wrong way to get information from additional tables</figcaption>
</figure>

In that example, it's essential to acknowledge that **a single call doesn't define an individual as a fraudster** - it is the overall pattern of their calls that can lead to this classification (e.g., a high volume of *out* calls but no *in* calls or consistently different recipients).

It is not feasible, or indeed correct, to map the customer's target outcome to each of their calls (rows), then attempt to train a model on all these rows in a homogeneous manner. Such an approach fundamentally **alters the 'statistical individual'** under consideration from the customer to the calls, thereby violating the principle of *independent learning examples*.

Instead, the ideal approach is to derive **features that encapsulate the call logs**, effectively summarizing customer behaviors. For instance, one could consider features such as the daily count of 'in' and 'out' calls (corresponding to the number of rows linked to individuals in the secondary tables), the average duration of calls, or the number of unique contacts.

<figure markdown>
<picture>
  <source srcset="/assets/images/relation_data_pipeline.webp" type="image/webp">
  <img style="width:100%;" src="/assets/images/relation_data_pipeline.png" alt="relation_data_pipeline" loading="lazy"> 
</picture>
  <figcaption>Getting aggregates from additional tables (group by)</figcaption>
</figure>

The outcome of this process is a streamlined dataset - a single row for each individual, containing both **the original variables from the primary table and the newly engineered features (or aggregates) that encapsulate the supplementary information from the secondary tables**. 

Performing this step manually would be time-consuming, carry technical constraints, and can be suboptimal. The limitations of human perception and inherent biases can obstruct the comprehensive exploration of potential aggregates. Additionally, any shift in the target - such as a new business objective - necessitates a fresh round of feature engineering.

One of the strengths of Khiops lies in its automation of this complex step. By leveraging the MODL approach, Khiops effectively examines numerous candidate aggregates from the secondary tables, retaining only those whose informational value outweighs their associated complexity. Consequently, **Khiops stands out as a solution that automates feature engineering while circumventing the pitfalls of overfitting**.


!!! example "See what Khiops-built aggregates look like using our tutorials [here][tuto_aggregates]."

[tuto_aggregates]: ../advanced/Notebooks/Use_in_any_ML_pipeline.ipynb "See the Jupyter Notebook"

## Interpretability

Khiops emphasizes interpretability throughout its implementation pipeline, aligning with critical industrial requirements:

- During the **auto feature engineering phase** (Step A), the aggregates produced bear explicitly descriptive names that mirror their calculation formulas. Khiops helps users to deepen their data comprehension by suggesting valuable aggregates for their specific task - aggregates that may have eluded even the sharpest business expertise.

- In the **optimal encoding phase** (Step B), effective and simplistic models are trained for discretization and grouping. This helps users to promptly grasp the predictive class distribution for each explanatory variable.

- During **parsimonious training** (Step C), after a rigorous aggregate search in Step A, the goal is to significantly reduce the number of utilized variables. This approach simplifies model analysis for data scientists. Moreover, the chosen variables are as independent as possible, enabling easy, additive analysis of their contribution to predictions.

Khiops is coupled with an interactive [**visualization tool**][visu], providing direct access to extensive pipeline results from a notebook or a dedicated application. The upcoming section offers a glimpse into visualizing variable encodings.


 [visu]: ../setup/demovisualization.md "Try it via our interactive demo!"


!!! info "This section only introduces the concept. For technical details, please refer to the :orange_book: [optimal encoding][preprocessing] and :orange_book: [visualization tool][visu] sections."

  [preprocessing]: preprocessing.md

While the final pipeline stage (**C**) leverages all variables to train models, preprocessing step (**B**) constructs univariate models for each variable. A key advantage of employing the MODL approach at this stage is that **it facilitates auditable and interpretable variable encoding**. Khiops practically encodes every variable into a discretized feature: **splitting numerical values into intervals** and **grouping categorical values**. The encoding aims to strike a balance between target prediction accuracy and encoding complexity (viz. the overfitting risk).

Consider a new example: predicting whether adult revenue falls *above* or *below* $50k. During preprocessing, Khiops analyzes every variable, partitioning numerical variables, such as *age*, into intervals. If **accuracy is prioritized, it will generate as many intervals as there are unique values**. However, **if complexity is minimized, only one interval is created**. Leveraging the MODL approach, **Khiops finds an optimal balance** without requiring parameter tuning. The visualization component of Khiops depicts the *age* variable encoding as follows:

<figure markdown>
<picture>
  <source srcset="/assets/images/KhiopsViz_Adult.webp" type="image/webp">
  <img style="width:100%;" src="/assets/images/KhiopsViz_Adult.png" alt="KhiopsViz_Adult" loading="lazy"> 
</picture>
  <figcaption>Discretization of the age variable on the Khiops Visualization tool</figcaption>
</figure>

The number of available training samples impacts this balance. More data leads to more precise discretization or grouping. **Doubling the number of individuals in our example would result in a more detailed interval structure.**


<figure markdown>
<picture>
  <source srcset="/assets/images/adult_sample_size.webp" type="image/webp">
  <img style="width:100%;" src="/assets/images/adult_sample_size.png" alt="adult_sample_size" loading="lazy"> 
</picture>
  <figcaption>Discretization of the age variable depending on the number of training examples</figcaption>
</figure>

In conclusion, Khiops' encoding provides insights into our data by offering a thorough variable analysis. The entire Auto ML pipeline is intuitively interpretable. For a comprehensive overview of the features offered by the Khiops visualization component, please refer to the relevant [section][visu].


## Outstanding Scalability

The Khiops MODL approach automatically adjusts model complexity based on available training data without needing hyperparameters. As a result, it uses algorithms that inherently **avoid overfitting** right from the training stage without the need for model evaluation on validation data.

This distinctive feature brings about **exceptional scalability**. Since Khiops is free from hyperparameters, it eliminates the need for time-consuming and resource-intensive steps such as cross-validation and grid search.

Additionally, thanks to efficient low-level coding, Khiops can operate across a wide range of hardware environments. Even when the hardware resources are insufficient to load the entire training set into RAM (this is also known as "out-of-core" training), Khiops still manages to function effectively.

Furthermore, **Khiops can seamlessly transition between out-of-core and distributed computations** due to its [strategy of adapting][auto_hardware_adaptation] to available hardware resources. That makes it flexible and versatile, able to accommodate various operational requirements and constraints.

<picture>
  <source srcset="/assets/images/bench_hardware_short.webp" type="image/webp">
  <img style="max-width:400px;width: -webkit-fill-available" src="/assets/images/bench_hardware_short.png" alt="bench_hardware_short" loading="lazy"> 
</picture>


 [auto_hardware_adaptation]: hardware_adaptation.md
 [modl]: modl.md 
 [publications]: ../references.md#publications "See scientific references"





!!! abstract "Deep Dive into MODL: An Overview and Guide"
    The remainder of this documentation's **Understanding** section aims to demystify the MODL approach and illustrate its applications across the Auto ML pipeline. The content is presented pedagogically, so it is crucial to maintain the prescribed reading sequence. Those seeking a more thorough scientific comprehension should browse the collection of bibliographic [references][references], organized as a reading guide.

[references]: ../references.md
