# Table Partition Rules

**Sparse partition of a secondary Table**

Table variables are used in the multi-table format of Khiops to specify a 0-n relationship between two entities, for example between a customer and its usages
in a secondary table.

The [`Partition`](table-partition-rules.md#partition) rule specifies how to partition a secondary table. 

The [`TablePartition`](table-partition-rules.md#tablepartition) rule 
produces a block of Table variables from a secondary table and the partition specification.

**Computing statistics from blocks of Table variables**

Blocks of Table parts can be then used to produce block of values by computing the statistics of a given secondary variable on each part defined in the block.
The sparse rules below allow to compute various statistic indicators from a block of Table parts.

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


## Partition

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


## TablePartition

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

## TablePartitionCount

```kdic-api-docs
Block(Numerical) TablePartitionCount(Block(Table) tableParts) tablePartition)
```
Number of records per part.

!!! example

	usagesCountsByServiceDuration =TablePartitionCount(usagesByServiceDuration);

## TablePartitionCountDistinct

```kdic-api-docs
Block(Numerical) TablePartitionCountDistinct(Block(Table) tableParts, Categorical value)
```
Number of distinct values per part for a given categorical variable defined in the secondary Table.

## TablePartitionEntropy

```kdic-api-docs
Block(Numerical) TablePartitionEntropy(Block(Table) tableParts, Categorical value)
```
Entropy of the distribution of the values per part for a given categorical variable defined in the secondary Table. 
For a part containing *k* distinct values with probabilities *p*<sub>1</sub>, *p*<sub>2</sub>… *p<sub>k</sub>*, the entropy is defined as 
entropy = -*p*<sub>1</sub> log(*p*<sub>1</sub>) -*p*<sub>2</sub> log(*p*<sub>2</sub>) … -*p<sub>k</sub>* log(*p<sub>k</sub>*). 
It can be seen as a measure of variance in the case of a categorical variable.

## TablePartitionMode

```kdic-api-docs
Block(Categorical) TablePartitionMode(Block(Table) tableParts, Categorical value)
```
Most frequent value per part for a given categorical variable defined in the secondary Table.

## TablePartitionModeAt

```kdic-api-docs
Block(Categorical) TablePartitionModeAt(Block(Table) tableParts, Categorical value, Numerical rank)
```
I<sup>th</sup> most frequent value per part for a given categorical variable defined in the secondary Table.

## TablePartitionMean

```kdic-api-docs
Block(Numerical) TablePartitionMean(Block(Table) tableParts, Numerical value)
```
Mean value per part for a given numerical variable defined in the secondary Table.

## TablePartitionStdDev

```kdic-api-docs
Block(Numerical) TablePartitionStdDev(Block(Table) tableParts, Numerical value)
```
Standard deviation per part for a given numerical variable defined in the secondary Table.

## TablePartitionMedian

```kdic-api-docs
Block(Numerical) TablePartitionMedian(Block(Table) tableParts, Numerical value)
```
Median value per part for a given numerical variable defined in the secondary Table.

## TablePartitionMin

```kdic-api-docs
Block(Numerical) TablePartitionMin(Block(Table) tableParts, Numerical value)
```
Min value per part for a given numerical variable defined in the secondary Table.

## TablePartitionMax

```kdic-api-docs
Block(Numerical) TablePartitionMax(Block(Table) tableParts, Numerical value)
```
Max value per part for a given numerical variable defined in the secondary Table.

## TablePartitionSum

```kdic-api-docs
Block(Numerical) TablePartitionSum(Block(Table) tableParts, Numerical value)
```
Sum of values per part for a given numerical variable defined in the secondary Table.
