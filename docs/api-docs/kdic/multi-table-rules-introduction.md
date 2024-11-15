# Multi-Table Rules Overview

The multi-table rules allow to extract values from entities in 0-1 relationship (`Entity`) or 0-n
relationship (`Table`) with their owner.

Below you find dictionaries describing a multi-table schema The main object is a `Customer` which
can have at most one `Address` and several `Sales` entries. This example is used to illustrate the
multi-table rules in this section, with variables added in the root dictionary to extract
information from the address and sales.

```kdic
Root Dictionary Customer (customer_id)
{
  Categorical customer_id;
  Numerical age;
  Categorical sex;
  Entity(Address) customerAddress; // 0-1 relationship
  Table(Sale) sales;               // 0-n relationship
};

Dictionary Address (customer_id)
{
  Categorical customer_id;
  Categorical street;
  Categorical city;
  Categorical zipcode;
  Categorical State;
};

Dictionary Sale (customer_id)
{
  Categorical customer_id;
  Categorical product;
  Numerical cost;
  Date purchaseDate;
};
```
