
## Benefits of using Khiops dictionary

Using the Khiops Core API, in particular by manipulating Khiops dictionaries, significantly accelerates the release of machine learning models into production, by enabling users to easily describe data and express their business knowledge during the data preparation step. What's more, the dictionaries record all the manual and automatic processing required for model training, and are executed by Khiops during the inference phase. The main user benefits include:

- **Meaningful data description**: in its simplest form, the dictionary describes the variables in a single training data table, with their names and types. With more complex data, for instance spread over several tables, the power of dictionaries represents a major advantage. Starting from a multitude of disorganized data sources, the user can easily describe and structure training data into a comprehensible relational schema. 
  
- **Meaningful data preparation**: then, the user simply expresses his business knowledge by selecting the relevant information for the problem at hand, and by enriching data with relevant user-defined variables.  
  
During training the dictionary, initially provided by the user, is automatically completed for describing the entire data transformation flow of the Auto-ML pipeline, from mapping available data sources to predicting the target variable. The main technical benefits include:

- **Agile model release**: a single dictionary file encodes an entire data transformation flow. Thus, updating a model simply involves replacing a file, enabling predictions to be made directly from the raw data. 

- **On-the-fly processing**: data transformation is implemented in a very efficient way, as it is processed on the fly. For example, user-defined variables and those resulting from the Auto Feature Engineering step are instantiated only when the model is used. This enables fast computations and efficient use of RAM and storage capacity.  

- **Distributed computing and Out-of-core**: the use of dictionaries enables Khiops to process large amounts of data very efficiently. [Advanced strategies][auto-adaptation] for adapting learning algorithms to available hardware resources are implemented. The initial learning task is divided into sub-tasks, either due to a lack of RAM (out-of-core processing loads sub-parts of data sequentially), or in order to distribute processing over a cluster of computers. 


[auto-adaptation]: ../learn/hardware_adaptation.md
 
## What is a Khiops dictionary ? 

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_as_a_program.webp" type="image/webp">
  <img style="width:48%;" src="/assets/images/dictionary_as_a_program.png" alt="dictionary_as_a_program" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>


!!! success "A dictionary is a program that describes and transforms data"
    Dictionaries are written using a declarative programming language dedicated to both data **definition** and **manipulation**. Thus, a dictionary includes a specification of the data itself (i.e. definition), as well as the transformations to be applied (i.e. manipulation).  


## How dictionaries are used ? 

This section illustrates how dictionaries are used throughout the Auto-ML pipeline: (i) who writes the dictionaries; (ii) what are they used for.   

### Data description and preparation 

In the standard case of machine learning, where training data is encoded in a single-table format, the dictionary file provided by the user takes its simplest form, just describing the variables with their names and types.

!!! success "Example of a simple dictionary describing a single training table"
    ```python
    Dictionary	iris
    {
        Numerical	SepalLength	;
        Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;	
    };
    ```

However, in most industrial applications more advanced dictionaries are required, as the raw data is made up of a multitude of disorganized data sources. To be read by Khiops, these sources must provide formatted data, typically csv, log or text files. At the end of this stage, the aim is to obtain structured and enriched data that can be easily understood by business units, and that carries business knowledge.       

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_data_preparation.webp" type="image/webp">
  <img style="width:70%;" src="/dictionary_data_preparation.png" alt="data preparation" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! abstract "The user write ✍️"
    The **user** write a dictionary for data preparation that consists in **describing** (i) the mapping of available data sources with tables; (ii) the selection of relevant tables and variables; (iii) the links between tables; (iv) the types of each variables.
     
    Then, the **manipulation** of data is specified, with (i) the selection of training examples (e.g. according to a time periode); and (ii) the coding user-defined variables to reflect business knowledge.
 

### Training stage 

During training, the Auto-ML pipeline is executed in two stages. First, pre-processing is performed, including both [auto feature engineering][auto_FE] and [optimal encoding][optimal_encoding]. Then, in the [parsimonious training][parcimonious_train] stage, the unvariate preprocessings are combined to obtain a multivariate predictive model.   

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

!!! abstract "Now, Khiops writes automatically ✍️"
    The dictionary provided by the user during the data preparation stage is **automatically enriched** in order to (i) compute a large number of informative aggregate variables; (ii) to define the rules used to encode each variable into intervals or groups.

**2) Parsimonious training**

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_train_2.webp" type="image/webp">
  <img style="width:70%;" src="/dictionary_train_2.png" alt="training 2/2" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! abstract "Khiops is still writing ✍️"
    Finally, this dictionary is modified (i) to select a subset of informative and independent variables; and (ii) to compute target prediction based on the encoded variables. 

### Release the model into production

At the end of training, predictions are made directly from the raw data, which facilitates model production in two respects. First, putting a new model into production consists in replacing one dictionary file with another, without changing anything in the IT project, provided raw data remain the same. Secondly, the archiving of a trained model includes the entire data transformation flow, which avoids the need to archive the program used to prepare the data, thus preventing the risk of a version change.  

<figure markdown>
<picture>
  <source srcset="/assets/images/dictionary_deploy.webp" type="image/webp">
  <img style="width:70%;" src="/dictionary_deploy.png" alt="using a model" loading="lazy"> 
</picture>
  <figcaption></figcaption>
</figure>

!!! abstract "The user and Khiops wrote together the final dictionary"
    At production time, the exploited dictionary both describes (i) all the **data-preparation** steps provided by the user, and (ii) all the **data flow processing** used by Khiops during training.  
    





