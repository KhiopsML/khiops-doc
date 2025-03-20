# Variable blocks and sparse data management

Sparse data often appears in data mining, in the case of many missing or null values in a large instances x variables data matrix. 
This is the standard case in text mining. It also occurs in the case of a multi-table schema, when many variables are constructed 
to extract information from secondary tables. For example, in the marketing domain, you might construct features such as the number 
of items purchased by a customer, per item type, by day of the week and by time of day, which represents potentially tens of thousands of variables, 
most of which contain the value 0.

Data mining algorithms can leverage sparse data to improve their efficiency, from data management, feature construction, data preparation, 
modeling to model deployment. Khiops automatically exploits sparse data throughout the data mining process, using variable blocks within dictionaries, 
sparse data format for storing data files and specific derivation rules to efficiently exploit variable blocks.

## Dictionaries and blocks of variables

The aim of Khiops dictionaries is to specify the variables, mainly with their type, name and derivations rules (see [`Dictionary`](dictionary-files.md)). 
Variables within a dictionary can be organized in variable blocks.

A variable block is defined as following:

- A variable block is a group of variables delimited by { and } in a dictionary,

- All variables in a block must have the same type: Numerical, Categorical or Table,

- A variable block has a name, that is an identifier among all the variables and variable blocks within its dictionary,

- A variable block can be computed from a block derivation rule, but variables within a block cannot be individually computed with their own derivation rule,

- Each variable within a variable block has “VarKey”, defined using meta-data :
  
	- it is an identifier of the variable locally to its block
  
	- it can be either an integer, starting from 1, or an alpha-numerical value
	
	- VarKeys are no necessary contiguous nor ordered

Dictionaries can contain zero to many variables blocks. All dictionary variables can be used exactly the same way throughout the data mining process, regardless of whether they belong to a variable block or not:

- Unused if it must be ignored during data analysis,

- chosen to be the target variable, or the selection variable,

- exploited as an input of a derivation rule.

!!! example 

	One variable block with numerical VarKeys

	```kdic
	Dictionary Document
	{
	Categorical DocId;
	Categorical Label;
	{
		Numerical archive; <VarKey=1>
		Numerical name; <VarKey=2>
		...
		Numerical etrbom; <VarKey=61188>
	} Words;
	};
	```

	One variable block with categorical VarKeys

	```kdic
	Dictionary Document
	{
		Categorical DocId ;
		Categorical Label ;
		{
		Numerical archive ; <VarKey=”archive”>
		Numerical name ; <VarKey=”name”>
		…
		Numerical etrbom ; <VarKey=”etrbom”\
		} Words ; 
	};
	```


### Variable blocks and derivation rules

A variable block can be computed from a derivation rule.

The derivation rule must then be able to generate a set of (VarKey, value) pairs. 
Each variable of the block is initialized with the value corresponding to its VarKey, so that the number of variables having an actual value can be much
smaller than the number of variables of the block. We then obtain a block of values than may be sparse.

Variables in a block can be set as Unused or removed from a block, which is equivalent. In both cases, the values will not be stored without error, 
even if they are available as output of the derivation rule.

A variable block can be used as input of a derivation rule, provided that it is fully declared in the dictionary with all its detailed specification, 
including all it VarKeys.

## Data files with sparse data format

Khiops exploits temporary data files during the data mining process, for example when data does not fit in RAM or to efficiently handle parallel processing. 
In the case of variable blocks, Khiops exploits a proprietary sparse data format to exploit the potential sparsity of variable blocks.

As a reminder, in the standard case, Khiops exploits a tabular format, with or without a header line and using a field separator. 
Fields can contain the separator character provided that they are surrounded by double-quotes.

This is extended to the sparse format by considering each numerical or categorical variable block as a sparse field. 
The name of the variable block is used in the header line, and for each record, all sparse values in the same block are stored in the same field as a list
of key-value pairs. Sparse fields are managed as following:

- list of pairs ‘*VarKey:value’* separated by the blank character,

- special cases:
  
	- *Varkey* : for a numerical variable with missing value or a categorical variable with empty value
  
	- *VarKey* : for a numerical variable with value 1 or a categorical variable with value “1”

- constraints on VarKeys within a sparse field :
	
	- must be unique within the field
	
	- must be sorted in the case of a numerical VarKey
	
	- value associated to VarKeys that do not exist in the dictionary are ignored without error message,

