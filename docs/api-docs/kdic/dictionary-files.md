## Format of the dictionary files

### Dictionary file

A dictionary file is a text file with extension .kdic, containing the definition of one or many dictionaries.

### Dictionary

A dictionary allows to define the name and type of native variables in a data table file, as well as the constructed variables described by means of derivation rules.

```cpp
Dictionary name
{
    {Variable definition}*
};
```

A dictionary is defined by its name and by the list of its variables, and optionally meta-data and a label.

Variables within a dictionary can be organized into *variables blocks*. This advanced feature, used internally by Khiops for the management of sparse data, is detailed in section 8. Appendix: variable blocks and sparse data management.

Meta-data is a list of keys or key value pairs (*\<key\>* or *\<key=value\>* for numerical or categorical constant values). Meta-data is used internally by Khiops to store information related to dictionaries or variables (to annotate the results of analysis). It is also used to store the external format of Date, Time and Timestamp variables, in case where the default format is not used. In the following example, the three predefined meta-data keys *DateFormat*, *TimeFormat, TimestampFormat* and *TimestampTZFormat* are used to specify the input and output format of the related variables:

```bash
Date MyDate ; <DateFormat="DD/MM/YYYY">*
Time MyTime ; <TimeFormat="HH.MM">
Timestamp MyTimestamp ; <TimestampFormat="YYYY-MM-DD_HH:MM:SS">
TimestampTZ MyTimestampTZ ; <TimestampTZFormat="YYYY-MM-DD_HH:MM:SS.zzzzz">
```

Each variable is defined by its type, its name and other optional information.

```
[Unused] type name [= derivation rule]; [meta-data] [// label]
```

A variable can be ignored in the data processing (memory loading, modeling, deployment) if the keyword *Unused* is specified before the variable definition. Even though, Khiops is still aware of the variable, which allows to construct new variables derived from the ignored variable.

The types are Categorical, Numerical, Date, Time or Timestamp for native variables.

The names are case sensitive and are limited to 128 characters. In the case where they use characters other than alphanumeric characters, they must be surrounded by back-quotes. Tabulations are not allowed inside variables names (replace by blank characters). Back-quotes inside variable names must be doubled.

Derivation rules are formulas that allow to compute the value of variable from other values coming from other variables, rules, or constants.

Each line in the definition of a dictionary can be commented, using "//" as a prefix.

Some technical types are used by Khiops to specify prepocessing or modeling methods: for example Structure(DataGrid), Structure(Classifier).

Example: dictionary file Iris.kdic with a constructed variable PetalArea

```cpp
Dictionary Iris
{
    Unused Numerical SepalLength;
    Numerical SepalWidth;
    Numerical PetalLength;
    Numerical PetalWidth;
    Numerical PetalArea = Product(PetalLength, PetalWidth);
    Categorical Class; // Class variable
};
```

### ![](../../assets/images-khiops-guides/khiops/image7.png) Multi-table dictionary

Whereas most data mining tools work on instances\*variables flat tables, real data often have a structure coming from databases. Khiops allows to analyse multi-table databases, where the data come from several tables, with zero to one or zero to many relation between the tables.

To analyse multi-table databases, Khiops relies on:

- an extension of the dictionaries, to describe multi-tables schemas, (this section)

- databases that are stored in one data file per table in a multi-table schema (cf. .section 2.2. Train database),

- automatic feature construction to build a flat analysis table(cf. Section 2.3.1.4. Variable construction parameters).

In this section, we present star schema, snowflake schemas, external tables, then give a summary.

#### Star schema

For each dictionary, one or several key fields have to be specified in the first line of the dictionary definition, using parenthesis (e.g. *Dictionary Customer (id\_customer)*). In case of multiple key fields, they must be separated by commas (e.g. *Dictionary Customer (id\_country, id\_customer)*). The key fields must be chosen among the Categorical variables and must not be derived from a rule.

One of the dictionaries has to be chosen as the Root dictionary, which represents the entities to analyze, using the Root flag (e.g. *Root Dictionary Customer (id\_customer)*).

The relation between the dictionaries has to be specified by creating new Entity or Table relational variables

- e.g. in *Dictionary Customer*, an *Entity(Address) Address* variable for a 0-1 relationship between a customer and its address (where *Address* is the dictionary of the sub-entity).

- e.g. in *Dictionary Customer*, a *Table(Usage) Usages* variable for a 0-n relationship between a customer and its usages (where *Usage* is the dictionary of the sub-entity).

The keys in the dictionaries of the sub-entities must have at least the same number of fields as in the root dictionary, but these key fields do not need to have the same names.

