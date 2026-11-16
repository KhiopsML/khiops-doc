# Python API and development

## How can you create custom features with the Khiops Python API? { #discussion-825 }

### Example: Building a ratio feature

Custom features can be added by using the Khiops dictionary API, which is included in the Khiops Core API.
For an introduction to the concept of Khiops dictionaries, we can refer to [https://khiops.org/api-docs/](https://khiops.org/api-docs/) on the official Khiops web site. For starting using and defining Khiops dictionaries, we can start from [https://khiops.org/tutorials/kdic_intro/](https://khiops.org/tutorials/kdic_intro/).

To answer to the original example question, a ratio-like feature can be defined by using the [`Divide`](https://khiops.org/api-docs/kdic/math-rules/#divide) rule, as in the following example, where the credit utilization rate of each customer is computed as the ratio between the account balance and the credit line,
in the `CreditInformation` dictionary file:

```kdic
Dictionary  CreditInformation
{
  Categorical  CustomerId    ;
  Categorical  CreditId    ;
  Numerical  AccountBalance    ;
  Numerical  CreditLine    ;
  Numerical  CreditUtilizationRate   = Divide(AccountBalance, CreditLine)  ;
};
```

Such a dictionary can be constructed via the [`core` API](https://khiops.org/api-docs/python-api/) of the Khiops Python library:

```python
# Perform the necessary imports
from khiops import core as kh

# Build empty dictionary domain object
credit_information_dict_domain = kh.DictionaryDomain()

# Build empty dictionary object; specify its name
credit_information_dict = kh.Dictionary()
credit_information_dict.name = "CreditInformation"

# Build customer ID variable; specify its name and type
customer_id = kh.Variable()
customer_id.name = "CustomerId"
customer_id.type = "Categorical"

# Build credit ID variable; specify its name and type
credit_id = kh.Variable()
credit_id.name = "CreditId"
credit_id.type = "Categorical"

# Build account balance variable; specify its name and type
account_balance = kh.Variable()
account_balance.name = "AccountBalance"
account_balance.type = "Numerical"

# Build credit line variable; specify its name and type
credit_line = kh.Variable()
credit_line.name = "CreditLine"
credit_line.type = "Numerical"

# Built credit utilization rate variable; specify its name and type
credit_utilization_rate = kh.Variable()
credit_utilization_rate.name = "CreditUtilizationRate"
credit_utilization_rate.type = "Numerical"

# Add variable construction rule
credit_utilization_rate.rule = "Divide(AccountBalance, CreditLine)"

# Add variables to the credit information dictionary
for variable in [
    customer_id, credit_id, account_balance, credit_line, credit_utilization_rate
]:
    credit_information_dict.add_variable(variable)

# Add credit information dictionary to the dictionary_domain
credit_information_dict_domain.add_dictionary(credit_information_dict)

# Write the credit information dictionary domain to a file on disk
credit_information_dict_domain.export_khiops_dictionary_file(
    "/path/to/credit_information.kdic"
)
```
Thus, a Khiops dictionary file with the `.kdic` extension and the precise contents shown above is
written on the storage to the specified path.

*Source: [discussion #825](https://github.com/orgs/KhiopsML/discussions/825)*

## Why doesn’t Khiops expose a random seed parameter? { #discussion-933 }

### Variance Analysis, Parameters and Reproducibility via Khiops

#### Evaluating the Variance of Prediction Results
- This is of natural interest in data mining.
- It is usually addressed using techniques such as cross-validation or bootstrapping, where the analysis method is applied on multiple samples.

#### Evaluating the Variance of an Algorithm with Respect to Its Parameters
- This process is called sensitivity analysis.
- It is particularly important for new techniques and research purposes.
- It mainly concerns user-defined technical parameters (e.g., the width or shape of a kernel) to provide recommendations for their optimal choices.
- Generally, random seeds are not considered as user parameters, but it can be interesting to study the variance of results with respect to the random seed.
    - High variance related to the random seed usually indicates instability, which is undesirable.

#### Khiops Parameters
- Khiops does not have such technical parameters
- Khiops is an AutoML solution designed to be as simple as possible to use.
- Only a minimal set of user parameters are available:
    - Problem specification: dictionary, database, target variable.
    - Business constraints:
    - Trade-off between accuracy, modeling, training, and deployment time (e.g., number of generated features, trees...).
    - Interpretability constraints (e.g., maximum number of selected variables, maximum number of part per preprocessed variable...).
    - Others as needed.
- Technical parameters are never exposed to the user.
    - They may be available as hidden parameters for the Khiops team, for research purposes.

#### Reproducibility of Results
- Importance:
    - For the user: ensuring that running the same workflow produces consistent results.
    - For debugging: reproducing issues reported by users.
    - For extensive non-regression testing performed by the Khiops team.
- How:
    - Fixing the random seed for each algorithm (preprocessing, feature engineering, SNB, etc.).
    - Managing seeds in parallelized algorithms to ensure consistent results regardless of the number of cores used.
    - Using stable sorting methods.
    - Fixing advanced compiler options to ensure stability across different operating systems.
    - etc.

*Source: [discussion #933](https://github.com/orgs/KhiopsML/discussions/933)*