- VarKeys are stored :
  
	- as is if they are alpha-numerical
  
	- between simple quotes otherwise
	
- values are stored : 
  
	- as is if they are alpha-numerical
	
	- between simple quotes otherwise

!!! example

	Numerical sparse fields:

		- with numerical VarKeys

		8:4965 1123:350 3069:6795 3972:7531 4100:7603

		1:0 2:3.7 3:5.2

		- with categorical VarKeys

		mon:1 nom:1.0 est:1 personne:1

		mon nom est personne

		'aujourdh''hui' il:1 fait 'très': beau

	Categorical sparse fields:

		- with numerical VarKeys

		1:bleu 2:blanc 3:rouge

		- with categorical VarKeys

		un:bleu deux:blanc trois:rouge

		10:rouge 20:bleu trente:'vert pommes' 40:rose


!!! example 

	Sparse files with two fields, one is a categorical variable named Class and the other is a numerical variable block named Words, which 
	contains counts per word, with one sparse variable per word declared in the dictionary:

	- with numerical VarKeys and a default value (1) per sparse variable :

	| Class   |  Words                                                                                               |
	| --------- | ------------------------------------------------------------------------------------------------------ |
	| 0         | 191 367 614 634 711 1202 1220 1311 1472 1730 2281 2572 2602 2611 2824 2855 2940 3149 3313 3560 3568 …  |
	| 0         | 118 307 367 478 505 512 807 878 939 1024 1095 1836 1915 1961 2261 2474 2521 2633 2673 2969 3143 3193 … |
	| 0         | 10 184 284 297 320 375 445 588 658 1108 1411 1471 1684 1787 1878 1889 1958 1986 2133 2208 2432 2460 …  |
	| 1         | 87 149 433 704 711 892 988 1056 1070 1234 1246 1289 1642 1669 1861 1924 1956 2081 2150 2909 3038 307 … |
	| 1         | 84 118 279 316 435 505 584 629 849 1029 1082 1176 1324 1327 1472 1504 1849 2004 2005 2240 2519 2568 …  |

	- with numerical VarKeys :

	| Class | Words                                                                                              |
	| --------- | ------------------------------------------------------------------------------------------------------ |
	| atheism   | 3:1 10:1 12:8 17:1 23:8 27:1 29:6 30:7 33:10 42:12 48:2 51:2 52:3 60:4 67:3 73:2 81:6 83:1 99:1 100: … |
	| atheism   | 23:2 27:1 29:3 30:1 33:5 42:3 48:1 51:1 60:7 71:1 72:1 81:1 122:4 131:1 144:2 291:1 297:1 335:1 368: … |
	| atheism   | 10:1 12:8 17:2 23:9 27:8 28:1 29:15 30:8 33:10 42:5 44:4 46:1 48:2 49:1 51:3 52:2 60:6 67:1 72:1 81: … |
	| graphics  | 297:1 27:2 29:3 30:3 33:1 80:2 131:1 233:1 235:2 304:1 355:1 365:1 474:1 475:1 770:2 775:2 778:2 813 … |
	| politics  | 29:4 30:1 33:1 35:1 51:1 143:1 245:1 388:1 466:1 467:1 511:1 747:1 748:1 770:1 775:2 778:1 850:1 23: … |
	| politics  | 9:2 12:3 23:1 27:1 29:3 30:2 33:4 42:1 48:1 51:1 54:1 60:1 72:1 73:1 76:1 81:3 122:2 137:1 144:1 1 …   |
	| politics  | 8:1 12:3 23:5 29:3 30:1 33:6 42:6 44:1 51:1 52:3 60:4 72:2 81:1 100:2 104:1 122:3 142:1 144:2 179: …   |

	- with categorical VarKeys :

	| Class | Words                                                                                              |
	| --------- | ------------------------------------------------------------------------------------------------------ |
	| atheism   | archive:4 name:2 atheism:10 resources:4 alt:2 last:1 modified:1 december:1 version:3 atheist:9 addre … |
	| atheism   | of:7 other:1 are:7 the:19 in:7 to:13 it:3 like:1 on:2 but:7 is:16 people:2 get:1 com:1 so:2 one:4 su … |
	| atheism   | of:6 and:7 are:2 the:13 in:5 us:1 to:4 it:6 on:1 but:2 is:3 people:2 can:2 for:3 one:1 or:1 society: … |
	| graphics  | of:1 and:2 the:9 in:1 to:3 like:1 on:1 but:1 with:2 is:5 people:1 for:7 who:1 one:1 address:1 black: … |
	| politics  | of:5 freedom:1 from:1 the:8 in:2 us:1 to:5 it:1 but:1 with:2 is:1 can:1 com:1 go:1 so:1 one:1 east:1 … |
	| politics  | of:11 from:4 and:21 are:5 the:38 in:10 to:17 it:17 like:1 on:2 their:1 but:2 with:4 is:18 north:1 pe … |
	| politics  | of:5 and:3 are:3 the:5 in:4 us:1 to:3 it:2 on:1 is:2 ca:2 people:2 for:3 who:1 by:3 see:3 they:2 tha … |

