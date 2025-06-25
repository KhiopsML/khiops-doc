# Table Block Rules

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
## TableBlockCountDistinct

```kdic-api-docs
Block(Numerical) TableBlockCountDistinct(Table table, Block(Categorical) valueBlock)
```
Number of distinct values per variable of a categorical block defined in the secondary Table.

## TableBlockEntropy

```kdic-api-docs
Block(Numerical) TableBlockEntropy(Table table, Block(Categorical) valueBlock)
```
Entropy of the value distribution per variable of a categorical block defined in the secondary Table.

## TableBlockMode

```kdic-api-docs
Block(Categorical) TableBlockMode(Table table, Block(Categorical) valueBlock)
```
Most frequent value per variable of a categorical block defined in the secondary Table.

## TableBlockMean

```kdic-api-docs
Block(Numerical) TableBlockMean(Table table, Block(Numerical) valueBlock)
```
Mean value per variable of a numerical block defined in the secondary Table.

## TableBlockStdDev

```kdic-api-docs
Block(Numerical) TableBlockStdDev(Table table, Block(Numerical) valueBlock)
```
Standard deviation per variable of a numerical block defined in the secondary Table.

## TableBlockMedian

```kdic-api-docs
Block(Numerical) TableBlockMedian(Table table, Block(Numerical) valueBlock)
```
Median value per variable of a numerical block defined in the secondary Table.

## TableBlockMin

```kdic-api-docs
Block(Numerical) TableBlockMin(Table table, Block(Numerical) valueBlock)
```
Min value per variable of a numerical block defined in the secondary Table.

## TableBlockMax

```kdic-api-docs
Block(Numerical) TableBlockMax(Table table, Block(Numerical) valueBlock)
```
Max value per variable of a numerical block defined in the secondary Table.

## TableBlockSum

```kdic-api-docs
Block(Numerical) TableBlockSum(Table table, Block(Numerical) valueBlock)
```
Sum of values per variable of a numerical block defined in the secondary Table.

