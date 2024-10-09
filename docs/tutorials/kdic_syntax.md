

## Libraries skl and core 

Expliquer qu'il y a deux librairies qui correspondent à des usages différents.  

**skl**

La librairie *skl* gère elle-même la création de dictionnaire, dans le but de correspondre parfaitement aux habitudes des utilisateurs de la communauté python. Mais cette librairie compporte des limitation car elle cache le nouveau concept que sont les dictionnaire à l'utilisateur. En particulier, les tables sont forcément des Dataframe Pandas déjà chargées en mémoire, le schéma multi-table et forcément de type flocon, et les tables sont considérée comme étant déjà préparées. 

**core**

La librairie *core* expose le nouveau concept des dictionnaires à l'utilisateur, dans le but de dépasser les limitations de skl mentionnées précédement. Pour permettre un apprentissage progressif des dictionaires, il existe deux niveaux de syntaxe. Le niveau *simplifié* et un sous-ensemble du niveau *complet* et la librairy *core* prend en charge ces deux niveaux de syntaxe. 

La suite de cette section est dédiée à un apprentissage progressif des dictionnaires khiops et à leur utilisation grâce à la librairy *core*


!!! success "Example of dictionary file"

    This is a fisrt simple example:
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


!!! example "Example of Python code to generate the same dictionary"

    ```python
    # Imports
    import os
    from khiops import core as kh

    # Set the file paths
    data_table_path = os.path.join(kh.get_samples_dir(), "Adult", "Adult.txt")
    dictionary_name = "AutoAdult"
    dictionary_file_path = os.path.join(
        "kh_samples", "build_dictionary_from_data_table", "AutoAdult.kdic"
    )   

    # Create the dictionary from the data table
    kh.build_dictionary_from_data_table(
        data_table_path, dictionary_name, dictionary_file_path
    )
    ```

!!! example "Proposition de Marc"

    ```python
    X = {
          "tables": {
              "": ("Accident", accidents_df,  ["AccidentId"]),
              "Vehicles": ("Vehicle", vehicles_df, ["AccidentId", "VehicleId"]),
              "Vehicles/Users": ("User", users_df, ["AccidentId", "VehicleId"]),
              "Place": ("Place", places_df, ["AccidentId"], True),
          }
      }
    ```


!!! example "Interprétation Alexis"

    ```python
    X = {
          "tables(mot-clé-fixé)": {
              "(la table principale correspond à l'origine relative des datapath)": ("Accident(nom d'un type)", accidents_df(un dataframe, p-e subtituable par un chemin de fichier),  ["AccidentId"](clée)),
              "Vehicles": ("Vehicle", vehicles_df, ["AccidentId", "VehicleId"]),
              "Vehicles/Users": ("User", users_df, ["AccidentId", "VehicleId"]),
              "Place": ("Place", places_df, ["AccidentId"], True(paramètre optionnel indiquant un lien 1:1)),
          }
      }
    ```  
    
!!! example "Proposition Alexis : plus éloigné de la syntaxe des dico mais plus typé ?"

    ```python
    X = {
            ".": {"type":"Accident", "data_source":accidents_df,  "keys":["AccidentId"]},
            "./Vehicles": {"type":"Vehicle", "data_source":vehicles_df, "keys":["AccidentId", "VehicleId"]},
            "./Vehicles/Users": {"type":"User", "data_source":users_df, "keys":["AccidentId", "VehicleId"]},
            "./Place": {"type":"Place", "data_source":places_df, "keys":["AccidentId"], "one_to_one_cardinality":True},
      }
    ```
   
 


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

**(TODO : donner l'exemple d'une ligne python core pour utiliser ce dictionnaire)**

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