### Khiops versus SVMLight sparse format

The SVMLight tool exploits a sparse format that mainly consists of the target value followed by a list of key-value pairs with integer keys:

<target\> <feature\>:<value\> <feature\>:<value\> ... <feature\>:<value\> \# <info\>

Khiops can handle any number of fields, either for dense variables or for blocks of sparse variables. In the case of one dense field followed by one block of sparse variables with numerical VarKeys, Khiops format is very close from SVMLight format:

<target\> SEP <feature\>:<value\> <feature\>:<value\> ... <feature\>:<value\>

The main difference is that there must be a separator character (SEP) between the two fields. This separator character can be a tab or ‘;’ for example. If the separator character is the space character, the second field that contains the block of sparse variables must be surrounded by double-quotes, as it contains the space character.

The other difference is that the dictionary must explicitly specify all the variables in the block, with their names and VarKeys.

## Variable block derivation rules

### Basic variable block rules

The following variable block rules allow to copy a block of variable within a dictionary (like Copy and CopyC), 
or to obtain a copy of a block of variable defined in an Entity variable (like GetValue and GeValueC).

### CopyBlock

```kdic-api-docs
Block(Numerical) CopyBlock(Block(Numerical) valueBlock)
```
Copy of a block of numerical variables.

```kdic-api-docs
Block(Numerical) CopyBlock(Block(Categorical) valueBlock)
```
Copy of a block of categorical variables.

!!! example 

	In this  example, the block of variables named *Items* is copied to a new block named *Words*. 
	Each variable has a unique name within the whole dictionary, and a unique VarKey within its block. 
	The variables of the input block are copied to those of the output block having the same VarKey.

	```kdic
	Dictionary Document
	{
		Categorical DocId;
		Categorical Label;
		{
		Numerical item1; <VarKey=1>
		Numerical item2; <VarKey=2>
		…
		} Items ;
		{
		Numerical archive; <VarKey=1>
		Numerical name; <VarKey=2>
		…
		} Words = CopyBlock(Items) ;
	};
	```


### GetBlock

```kdic-api-docs
Block(Numerical) GetBlock(Block(numerical) valueBlock)
```
Access to a block of numerical variables of an entity.

```kdic-api-docs
Block(Categorical) GetBlockC(Block(Categorical) valueBlock)
```
Access to a block of categorical variables of an entity.

In the following example, the block of variables named *Items* in the Entity(Document) variable *CurriculumVitae* is accessed in a new block named *CVWords*. 
In the main entity.

!!! example

	```kdic 
	Root Dictionary Applicant(id_applicant)
	{
		Categorical id_applicant ;
		Categorical Name ;
		Entity(Document) CurriculumVitae ;
		Entity(Document) MotivationLetter ;
		{
		Numerical archive ; <VarKey=1>
		Numerical name ; <VarKey=2>
		…
		} CVWords = GetBlock(CurriculumVitae, items) ;
	};
	```

	```kdic 
	Dictionary Document(id_applicant)
	{
		Categorical id_applicant ;
		{
		Numerical item1 ; <VarKey=1>
		Numerical item2 ; <VarKey=2>
		…
		} Items ;
	};
	```

### Sparse partition of a secondary Table

Table variables are used in the multi-table format of Khiops to specify a 0-n relationship between two entities, for example between a customer and its usages
in a secondary table.

The following rules allow to partition a secondary table into a set of part, using a Partition rule that specifies how to partition the secondary table 
and a TablePartitionRule that produces a block of Table variables from a secondary table and the partition specification.


