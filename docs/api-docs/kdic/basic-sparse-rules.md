# Basic Sparse Rules

The following variable block rules allow to copy a block of variables within a dictionary (like Copy and CopyC), 
or to obtain a copy of a block of variables defined in an Entity variable (like GetValue and GeValueC).

## CopyBlock

```kdic-api-docs
Block(Numerical) CopyBlock(Block(Numerical) valueBlock)
```
Copy of a block of numerical variables.

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

## CopyBlockC

```kdic-api-docs
Block(Numerical) CopyBlockC(Block(Categorical) valueBlock)
```
Copy of a block of categorical variables.


## GetBlock

```kdic-api-docs
Block(Numerical) GetBlock(Block(numerical) valueBlock)
```
Access to a block of numerical variables of an entity.

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

## GetBlockC

```kdic-api-docs
Block(Categorical) GetBlockC(Block(Categorical) valueBlock)
```
Access to a block of categorical variables of an entity.