There must be one table file per table use in the schema. All tables must be sorted by key, and as for the root table, each record must have a unique key.

![Customer3tables.emf](../../assets/images-khiops-guides/khiops/image30.emf)

Example: dictionary file Customer.kdic with a root dictionary *Customer* and a 0-1 relation with address and a 0-n relation with sales. A multi-table database related to this multi-table dictionary consists of three data table files, sorted by their key fields.

```cpp
Root Dictionary Customer(id_customer)
{
    Categorical id_customer;
    Categorical Name;
    Entity(Address) Address; // 0-1 relationship*
    Table(Usage) Usages; // 0-n relationship*
};

Dictionary Address(id_customer)
{
    Categorical id_customer;
    Numerical StreetNumber;
    Categorical StreetName;
    Categorical City;
};

Dictionary Usage(id_customer)
{
    Categorical id_customer;
    Categorical Product
    Timestamp Time;
    Numerical Duration
};
```

#### Snowflake schema

The example in the preceding section illustrates the case of a star schema, with the customer in a root table and its address and sales in secondary tables. Secondary tables can themselves be in relation to sub-entities, leading to a snowflake schema. In this case, the number of key fields must increase with the depth of the schema (but not necessarily at the last depth).

![CustomerSF4tables.emf](../../assets/images-khiops-guides/khiops/image31.emf)

#### External tables

External tables can also be used, to reuse common tables that are shared by all the analysis entities. In the following schema, the products can be referenced from the services of a customer.

![CustomerSFE5tables.emf](../../assets/images-khiops-guides/khiops/image32.emf)

Whereas the sub-entities of root entity Customer are all ***included*** in the customer ***folder*** (the address, services and usages per service belong to the folder), the products are ***referenced*** by the services.

The dictionary of an external table must be a root dictionary, with a unique key.

The related table file will be fully loaded in memory for efficient direct access, whereas the entities of each folder can be loaded one at a time, for scalability reasons.

Whereas the joins between the tables of the same folder are implicit, on the basis of the table keys, the join with an external table must be explicit in the dictionary, using a key (into brackets) from the referencing entity.

> *Dictionary Service (id\_customer, id\_product)*
> 
> *{*
> 
> *Categorical id\_customer ;*
> 
> *Categorical id\_product ;*
> 
> *Entity(Product) Product \[id\_product\] ;*
> 
> *Table(Usage) Usages ;*
> 
> *};*
> 
> *Root Dictionary Product (id\_product)*
> 
> *{*
> 
> *Categorical id\_product ;*
> 
> *Categorical Name ;*
> 
> *Numerical Price ;*
> 
> *};*

Examples of datasets with multi-table schemas and external tables, are given in the “samples” directory of the Khiops package (%PUBLIC%\\khiops\_data\\samples in windows, $HOME/khiops\_data/samples in Linux) .

#### Summary

Khiops allow to analyse multi-table databases, from standard mono-table to complex schema.

<table>
<thead>
<tr class="header">
<th><p>Mono-table</p>
<ul>
<li><p>standard representation</p></li>
</ul>
<p>Fields types</p>
<ul>
<li><p>Numerical</p></li>
<li><p>Categorical</p></li>
<li><p>Date</p></li>
<li><p>Time</p></li>
<li><p>Timestamps</p></li>
</ul></th>
<th><img src="../../assets/images-khiops-guides/khiops/image33.wmf" style="width:0.55059in;height:0.28571in" /></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Star schema</p>
<ul>
<li><p>Multi-table extension</p></li>
<li><p>Each table must have a key</p></li>
<li><p>The root table is the main entity</p></li>
</ul>
<p>Additional field types in the root table</p>
<ul>
<li><p>Entity: 0-1 relation ship</p></li>
<li><p>Table: 0-n relationship</p></li>
</ul></td>
<td><img src="../../assets/images-khiops-guides/khiops/image34.wmf" style="width:1.11309in;height:0.55357in" /></td>
</tr>
<tr class="even">
<td><p>Snowflake schema</p>
<ul>
<li><p>Extended star schema</p></li>
<li><p>Each table must have a key</p></li>
<li><p>The root table is the main entity</p></li>
</ul>
<p>Additional field types in any table of the schema</p>
<ul>
<li><p>Entity: 0-1 relation ship</p></li>
<li><p>Table: 0-n relationship</p></li>
</ul></td>
<td><img src="../../assets/images-khiops-guides/khiops/image35.wmf" style="width:1.80347in;height:1.13403in" /></td>
</tr>
<tr class="odd">
<td><p>External tables</p>
<ul>
<li><p>External tables allow to reuse common tables referenced by all entities</p></li>
<li><p>Must be root tables</p></li>
<li><p>Must be referenced explicitly, using keys from the referencing entities</p></li>
</ul></td>
<td><img src="../../assets/images-khiops-guides/khiops/image36.wmf" style="width:1.88403in;height:1.09792in" /></td>
</tr>
</tbody>
</table>

