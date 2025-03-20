Sparse data often appears in data mining, in the case of many missing or null values in a large instances x variables data matrix. 
This is the standard case in text mining. It also occurs in the case of a multi-table schema, when many variables are constructed 
to extract information from secondary tables. For example, in the marketing domain, you might construct features such as the number 
of items purchased by a customer, per item type, by day of the week and by time of day, which represents potentially tens of thousands of variables, 
most of which contain the value 0.

Data mining algorithms can leverage sparse data to improve their efficiency, from data management, feature construction, data preparation, 
modeling to model deployment. Khiops automatically exploits sparse data throughout the data mining process, using variable blocks within dictionaries, 
sparse data format for storing data files and specific derivation rules to efficiently exploit variable blocks.
