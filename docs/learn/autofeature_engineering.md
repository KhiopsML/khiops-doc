

# Auto Feature Engineering

Auto Feature Engineering corresponds to the first **(A)** step of the Auto-ML pipeline implemented by Khiops. It is an optional pre-processing step to handle multi-table input data. Feature engineering is usually performed manually by data scientists, and is a time-consuming and risky task that can lead to overfitting. Khiops is able to automatically extract a large amount of aggregates from the secondary tables which are constructed and selected to avoid overfitting. These aggregates are all informative for the learning task at hand.

<picture>
  <source srcset="/assets/images/auto-ml-pipeline-A.webp" type="image/webp">
  <img style="max-width:800px;width: -webkit-fill-available;" src="/assets/images/auto-ml-pipeline-A.png" alt="auto-ml-pipeline"> 
</picture>

In the rest of the pipeline, the aggregates are recoded in [step (B)][preprocessing], as well as the native variables. Then the encoding models (discretization and univariate grouping) are combined in [step (C)][learning_models] in order to learn a parsimonious predictive model, by selecting relatively few variables.   

!!! example "Purpose"
    This section presents the key ideas of Auto Feature Engineering. For an easier understanding,  it is highly recommended to first read the following sections: (i) [An original formalism][a_unique_formalism], (ii) [Optimal Encoding][preprocessing]. 

[preprocessing]: preprocessing.md
[learning_models]: learning_models.md
[a_unique_formalism]: modl.md

## Definition 

The Auto Feature Engineering task, also known as [propositionalization:octicons-link-external-16:][propositionalization]{:target="_blank"}, consists in *"flattening"* multi-table data by summarizing the useful information contained in the secondary tables, through new columns inserted in the main table.

[propositionalization]: https://link.springer.com/chapter/10.1007/978-3-662-04599-2_11

<picture>
  <img style="max-width:960px;width: -webkit-fill-available;" src="/assets/images/multi-table.gif" alt="multi-table"> 
</picture>

**Input:**

Multi-table data consists of: (i) a root table, where each row represents a training example, (ii) and several secondary tables that potentially contain several records for each example. For example, the customers of a telecommunications company can be described by a root table that contains native variables (name, first name, address, age etc.) and several secondary tables containing detailed information about each customer (contracts, communication details, use of services such as VOD etc). Notice that the target variable is contained in the root table. In our example, this target variable could describe whether a customer is churner or not.

**Output:** 

The purpose of Auto Feature Engineering is to enrich the root table with informative aggregates, which are useful to predict the target variable. These aggregates are computed from the secondary tables. For example, the call rate to a foreign country could be a useful aggregate to predict customer churn. As a result, each row of the enriched root table describes a training example. This table can therefore be used by any learning algorithm.

!!! success "Key idea #1"
    Auto Feature Engineering is a **supervised learning task**  aiming at finding the most useful aggregates to predict the target variable. 


## Model Parameters

As before, the first modeling step is to define the family of models $\mathcal{H}$ which contains all the learnable hypotheses $h \in \mathcal{H}$. In the case of Auto Feature Engineering, this family is an extension of the [optimal encoding][preprocessing] models which perform two tasks: (i) choosing the variable to be encoded, which can either be a native variable or an aggregate generated from the secondary tables; (ii) encoding this variable by a discretization model or a grouping model depending on its type.  

Khiops uses a language similar to SQL to build aggregates. Formally, it is a collection of functions which can be [composed:octicons-link-external-16:][composition]{:target="_blank"} with each other an unlimited number of times, provided that the operand and return types of each function are consistent. Here is the list of functions used:    

[composition]: https://en.wikipedia.org/wiki/Function_composition

| Name        | Return type | Operands    | Description    |
| ----------- | ----------- | ----------- | -------------- |
| $Count$       | Numerical   | Table       | Number of records in a table |
| $CountDistinct$ | Numerical   | Table, Categorical  | Number of distinct values |
| $Mode$ | Categorical | Table, Categorical  | Most frequent value |
| $Mean$ | Numerical   | Table, Numerical  | Mean value |
| $StdDev$ | Numerical   | Table, Numerical  | Standard deviation |
| $Median$ | Numerical   | Table, Numerical  | Median value |
| $Min$ | Numerical   | Table, Numerical  | Min value |
| $Max$ | Numerical   | Table, Numerical  | Max value |
| $Sum$ | Numerical   | Table, Numerical  | Sum of values |
| $Selection$ | Table   | Table, (Cat, Num)  | Selection from a table given a selection criterion |
| $YearDay$ | Numerical   | Date | Day in year |
| $WeekDay$ | Numerical   | Date | Day in week |
| $DecimalTime$ | Numerical   | Time | Decimal hour in day |


In the remainder of this section, we consider a very simple example of multi-table data describing the customers of a company:

