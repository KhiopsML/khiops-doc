# Variable block derivation rules

## Basic variable block rules

The following variable block rules allow to copy a block of variable within a dictionary (like Copy and CopyC), 
or to obtain a copy of a block of variable defined in an Entity variable (like GetValue and GeValueC).

<!--- TODO la syntaxe kdic-api-docs ne permet de highlighter les RDD : CopyBlock, GetBlock, GetBlockC et les RDD de calculs de statistiques a partir de bloc --->

## CopyBlock

```kdic-api-docs
Block(Numerical) CopyBlock(Block(Numerical) valueBlock)
```
Copy of a block of numerical variables.

```kdic-api-docs
Block(Numerical) CopyBlock(Block(Categorical) valueBlock)
```
Copy of a block of categorical variables.

<!--- TODO la syntaxe kdic ne permet pas de highlighter le mot-cle VarKey ou le nom d'un bloc de variables --->

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


## GetBlock

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

## Sparse partition of a secondary Table

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

## Computing statistics from blocks of Table variables

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

## Computing statistics from blocks of values in secondary tables

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

