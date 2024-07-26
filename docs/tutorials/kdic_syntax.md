

## Libraries skl and core 

## List of table types

- Root
- Entity
- Table  

## List of variable types


## Monotable 

```python
Dictionary	iris
{
    Numerical	SepalLength	;
    Numerical	SepalWidth		;
    Numerical	PetalLength		;
    Numerical	PetalWidth		;
    Categorical	Class	;	
};
```

## Star 

```python
Root Dictionary	Customer (id_customer)
{
    Categorical id_customer;
    Categorical Name;
    Entity(Address) Address;    //0-1 relationship
    Table(Usage) Usages;    //0-n relationship	
};

Dictionary	Address (id_customer)
{   
    Categorical id_customer;
    Numerical	StreetNumber;
    Categorical	StreetName;
    Numerical	ZipCode;
    Categorical	City;	
};

Dictionary	Usage (id_customer)
{   
    Categorical id_customer;
    Categorical	Product;
    Timestamp	Time;
    Numerical	Duration;	
};

```

## Snow falke
