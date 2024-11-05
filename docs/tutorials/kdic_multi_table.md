
## Data Description 

## Table Selection 

## User-defined Relational Schema

## Advanced Example Selection 


## ------------


## List of primitives 

## Seletion or variables



## Selection of examples

```python
Dictionary	Adult
{
        Categorical		Label	;	
        Numerical		age	;	
        Categorical		workclass	;	
        Numerical		fnlwgt	;	
        Categorical		education	;	
        Numerical		education_num	;	
        Categorical		marital_status	;	
        Categorical		occupation	;	
        Categorical		relationship	;	
        Categorical		race	;	
        Categorical		sex	;	
        Numerical		capital_gain	;	
        Numerical		capital_loss	;	
        Numerical		hours_per_week	;	
        Categorical		native_country	;	
        Categorical		class	;
Unused	Numerical		SelectionSenior = GE(age, 60);
};
```

## User-defined variables


```python
Dictionary	iris
{
    Numerical	SepalLength	;
    Numerical	SepalWidth		;
    Numerical	PetalLength		;
    Numerical	PetalWidth		;
    Numerical	SepalArea = Product(SepalLength,SepalWidth);
    Categorical	Class	;	
};
```