### Edition of dictionary files by means of Excel

The dictionary files, which are text files with tabulation separators, could be easily edited using Excel. Unfortunately, the use of derivation rules or categorical constants (surrounded by double quotes) is error prone in Excel (due to automatic data conversion in Excel). However, Excel can be used safely with the following process:

- Open the dictionary file using a basic text editor (for example: Notepad),

- Copy-past all or part of the defined variables to Excel,

- Edit the variables in Excel (select, modify, sort…),

- Copy-paste the edited variables back to the text editor.

Editing the variables using Excel allows to display the variables properties (Unused keyword, User type, Type, Name, Derivation rule, Comment, Level…) in Excel columns. This is then easy to perform sorts and modify the definition of variables.

### Derivation rules

The derivation rules allow to construct new variables in a dictionary. The operands in a derivation rule can be a variable (specified by its name), a constant numerical or categorical value, or the result of another derivation rule. The derivation rules can be used recursively.

A constant categorical value must be surrounded by double quotes. A double quote character inside a categorical value must be doubled. When the length of a categorical value is too important, the value can be split into sub-values, concatenated using '+' characters.

A constant numerical value can be specified using scientific notation (for example: 1.3E7). The decimal separator is the dot. The missing value is represented as \#Missing when used in a derivation rule.

There are no Date, Time Timestamp constants, but they can be produced using conversion rules (see appendix: e.g. *AsDate(“2014-01-15”, “YYYY-MM-DD”)*);

The list of available derivation rules is given in appendix.

#### Derivation rules for multi-table schemas

Derivation rules can be used to extract information from other tables in a multi-table schema. In this case, they use variables of different scopes:

- First operand of type Entity or Table, in the current dictionary scope (ex: DNA),

- Next operands, in the scope of the secondary table (ex: Pos, Char).

In the following example, the “MeanPos” and “MostFrequentChar” extract information from a DNA sequence in the secondary table. The derivation rules (TableMean and TableMode) have a first operand that is a Table variable in the scope of SpliceJunction, while their second operand is in the scope of SpliceJunctionDNA.

> *Root Dictionary SpliceJunction(SampleId)*
> 
> *{*
> 
> *Categorical SampleId;*
> 
> *Categorical Class;*
> 
> *Table(SpliceJunctionDNA) DNA;*
> 
> *Numerical MeanPos = TableMean(DNA, Pos); // Mean position in the DNA sequence*
> 
> *Categorical MostFrequentChar = TableMode(DNA, Char); // Most frequent char in the DNA sequence*
> 
> *};*
> 
> *Dictionary SpliceJunctionDNA(SampleId)*
> 
> *{*
> 
> *Categorical SampleId;*
> 
> *Numerical Pos;*
> 
> *Categorical Char;*
> 
> *};*

#### Derivation rules with multiple scope operands

For operands in the scope of a secondary table, it is possible to use variables from the scope of the current dictionary, which is in the “upper” scope of the secondary table. In this case, the scope operator “.” must be used.

In the following example, the “FrequentDNA” selects the record of the “DNA” table, where the Char variable (in secondary table) is equal to the “MostFrequentChar” variable (with the scope operator “;”, as it in the scope of the current dictionary. And the “MostFrequentCharFrequency” computes the frequency of this selected sub-table.

> *Root Dictionary SpliceJunction(SampleId)*
> 
> *{*
> 
> *Categorical SampleId;*
> 
> *Categorical Class;*
> 
> *Table(SpliceJunctionDNA) DNA;*
> 
> *Categorical MostFrequentChar = TableMode(DNA, Char);*
> 
> *Table(SpliceJunctionDNA) FrequentDNA = TableSelection(DNA, EQc(Char, .MostFrequentChar));*
> 
> *Numerical MostFrequentCharFrequency = TableCount(FrequentDNA);*
> 
> *};*

Note that the resulting “MostFrequentCharFrequency” could be computed using one single formula:

> *Numerical MostFrequentCharFrequency = TableCount(*
> 
> *TableSelection(DNA,*
> 
> *EQc(Char,*
> 
> *.TableMode(DNA, Char))));*
