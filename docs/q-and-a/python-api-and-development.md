# Python API and Development

This page centralizes recurring implementation questions around the Khiops Python ecosystem.

!!! question "Have a question or request?"
    - **Ask in [GitHub Discussions](https://github.com/orgs/KhiopsML/discussions)**
    - **Report bugs or request product changes in the [Khiops repository issues](https://github.com/KhiopsML/khiops/issues)**

## Index of questions

1. [How can we build custom features by using the Khiops Python API?](#how-can-we-build-custom-features-by-using-the-khiops-python-api)
2. [Add random_state parameter](#add-random_state-parameter)

---

## How can we build custom features by using the Khiops Python API?

For example, how can we add a new feature expressed as a ratio between two other features, by using the Khiops Python API?

Custom features can be added by using the Khiops dictionary API, which is included in the Khiops Core API. For an introduction to the concept of Khiops dictionaries, we can refer to [https://khiops.org/api-docs/](https://khiops.org/api-docs/) on the official Khiops web site. For starting using and defining Khiops dictionaries, we can start from [https://khiops.org/tutorials/kdic_intro/](https://khiops.org/tutorials/kdic_intro/).

To answer to the original example question, a ratio-like feature can be defined by using the [Divide](https://khiops.org/api-docs/kdic/math-rules/#divide) rule, as in the following example, where the credit utilization rate of each customer is computed as the ratio between the account balance and the credit line, in the `CreditInformation` dictionary file:

```
Dictionary CreditInformation
{
  Categorical CustomerId;
  Categorical CreditId;
  Numerical AccountBalance;
  Numerical CreditLine;
  Numerical CreditUtilizationRate = Divide(AccountBalance, CreditLine);
};
```

Such a dictionary can be constructed via the [core API](https://khiops.org/api-docs/python-api/) of the Khiops Python library:

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

Thus, a Khiops dictionary file with the `.kdic` extension and the precise contents shown above is written on the storage to the specified path.

**Example: Aggregating the Credit Utilization Rate Across Multiple Accounts**

For multiple accounts, there are two algorithms for calculating the credit utilization rate. The first is to calculate the credit utilization rate for each account and then take the average. The second is to first aggregate the credit limits and loan balances, then divide the total loan balance by the total credit limit to obtain the overall credit utilization rate.

The solution shown above implements the first method. Consider an illustration with 5 accounts and the following data, to see how the calculation can be customized for the second method:

| Account | Credit Limit | Loan Balance |
|---|---|---|
| A1 | 100,000 | 20,000 |
| A2 | 50,000 | 45,000 |
| A3 | 80,000 | 10,000 |
| A4 | 120,000 | 0 |
| A5 | 30,000 | 5,000 |

Method 1 Results: Average of Individual Rates

Individual Calculations:

- A1: (20,000 / 100,000) × 100% = 20%
- A2: (45,000 / 50,000) × 100% = 90%
- A3: (10,000 / 80,000) × 100% = 12.5%
- A4: (0 / 120,000) × 100% = 0%
- A5: (5,000 / 30,000) × 100% ≈ 16.67%

Average Utilization Rate = (20 + 90 + 12.5 + 0 + 16.67) / 5 = 139.17 / 5 = 27.83%

Method 2 Results: Aggregate Method

Aggregate Calculations:

- Total Credit Limit = 100,000 + 50,000 + 80,000 + 120,000 + 30,000 = 380,000
- Total Loan Balance = 20,000 + 45,000 + 10,000 + 0 + 5,000 = 80,000

Final Result: Overall Utilization Rate = (80,000 / 380,000) × 100% ≈ 0.210526 × 100% = 21.05%

The second algorithm can be implemented using Khiops custom rules as follows.

These types of aggregations can be modeled, in Khiops, via a [multi-table](https://khiops.org/tutorials/kdic_multi_table/) specification of the data. Thus, data according to this example can be structured in two tables:

- table `Customer` for storing the per-customer aggregations across several accounts; it is the main table (indicated by the optional `Root` keyword);
- table `Accounts` for storing the account information.

Thus, by using the Khiops dictionary [mathematical rules](https://khiops.org/api-docs/kdic/math-rules/) and [table rules](https://khiops.org/api-docs/kdic/table-rules/), we can specify that:

- the `Account` dictionary:
    - has the customer ID `CustomerId` as key;
    - has a calculated field, `CreditUtilizationRate`, which uses the [Divide](https://khiops.org/api-docs/kdic/math-rules/#divide) and [Product](https://khiops.org/api-docs/kdic/math-rules/#product) mathematical rules to state that this field is the product between the division of `LoanBalance` by `CreditLimit`, and `100`;
- the `Customer` dictionary:
    - has the customer ID `CustomerId` as key, which acts as the join key with the `Account` dictionary;
    - has two calculated fields:
        - `CreditUtilizationRateMethodOne`, which computes the credit utilization rate according to Method 1, that is as the division between the total credit utilization rate per customer (`CreditUtilizationRate` in the `Accounts` dictionary), and the number of accounts per customer. Table rules [TableSum](https://khiops.org/api-docs/kdic/table-rules/#tablesum) and [TableCount](https://khiops.org/api-docs/kdic/table-rules/#tablecount) are used for computing the numerator and the denominator of this division, respectively;
        - `CreditUtilizationRateMethodTwo`, which computes the credit utilization rate according to Method 2, that is, as the division between the sum of load balances and the sum of credit limits, per customer, multiplied by 100; the same rules as for Method 1 are used.

The resulting Khiops dictionary (kdic) file is:

```
// Customer with its attached bank accounts
Root Dictionary Customer(CustomerId)
{
    Categorical CustomerId;
    Table(Account) accounts;
    // Compute credit utilization rate according to Method 1
    Numerical CreditUtilizationRateMethodOne = Divide(TableSum(accounts, CreditUtilizationRate), TableCount(accounts));
    // Compute credit utilization rate according to Method 2
    Numerical CreditUtilizationRateMethodTwo = Product(Divide(TableSum(accounts, LoanBalance), TableSum(accounts, CreditLimit)), 100);

};

// Bank account
Dictionary Account(CustomerId)
{
    Categorical CustomerId;
    Categorical AccountId;
    Numerical CreditLimit;
    Numerical LoanBalance;
    // Compute credit utilization rate at the account level
    Numerical CreditUtilizationRate = Product(Divide(LoanBalance, CreditLimit), 100);
};
```

These dictionaries can be constructed via the [core API](https://khiops.org/api-docs/python-api/), by extending the code shown in the previous answer according to the new dictionary definition.

This dictionary can be loaded into Khiops and used with data as follows:

- for the customers (according to the `Customer` dictionary), only the `CustomerId` field is provided as input; the remaining aggregated fields are calculated:

| CustomerId |
|---|
| C1 |
| C2 |

- for the accounts (according to the `Account` dictionary):

| CustomerId | AccountId | CreditLimit | LoanBalance |
|---|---|---|---|
| C1 | A1 | 100.000 | 20.000 |
| C1 | A2 | 50.000 | 45.000 |
| C1 | A3 | 80.000 | 10.000 |
| C1 | A4 | 120.000 | 0 |
| C1 | A5 | 30.000 | 5.000 |
| C2 | A6 | 90.000 | 20.000 |
| C2 | A7 | 150.000 | 0 |
| C2 | A8 | 10.000 | 5.000 |

The `CreditUtilizationRate` is not provided as input, because it is calculated by Khiops.

Using the Khiops dictionary for training and deploying the model on these same data, the outputs obtained contain the computed fields, for both `Customer` and `Account` tables:

- for the customers:

| CustomerId | CreditUtilizationRateMethodOne | CreditUtilizationRateMethodTwo |
|---|---|---|
| C1 | 27.83333333 | 21.05263158 |
| C2 | 24.07407407 | 10 |

We notice that for customer `C1` we obtain the expected rates for each of the two methods, as indicated in the previous comment of this Q&A.

- for the accounts:

| CustomerId | AccountId | CreditLimit | LoanBalance | CreditUtilizationRate |
|---|---|---|---|---|
| C1 | A1 | 100 | 20 | 20 |
| C1 | A2 | 50 | 45 | 90 |
| C1 | A3 | 80 | 10 | 12.5 |
| C1 | A4 | 120 | 0 | 0 |
| C1 | A5 | 30 | 5 | 16.66666667 |
| C2 | A6 | 90 | 20 | 22.22222222 |
| C2 | A7 | 150 | 0 | 0 |
| C2 | A8 | 10 | 5 | 50 |

We notice that the `CreditUtilizationRate` field is now calculated according to the specified rule.

*Source: [discussion #825](https://github.com/orgs/KhiopsML/discussions/825)*

---

## Add random_state parameter

Allow Khiops and pykhiops to produce different results by modulating the random seed of Khiops.

For example: measure the variance of the AUC with respect to the automatic generation of aggregates or even the SNB.

**Evaluating the Variance of Prediction Results**

- This is of natural interest in data mining.
- It is usually addressed using techniques such as cross-validation or bootstrapping, where the analysis method is applied on multiple samples.

**Evaluating the Variance of an Algorithm with Respect to Its Parameters**

- This process is called sensitivity analysis.
- It is particularly important for new techniques and research purposes.
- It mainly concerns user-defined technical parameters (e.g., the width or shape of a kernel) to provide recommendations for their optimal choices.
- Generally, random seeds are not considered as user parameters, but it can be interesting to study the variance of results with respect to the random seed.
    - High variance related to the random seed usually indicates instability, which is undesirable.

**Khiops Parameters**

- Khiops does not have such technical parameters
- Khiops is an AutoML solution designed to be as simple as possible to use.
- Only a minimal set of user parameters are available:
    - Problem specification: dictionary, database, target variable.
    - Business constraints:
        - Trade-off between accuracy, modeling, training, and deployment time (e.g., number of generated features, trees...).
        - Interpretability constraints (e.g., maximum number of selected variables, maximum number of part per rpeprocessed variable...).
    - Others as needed.
- Technical parameters are never exposed to the user.
    - They may be available as hidden parameters for the Khiops team, for research purposes.

**Reproducibility of Results**

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

!!! tip
    Maybe this is helpful for this problem: [samples.train_predictor_with_cross_validation](https://khiops.org/api-docs/python-api/api/samples/samples.html#samples.train_predictor_with_cross_validation)

*Source: [discussion #933](https://github.com/orgs/KhiopsML/discussions/933)*