<picture>
  <source srcset="/assets/images/multi-table-data-simple-example.webp" type="image/webp">
  <img style="max-width:385px;width: -webkit-fill-available;" src="/assets/images/multi-table-data-simple-example.png" alt="auto-ml-pipeline" loading="lazy"> 
</picture>


The root table contains three columns: (i) the name of the client which is a native categorical variable, (ii) the age of the client which is a native numeric variable, (iii) and the client's identifier which serves as the join key. This key is not an explanatory variable used by the model; it simply identifies the rows of the secondary table corresponding to each client. This multi-table data contains a single secondary table describing the usages of the customers. This table consists of three columns: (i) the join key, (ii) the name of the product used, (iii) and the date of its use.

Here are some examples of aggregates that can be generated from this multi-table data:

1. $Mode$(Usages, Product)
2. $Max$(Usages, $YearDay$(useDate))
3. $Count$($Selection$(Usages, $YearDay$(useDate) in [1;90] and Product="VOD"))$

**Interpretation:**

1. The first aggregate corresponds to the most frequently used product for each customer,
2. The second aggregate combines two functions and represents the day of the year of the last usage, 
3. The third aggregate is more complex: it corresponds to the number of VOD uses during the first quarter.  

Similarly, the aggregates generated by Khiops are named by their formula and can be interpreted by the user.

!!! success "Key idea #2"
    The **choice of the functions** that compose an aggregate and the **order** in which they are combined are **additional parameters** which enrich the discretization and grouping models.  


As shown in the previous examples, the generated aggregates can be more or less complex, i.e. be composed of a varying number of functions. As the number of compositions is not limited, the aggregates can be arbitrarily complex, which poses a risk of overfitting. This risk is intrinsic to feature engineering, even when it is done manually by data scientists and business experts. For example, to predict customer churn, the following aggregate is certainly too complex to generalize its good performance on test data:

 - *"the number of calls that a customer makes to Spain, on Friday nights between 10:31 and 10:38, having used the VOD service in the previous 40 minutes"*.

!!! success "Key idea #3"
    The **cardinality** of the family of models $\mathcal{H}$ is not bounded, and can potentially be **infinite**. There is therefore a risk of **overfitting** and the complexity of the generated aggregates must be regularized.

## Optimization Criterion 

[Information theory:octicons-link-external-16:][information_theory]{:target="_blank"} provides the same interpretation for both optimization criteria previously described for [discretization][discretization] and [grouping][grouping] models. Indeed, these two criteria can be rewritten as follows:

[information_theory]: https://en.wikipedia.org/wiki/Information_theory
[discretization]: preprocessing.md#discretization
[grouping]: preprocessing.md#grouping

$$-\log(P(h).P(d|h)) = \underbrace{L(h)}_{\textbf{Prior}} 
+ \underbrace{L(d_y | h, d_x)}_{\textbf{Likelihood}} $$

where the **prior** term $L(h)$ refers to the *coding length* of the model, i.e. the number of bits needed to describe the model parameters. And the **likelihood** term $L(d_y | h, d_x)$ is the coding length of the target variable of the training examples $d_y = \{y_i\}_{i \in [1,n]}$, knowing the model $h$ and the explanatory variables of the entire training set $d_x = \{x_i\}_{i \in [1,n]}$. In other words, the encoding model (discretization or grouping) is considered as a compression of the information provided by the target variable of the training set.

In the case of Auto Feature Engineering, the complexity of the aggregates is taken into account in the prior distribution, with a new term $L(h_a)$, such as:

$$-\log(P(h).P(d|h)) = \underbrace{ {\color{red} L(h_a)} + L(h_e)}_{\textbf{Prior}} 
+ \underbrace{L(d_y | h_a, h_e, d_x)}_{\textbf{Likelihood}} $$

This term represents a *construction cost* that penalizes complex aggregates, in order to prevent overfitting. Notice that the model $h$ is sliced in two, with $h_a$ representing the constructed aggregate and $h_e$ being the associated encoding model. The construction cost $L(h_a)$ is defined recursively, following a hierarchical and uniform prior distribution:

$$ {\color{red} L(h_a)} = \underbrace{\vphantom{\frac{1}{\binom{N+I-1}{I-1}}} \log(K+1)}_{\substack{\textbf{level 1:} \\ \vphantom{a} \\ \textrm{choice to generate} \\ \textrm{an aggregate, or not.}}} 
+ \underbrace{\vphantom{\frac{1}{\binom{N+I-1}{I-1}}} \log(R)}_{\substack{\textbf{level 2:} \\ \vphantom{a} \\ \textrm{choice of function $\mathcal{R}$} \\ \textrm{among $R$.}}} 
+ \underbrace{\sum \limits_{op \in \mathcal{R}} {\color{red} L(h_a)}}_{\substack{\textbf{level 3:} \\ \vphantom{a} \\ \textrm{choice of each operand} \\ \textrm{of the function $\mathcal{R}$.}}} $$

