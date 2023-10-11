# Quickstart Guide

Khiops is a user friendly python library providing a unique [Auto-ML pipeline][what_makes_khiops_different]. Khiops offers significant practical advantages, based on an original formalism: 

- Advanced Automation
- Model Interpretability
- Outstanding Scalability

To find out more, read the page ["What makes Khiops different"][what_makes_khiops_different].

[what_makes_khiops_different]: /learn/understand

## Auto-ML as simple as a regular classifier 

The Khiops Auto-ML pipe automates supervised Machine Learning, which is used to classify input examples into predefined groups, each identified by a label. Common applications include predicting customer chrun (Yes or No), the severity of a failure (Minor, Major, Critical) etc. 

Featuring [unique learning algorithms][original_formalism], Khiops automates many steps seamlessly for the user. For example, there's no longer any need to prepare training data, as [missing values, labeling noise, outliers and unbalanced classes][no_data_preparation] are handled for you. [Encoding categorical variables][encoding] is also no longer a problem. 

Ultimately, all you need is to use the standard `sklearn` syntax, and Khiops takes care of handling poor-quality raw data, producing competitive, robust and interpretable models.  


The following is a minimal code sample, and more detailed [tutorials][tuto] are available.

[original_formalism]: /learn/modl
[no_data_preparation]: /advanced/Notebooks/No_data_Cleaning
[encoding]: /advanced/Notebooks/Optimal_Encoding
[tuto]: https://khiops.tech.orange/html/pykhiops-doc/tutorials/index.html


### 🔧 Setup


```python
# Simple installation using conda.
#!conda install -c khiops khiops
```


```python
# Import of the used packages.

from khiops.sklearn import KhiopsClassifier
from sklearn.model_selection import train_test_split
```

### 📊 Load sample dataset


```python
# Loading and reading the data file into a Pandas DataFrame.
url = "https://raw.githubusercontent.com/KhiopsML/khiops-samples/1686433ec63549a741cec49604d7004bec6e1eeb/Adult/Adult.txt"
df = pd.read_csv(url, delimiter='\t',index_col="Label")
```


```python
# Drop the "class" column to create the feature set (X).
X = df.drop("class", axis=1)
```


```python
# Extract the "class" column to create the target labels (y).
y = df["class"].map({'less': 0, 'more': 1})
```


```python
# Random split
X_train, X_test, y_train, y_test = train_test_split(X, y)
```

### 🚀 Just fit it


```python
# Classifier declaration and pipeline training.
clf = KhiopsClassifier()
clf.fit(X_train, y_train)
```

### 🔮 Predict 


```python
# Test set prediction.
pred = clf.predict(X_test, y_test)
```

## Auto Feature Engineering as simple as writting a dictionnary 

[Feature Engineering][Auto_feature_engineering] aimes to build a training set from multi-table data, by summarizing the useful information from the secondary tables. For example, let's consider multi-table data where the root table describes the customers of a telecom operator (with one record per customer) and the secondary tables each describe call details, services used, contracts (with a varying number of records per customer). In this case, the *``call rate to foreign countries''* could be a useful aggregate for predicting customer churn.

[Auto_feature_engineering]: /learn/autofeature_engineering

In practice, Feature Engineering is an extremely time-consuming manual task which is not efficient and risks over-fitting (i.e. when using over-complex aggregates). Just feed multi-table data into the Khiops Auto-ML pipeline to trigger an ultra-efficient [Auto Feature Engineering algorithm][Auto_feature_engineering]. All you need to do is describe the structure of the input multi-table data with a dictionary.

### 🖋️ Simply describe your multi-table data

The following only shows the `syntax` to be used when describing multi-table data. For a running code sample, please refer to the [dedicated page][full_pipeline].
Here we continue with the previous example, where the multi-table data describes the customers of a telecom operator and where the goal is to predict the chrun:

[full_pipeline]: /advanced/Notebooks/Use_in_any_ML_pipeline

<img src="/assets/images/simple_multi_table_data.png" style="width:400px;"/>

Khiops provides a simple language for describing multi-table data as a dictionary ([a running sample is available][MT_tutorial]). Here's an example: 

[MT_tutorial]: /advanced/Notebooks/Use_in_any_ML_pipeline/


```python
X_train = {
    "main_table": "Customer",
    "tables": {
        "Customer": (customer_main_df, "CustomerId"),
        "Call": (call_df, ["CustomerId", "CallId"]),
        "Service": (service_df, ["CustomerId", "ServiceId"]),
        "Contrat": (contrat_df, ["CustomerId", "ContratId"]),
    },
    "relations": [
        ("Customer", "Call"),
        ("Customer", "Service"),
        ("Customer", "Contrat"),
    ],
}
```

This dictionary includes three attributes: 

- `main_table` indicating the name of the main table,
- `tables` describing all tables, 
- `relations` describing the links between tables. 

`main table` is itself a dictionary, composed of one record per table. For each record, the *key* corresponds to the table name and the *value* is a tuple associating a Pandas Dataframe and a list of keys (first the main key, then the secondary keys). And `relations` is a tuple list indicating the links between tables.

### 🚀 Just fit it ... as usual

Once you've described the multi-table input data, no further effort is required.


```python
# Classifier declaration and full pipeline training.
clf = KhiopsClassifier()
clf.fit(X_train, y_train)
```

## Embedded visualization in Jupyter <small>  🚧 Beta 🚧 </small> 

In the beta version, the interactive visualization widget is not yet integrated into Jupyter Notebook. It will shows the features obtained by the Auto Feature Engineering algorithm, the encoding of variables, the selection of variables and their importance for predictions. 

But, you can open the visualization report using the standalone application what is available on several Operating Systems. More details on this visualization tool can be found on the [dedicated page][visu]. 

[visu]: /setup/visualization

To generate the report, you need to specify the `output_dir` parameter when call KhiopsClassifer(): 

```python
# Classifier declaration with a specifed output directory
clf = KhiopsClassifier(output_dir="User/Documents/test_khiops")
clf.fit(X_train, y_train)
```

<!---  
```python
# import of the vizualisation package 
import pkvisualization

# call of the visualization tool
with open('AllReports.khj', 'r') as file:

    data = file.read()

pkvisualization.visualize(data)
```

<img src="/assets/images/visu_in_jupyter.png"/>

-->

Open the `AllReports.khj` file on the standalone app:

<img style="width: -webkit-fill-available;" src="/assets/images/Visualization Adult Modeling.png" ;></img>