```kdic-api-docs
Structure(Partition) Partition(Structure(\<partition\>) partition1, …)
```
Builds a partition structure, which is a cross-product of univariate partitions. 
The parameters are univariate partitions, chosen among IntervalBounds, ValueGroups, ValueSetC or ValueSet.

!!! example

	The following bivariate partition exploits a ValueSetC rule to partition categorical values into three groups and a IntervalBounds rule 
	to partition numerical rules into two intervals

	```kdic-api-docs
	Structure(Partition) partitionServiceDuration = Partition(ValueSetC("Mobile", "Tel", " * "), IntervalBounds(5.5));
	```

	The resulting bivariate partition consists of 6 parts, with index from 1 to 6.

	|              | Mobile | Tel |  *  |
	| ------------ | ------ | --- | --- |
	| \]-inf;5.5\] | 1      | 2   | 3   |
	| \]5.5;+inf\[ | 4      | 5   | 6   |


```kdic-api-docs
Block(Table) TablePartition(Table table, Structure(Partition) partition)
```
Builds a block of Table parts from a secondary Table and the specification of a partition. 
Note that the block variable is potentially sparse, as only the non-empty parts are managed.

!!! example

	In the following dictionary, the *usagesByServiceDuration* block of variables is computed from a TablePartition rule 
	that divides the secondary table *Usages* into a set of sub-parts according to the partition specified in the variable *partitionServiceDuration*. 
	Among the 6 potential parts, 4 are described in the block of variables and related to their part index using their VarKey. 
	The other 2 parts are simply ignored in the dictionary.

	```kdic
	Root Dictionary Customer(id_customer) 
	{
		Categorical	id_customer ;
		Categorical Name;
		Table(Usage) Usages;
		Structure(Partition) partitionServiceDuration = Partition(ValueSetC("Mobile", "Tel", " * "), IntervalBounds(5.5));
		{                 
		Table(Usage)	MobileSmallDuration; <VarKey=1>
		Table(Usage)	TelSmallDuration; <VarKey=2>
		Table(Usage)	MobileLargeDuration; <VarKey=4>
		Table(Usage)    TelLargeDuration; <VarKey=5>
		}               usagesByServiceDuration = TablePartition(Usages, partitionServiceDuration, Service, Duration);
	};
	```

	```kdic
	Dictionary	Usage(id_customer)
	{
		Categorical	id_customer;
		Categorical Service;
		Numerical Duration;
		Numerical Price;
	};
	```

### Computing statistics from blocks of Table variables

Blocks of Table parts can be used to produce block of values by computing the statistics of a given secondary variable on each part defined in the block.

!!! example

	The TablePartitionMean rule computes the mean value of the secondary variable *Price* for each Table part in the block of Table variables *usagesByServiceDuration*.

	```kdic
	Root Dictionary Customer(id_customer)
	{
		Categorical	id_customer;
		Categorical Name;
		Table(Usage)	Usages;
		Structure(Partition)	partitionServiceDuration = Partition(ValueSetC("Mobile", "Tel", " * "), IntervalBounds(5.5));
		{
		Table(Usage)	MobileSmallDuration;	<VarKey=1>
		Table(Usage)	TelSmallDuration; <VarKey=2>
		Table(Usage)    MobileLargeDuration; <VarKey=4>
		Table(Usage)	TelLargeDuration; <VarKey=5>
		}               usagesByServiceDuration = TablePartition(Usages, partitionServiceDuration, Service, Duration);
		{
		Numerical	MobileSmallDurationMeanPrice; <VarKey=1>
		Numerical   TelSmallDurationMeanPrice; <VarKey=2>
		Numerical   MobileLargeDurationMeanPrice; <VarKey=4>
		Numerical   TelLargeDurationMeanPrice; <VarKey=5>
		}			usagesMeanPriceByServiceDuration = TablePartitionMean(usagesByServiceDuration, Price);
	};
	```

	```kdic
	Dictionary	Usage(id_customer)
	{
		Categorical id_customer;
		Categorical Service;
		Numerical Duration;
		Numerical Price;
	};
	```

The following sparse rules allow to compute various statistic indicators from a block of Table parts.

```kdic-api-docs
Block(Numerical) TablePartitionCount(Block(Table) tableParts) tablePartition)
```
Number of records per part.

!!! example

	usagesCountsByServiceDuration =TablePartitionCount(usagesByServiceDuration);

```kdic-api-docs
Block(Numerical) TablePartitionCountDistinct(Block(Table) tableParts, Categorical value)
```
Number of distinct values per part for a given categorical variable defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TablePartitionEntropy(Block(Table) tableParts, Categorical value)
```
Entropy of the distribution of the values per part for a given categorical variable defined in the secondary Table. 
For a part containing *k* distinct values with probabilities *p*<sub>1</sub>, *p*<sub>2</sub>… *p<sub>k</sub>*, the entropy is defined as 
entropy = -*p*<sub>1</sub> log(*p*<sub>1</sub>) -*p*<sub>2</sub> log(*p*<sub>2</sub>) … -*p<sub>k</sub>* log(*p<sub>k</sub>*). 
It can be seen as a measure of variance in the case of a categorical variable.

```kdic-api-docs
Block(Categorical) TablePartitionMode(Block(Table) tableParts, Categorical value)
```
Most frequent value per part for a given categorical variable defined in the secondary Table.

```kdic-api-docs
Block(Categorical) TablePartitionModeAt(Block(Table) tableParts, Categorical value, Numerical rank)
```
I<sup>th</sup> most frequent value per part for a given categorical variable defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TablePartitionMean(Block(Table) tableParts, Numerical value)
```
Mean value per part for a given numerical variable defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TablePartitionStdDev(Block(Table) tableParts, Numerical value)
```
Standard deviation per part for a given numerical variable defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TablePartitionMedian(Block(Table) tableParts, Numerical value)
```
Median value per part for a given numerical variable defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TablePartitionMin(Block(Table) tableParts, Numerical value)
```
Min value per part for a given numerical variable defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TablePartitionMax(Block(Table) tableParts, Numerical value)
```
Max value per part for a given numerical variable defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TablePartitionSum(Block(Table) tableParts, Numerical value)
```
Sum of values per part for a given numerical variable defined in the secondary Table.

### Computing statistics from blocks of values in secondary tables

A block of values in a secondary table corresponds to a list of secondary variables managed in the same block. 
Table rules such as TableMean, TableMode, TableStandard deviation are then extended to the case of a secondary block of variables to compute a block of values 
for all variables in the secondary block.

!!! example 
	
	The TableBlockSum rule computes the sum of the values of each variable in the block of variables defined in the secondary table.

	```kdic
	Root Dictionary Applicant(id_applicant)
	{
		Categorical id_applicant ;
		Categorical Name ;
		Entity(Document) CurriculumVitae ;
		Entity(Document) MotivationLetter ;
		Table(Document) RecommandationLetters ;
		{
		Numerical archive ; <VarKey=1>
		Numerical name ; <VarKey=2>
		…
		} RecommandationWords = TableBlockSum(RecommandationLetters, items) ;=
	};
	```

	```kdic
	Dictionary Document(id_applicant)
	{
		Categorical id\_ applicant;
		{
		Numerical item1 ; <VarKey=1>
		Numerical item2 ;<VarKey=2>
		…
		} Items ;
	};
	```

```kdic-api-docs
Block(Numerical) TableBlockCountDistinct(Table table, Block(Categorical) valueBlock)
```
Number of distinct values per variable of a categorical block defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TableBlockEntropy(Table table, Block(Categorical) valueBlock)
```
Entropy of the value distribution per variable of a categorical block defined in the secondary Table.

```kdic-api-docs
Block(Categorical) TableBlockMode(Table table, Block(Categorical) valueBlock)
```
Most frequent value per variable of a categorical block defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TableBlockMean(Table table, Block(Numerical) valueBlock)
```
Mean value per variable of a numerical block defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TableBlockStdDev(Table table, Block(Numerical) valueBlock)
```
Standard deviation per variable of a numerical block defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TableBlockMedian(Table table, Block(Numerical) valueBlock)
```
Median value per variable of a numerical block defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TableBlockMin(Table table, Block(Numerical) valueBlock)
```
Min value per variable of a numerical block defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TableBlockMax(Table table, Block(Numerical) valueBlock)
```
Max value per variable of a numerical block defined in the secondary Table.

```kdic-api-docs
Block(Numerical) TableBlockSum(Table table, Block(Numerical) valueBlock)
```
Sum of values per variable of a numerical block defined in the secondary Table.