The construction of an aggregate is made according to the following successive choices:

- **level 1**: generating an aggregate in addition to the $K$ native variables of the root table is considered as an additional choice, so its probability is $\frac{1}{K+1}$;
- **level 2**: the choice of the function is random, the probability of using a particular rule $\mathcal{R}$ among $R$ is thus of $\frac{1}{R}$;
- **level 3**: each operand of the selected function must be defined, they can be either a variable or the result of another function ...

Notice that $L(h_a) = \log(K)$ if a native variable is selected instead of generating an aggregate. 


!!! success "Key idea #4"
    The **prior** distribution of aggregates has a particular form which **prevents overfitting**, i.e. it is recursive, hierarchical and uniform. Indeed, there are as many recursions in the prior as there are composed functions, which penalizes complex aggregates.  For a complex aggregate to be selected, the additional construction cost in the prior must be compensated by the likelihood, which measures how informative an aggregate is in predicting the target variable.



## Sampling Algorithm

Two different algorithms are successively executed to implement Auto Feature Engineering: 

1. **A sampling algorithm** which randomly generates aggregates from the prior distribution described above;
2. **An optimization algorithm** which trains the encoding models (discretization or grouping) for each candidate aggregate, and selects only informative ones. 

This section describes only **(1)** the sampling algorithm, as **(2)** the optimization algorithms for discretization and grouping models are described in the [previous section][preprocessing].

!!! example "Algorithmic Challenge"
    - How to design an efficient sampling algorithm?
    - How to randomly draw aggregates from a family $\mathcal{H}$ of **infinite size**, while the hardware resources (RAM and CPU) are **limited**? 
  

To answer this algorithmic challenge, several heuristics are used:

1. The set of aggregates can be represented in a compact way as a **tree**, where the branches factorize the successive choices defining the aggregates (i.e. choice of functions to compose, choice of operands). Although compact, this tree has a potentially **infinite depth** since the number of function compositions is not bounded. 
   
2. Due to limited hardware resources, this tree can only be **explored partially**. The trick is to use a **finite number of tokens** that move through the tree and which are distributed on the branches according to the a priori distribution. The tree is thus partially built in RAM, considering only the branches in which tokens circulate.   

<video autoplay loop muted playsinline style="max-width:1280px;width: -webkit-fill-available;">
  <source src="/assets/images/algo-autofeature.mp4" type="video/mp4">
  <source src="/assets/images/algo-autofeature.gif" type="image/gif" media="(not type: video/mp4)">
</video>


The animation above shows the sampling algorithm in a very simple case, where the aggregate construction language is limited to three functions (Mode,Min,Max), and where the multi-table data considered is the same as in the previous example. Here is a description of the successive steps:

- Among the $100$ considered tokens, $34$ correspond to the choice to generate an aggregate in addition to the two native variables of the root table.  
- These $34$ tokens are uniformly distributed over the $3$ branches corresponding to the choice of the function to use.
- Then, there is only one possible choice of the 1st operand of these functions, which is the unique secondary table "Usages" of the multi-table data. 
- Finally, the last step shows that some branches end (e.g. the function Mode necessarily takes as 2nd operand the categorical variable "Product") and other branches continue to grow through the composition of functions (e.g. the function Min is composed with the function YearDay). 


The user specifies a number of candidate aggregates one wants to generate, and the algorithm is repeated several times by increasing the number of tokens, until the wanted number of distinct aggregates is generated. For more details on this sampling algorithm, the interested reader can refer to the scientific [publications][publications].

[publications]: ../references.md#publications

## Technical benefits 

!!! tip "Use in any Machine Learning pipeline "
    Only part of the Khiops Auto ML pipeline can be reused. In particular, the Auto Feature Engineering step can be integrated into any Machine Learning pipeline. This saves a lot of time in data science projects by automatically generating a large number of informative aggregates. Then, any Machine Learning model can be trained from the root table enriched by the aggregates.  

    [:material-test-tube: Experiment on Google Collab][no-data-cleaning-notebook]

[no-data-cleaning-notebook]: https://colab.research.google.com 

!!! tip "Improve business knowledge "
    The aggregates produced by Khiops are labeled with their mathematical formula, which allows us to interpret them a posteriori. In practice, the analysis of the most informative aggregates allows us to better understand the data and to easily identify the useful information for the learning task at hand.

    [:material-test-tube: Experiment on Google Collab][no-data-cleaning-notebook]

[no-data-cleaning-notebook]: https://colab.research.google.com 



## One more thing ...

<span style="color:red">**TODO : faire une section courte sur les arbres**</span> 
