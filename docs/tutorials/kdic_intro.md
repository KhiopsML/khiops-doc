## Benefits of Using Khiops Dictionaries

Using the Khiops Core API, particularly through the manipulation of Khiops dictionaries, significantly accelerates the deployment of machine learning models into production. By enabling users to easily describe their data and incorporate business knowledge during the data preparation step, dictionaries streamline workflows and enhance efficiency. Moreover, they serve as a comprehensive record of all manual and automated processing steps required for model training, and are executed seamlessly by Khiops during inference.

The main user benefits include:

- **Meaningful data description**: In its simplest form (a single training data table), the dictionary describes the variables, with their names and types. For more complex data spread across multiple tables, the dictionary also encodes relationships by linking tables, treating a secondary table as a "variable" of the table it is linked to. This approach allows users to easily define and structure data into a comprehensible relational schema, even for advanced setups such as snowflake schemas (see examples in the [multi-table learning page][kdic_multi_table]).
  
[kdic_multi_table]: kdic_multi_table.md

- **Meaningful data preparation**: The user simply expresses their business knowledge by selecting the relevant information for the problem at hand and enriching data with relevant user-defined variables. These enrichment rules are similar to SQL expressions, allowing users to define new variables with intuitive logic (e.g. using the mathematical rules described [here][math-rules]). 

 [math-rules]: ../api-docs/kdic/math-rules.md

During training, the dictionary provided by the user is automatically enriched to implement the entire data transformation flow of the machine learning pipeline, from mapping available data sources to predicting the target variable. For instance, during the automated feature engineering phase, new aggregates are generated and added to the dictionary as variables (the predefined functions used to create these aggregates are listed [here][auto_feature_engineering]).

[auto_feature_engineering]: ../learn/autofeature_engineering.md#model-parameters

The main technical benefits include:

- **Agile model release**: A single dictionary file encodes an entire data transformation flow, enabling predictions to be made directly from the raw data. Furthermore, updating a model simply involves replacing a file, what ensures straightforward versioning, traceability, and easy rollbacks using standard tools like `git`.

- **On-the-fly processing**: Data transformation is implemented dynamically, which means that variables are computed only when required during execution, rather than being precomputed and stored. For instance, the aggregates defined during the Auto Feature Engineering step are instantiated just-in-time for predictions. This minimizes RAM usage, avoids storage overhead, and ensures scalability for large-scale datasets. 

- **Distributed computing and Out-of-core**: Khiops' low-level implementation ensures data transformations are executed with exceptional efficiency, dynamically adapting to [available hardware resources][auto-adaptation]. The initial learning task is divided into sub-tasks, either due to limited RAM (out-of-core processing sequentially loads sub-parts of the data) or to distribute processing across a cluster of computers. This makes Khiops not only a powerful modeling tool but also a lightweight solution for scalable data transformation.

[auto-adaptation]: ../learn/hardware_adaptation.md
 
## What Is a Khiops Dictionary? 

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_as_a_program.webp" type="image/webp">
  <img style="width:48%;" src="/assets/images/dictionary_as_a_program.png" alt="dictionary_as_a_program" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>


!!! success "A dictionary is a program that describes and transforms data"
    Dictionaries are written using a declarative programming language dedicated to both data **definition** and **manipulation**. Thus, a dictionary includes a specification of the data itself (i.e. definition), as well as the transformations to be applied (i.e. manipulation).  


## How Are Dictionaries Used? 

This section illustrates how dictionaries are used throughout the machine learning pipeline: (i) who writes the dictionaries; (ii) what are they used for.   

### Data Description and Preparation 

In the standard case of machine learning, where training data is encoded in a single-table format, the dictionary file provided by the user takes its simplest form, just describing the variables with their names and types.

!!! success "Example of a simple dictionary describing a single training table"
    ```kdic
    Dictionary	iris
    {
        Numerical	SepalLength	;
        Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;
    };
    ```

However, in most industrial applications, raw data is scattered across multiple, loosely organized sources. In these cases, dictionaries play a crucial role in organizing the data. To be read by Khiops, these sources must provide formatted data, typically CSV, log or text files. At this stage, the goal is to produce structured and enriched data that reflects business knowledge and is comprehensible to stakeholders.    

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_data_preparation.webp" type="image/webp">
  <img style="width:70%;" src="/dictionary_data_preparation.png" alt="data preparation" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! abstract "What the user writes ✍️"
    
    The **user** writes an initial dictionary to describe and prepare the data:
    
    - **Description:** (i) Mapping available data sources to tables, (ii) selecting relevant tables and variables, (iii) defining relationships between tables, and (iv) specifying variable types.
     
    - **Manipulation:** (i) Selecting training examples (e.g., filtering by time period), and (ii) coding new user-defined variables to integrate business knowledge.
 

### Training Stage 

During training, the machine learning pipeline is executed in two stages. First, pre-processing is performed, including both [auto feature engineering][auto_FE] and [optimal encoding][optimal_encoding]. Then, the [parsimonious training][parcimonious_train] stage combines the univariate pre-processing steps to obtain a multivariate predictive model.   

[auto_FE]: ../learn/autofeature_engineering.md
[optimal_encoding]: ../learn/preprocessing.md
[parcimonious_train]: ../learn/learning_models.md

**1) Pre-processing**

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_train_1.webp" type="image/webp">
  <img style="width:100%;" src="/dictionary_train_1.png" alt="training 1/2" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! abstract "What Khiops writes automatically ✍️"
    
    The dictionary initially provided by the user is **automatically enriched** in order to (i) compute a large number of informative aggregate variables, and (ii) to define the rules used to encode each variable into intervals or groups.

**2) Parsimonious training**

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_train_2.webp" type="image/webp">
  <img style="width:70%;" src="/dictionary_train_2.png" alt="training 2/2" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! abstract "What Khiops continues to write ✍️"
    
    Finally, this dictionary is modified (i) to select a subset of informative and independent variables, and (ii) to compute target predictions based on the encoded variables. 

### Model Release in Production Stage

At the end of training, predictions can be made directly from raw data, which facilitates model productionalization in two aspects. 

- Updating a model involves simply replacing the dictionary file, as long as the raw data format remains unchanged, without changing anything else in the project. 

- The trained model's archive includes the complete data transformation flow, eliminating the need to maintain external pre-processing code and mitigating risks from versioning conflicts. 

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_deploy.webp" type="image/webp">
  <img style="width:70%;" src="/dictionary_deploy.png" alt="using a model" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! abstract "What the user and Khiops wrote together"
    
    The final dictionary integrates both the **data preparation** provided by the user and the **data transformation flow** applied by Khiops during training.
    





