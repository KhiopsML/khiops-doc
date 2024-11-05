

## Data Description 

- Context : décrire les types des variables avant de lancer l'entrainement d'un modèle.
- Habituellement : il faut charger les données en mémoire dans un Dataframe Pandas ou équivalent, puis vérifier les types.  
- Avec les dictionnaires : il n'est pas necessaire de charger les données en mémoire, le dictionnaire est lui-même un fichier qui spécifie les types. Le dictionnaire est lu par Khiops en même temps que les données d'entrainement, avec des stratégie de gestion de très gros volumes de données, incluant l'optimisation des I/O, les traitements out-of-core, et les traitement distribué.     

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

## Feature Selection 

- Context : sélectionner les variables à utiliser avant de lancer l'entrainement d'un modèle.
- Habituellement : il faut charger les données en mémoire entièrement, puis éliminer les variables non-désirées, ce qui requière plus de RAM.    
- Avec les dictionnaires : il n'est pas necessaire de charger les colonnes innutiles en mémoire. Grace au dictionnaire, seules les colonnes utiles du fichier d'entrée seront chargées en mémoire par Khiops. 

!!! success "Example of dictionary file"

    This is a fisrt simple example:
    ```python
    Dictionary	iris
    {
        Unused Numerical	SepalLength	;
        Unused Numerical	SepalWidth		;
        Numerical	PetalLength		;
        Numerical	PetalWidth		;
        Categorical	Class	;	
    };
    ```

## User-defined Feature

- Context : exprimer de la connaissance métier à travers des variables définies à la main, et calculée à partir des variables présentes dans les données d'entrée. 
- Habituellement : il faut charger les données en mémoire entièrement pour calculer les nouvelles variables définies par l'utilisateur. Le versionnage de ce nouveau jeux de données enrichi peut être très couteux, surtout si l'utilisateur fait un grand nombre d'essais / erreure pendant la phase de feature engineering.  
- Avec les dictionnaires : les variables définies par l'utilisateur sont calculées à la volée lors de la lecture du fichier de données. Le dictionnaire joue le role d'une spécification des variables à calculer, et il est beaucoup legers à stoker que les données d'entrainement enrichies.  

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

## Example Selection 




