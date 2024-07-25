

The use of Khiops dictionaries significantly accelerates the release of Machine Learning models into production, and enables users to easily express their business knowledge. The main benefits include:

- **Meaningful data preparation**: Starting from a multitude of disorganized data sources, the user can easily structure training data into a comprehensible relational schema. The user simply expresses his business knowledge by selecting the relevant information for the problem at hand, and by enriching data with relevant user-defined variables.
  
- **End-to-end data transformation flow**: Khiops dictionaries encode the entire data transformation flow of the Auto-ML pipeline, from mapping available data sources to predicting the target variable. This makes model release into production more agile, and is also beneficial for model archiving. 

- **On-the-fly processing**: Data transformation is implemented in a very efficient way, as it is processed on the fly. For example, user-defined variables and those resulting from the Auto Feature Engineering step are instantiated only when the model is used. This enables fast computations and efficient use of RAM.  

- **Distributed computing and Out-of-core**: The use of dictionaries enables Khiops to process large amounts of data very efficiently. [Advanced strategies][auto-adaptation] for adapting learning algorithms to available hardware resources are implemented. The initial learning task is divided into sub-tasks, either due to a lack of RAM (out-of-core processing loads sub-parts of data sequentially), or in order to distribute processing over a cluster of computers. 


[auto-adaptation]: ../learn/hardware_adaptation.md
 
## What is a Khiops dictionary ? 

## How dictionary are used ? 



