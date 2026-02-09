# Json extraction rules

The JSON extraction rules outlined here provide a flexible framework for transforming JSON data into structured entities and tables within a target dictionary. 
These rules enable seamless integration of complex JSON objects and arrays,
supporting various Khiops variable types such as Numerical, Categorical, Date, Text, Entity or Table.
By following these guidelines, users can efficiently map JSON data to Khiops dictionaries, ensuring accurate and consistent data ingestion for analysis and processing.

## BuildEntityFromJson

```kdic-api-docs
Entity(TargetDic) BuildEntityFromJson(Text jsonValue)
```

Creation of an entity from a JSON field according to the structure defined in the target dictionary, provided that the hierarchical structure of the target dictionary, including its sub-entities and sub-tables, matches that of the JSON object field, with its nested objects and arrays.

This derivation rule is similar to `BuildTableFromJson`, but with an input JSON value of type `object` instead of `array`, and an ouput `Entity` rather than `Table`.

JSON (JavaScript Object Notation) is a lightweight data-interchange format: <https://www.json.org/json-en.html>. A JSON field contains information organized hierarchically, with nested objects and repeated values in arrays. It consists of a list of key/value pairs, where keys are strings and values can be:

- string

- number

- object: a list of key/value pairs

- array: an array of values

- true

- false

- null

The `BuildEntityFromJson` rule creates an instance of an entity based on the target dictionary, where each target variable is filled if its name matches a JSON key and the JSON value is compatible with the variable's type.

- JSON null values are ignored; the corresponding target variable remains unchanged, similar to when the JSON key is missing.

- Invalid JSON values with incompatible types are also ignored.

- When a JSON array is associated with a target Table, one instance is created for each value in the array, resulting in a table with the same number of instances as the array length. If null or invalid values are present in the JSON array, instances are still created, but only with missing values.

**Rules for populating target Khiops variables from JSON values:**

- **Numerical**

    - Default: missing

    - Filled if the json JSON values is:

        - a number

        - a string containing a number

        - true, false (filled with 1 or 0)

- **Categorical**

    - Default: empty string ""

    - Filled if the json JSON values is:

        - a string

        - a number

        - true, false

- **Date**

    - Default: missing

    - Filled if the JSON value is a string, formatted according to the target variable's format, as defined by the [`DateFormat`](../kdic/date-rules.md) meta-data or the default format.

- **Time**

    - Default: missing

    - Filled if the JSON value is a string, formatted according to the target variable's format, as defined by the [`TimeFormat`](../kdic/time-rules.md) meta-data or the default format.

- **Timestamp**

    - Default: missing

    - Filled if the JSON value is a string, formatted according to the target variable's format, as defined by the [`TimestampFormat`](../kdic/timestamp-rules.md) meta-data or the default format.

- **TimestampTZ**

    - Default: missing

    - Filled if the JSON value is a string, formatted according to the target variable's format, as defined by the [`TimestampTZFormat`](../kdic/timestamp-tz-rules.md) meta-data or the default format.

- **Text**

    - Default: empty string ""

    - Filled for any JSON value:

        - string, number, true, false (as for Categorical)

        - object (kept as is, e.g., `{"a":1,"b":2}`),

        - array (kept as is, e.g., `[1,2,3]`).

- **Entity**

    - Default: entity not created,

    - Created if the JSON value is an object, with the entity variables filled with the object's values.

- **Table**

    - Default: empty table,

    - Created if the JSON value is an array, with as many instances as there are values in the array (including nulls),

    - Each instance is populated as follows:

        - If the JSON value is an object, a target instance is created, and its variables are filled with the object's values.

        - Otherwise, the instance retains all its default values.

    - In the special case where the target dictionary contains exactly one native variable of type Numerical, Categorical, Date, Time, Timestamp, TimestampTZ or Text, a single value instance is created for each JSON value of the array.

**Additional notes**

- No target instance is created if the JON value is invalid with respect to the JSON format.

- Each target variable retains its default value if there is no matching or valid JSON value.

- Only native variables (not derived from derivation rules) can be filled with JSON values.

- The output can be a complex snowflake schema, but no keys are necessary in the target dictionaries, as the input data does not come from multiple tables requiring joins.

**Warnings are issued, mainly in the following cases:**

- JSON values with no matching target variable.

- JSON values with incompatible types.

- Invalid temporal formats for Date, Time, Timestamp, or TimestampTZ variables.

- Invalid numerical format.

As usual, any target variable can be used or not, and additional target variables can be derived from other variables.

### Example with a star schema

!!! example

    Let us consider the following target dictionary Customer, with a secondary entity contact, and two secondary tables hobbies and products.

    ```kdic-api-docs
    Dictionary CustomerJsonData
    {
      Text JsonCustomer;

      // Instance of Customer built from the JSON data
      Entity(Customer) customer = BuildEntityFromJson(JsonCustomer); 
    };
    
    Dictionary Customer
    {
      Categorical name;
      Entity(Contact) contact;
      Table(Hobby) hobbies;
      Table(Product) products;
    };
    
    Dictionary Contact
    {
      Categorical email;
      Categorical phone;
      Date birthday;
    };
    
    Dictionary Hobby
    {
      Categorical name;
    };
    
    Dictionary Product
    {
      Categorical name;
      Numerical price;
      Timestamp purchaseDate; <TimestampFormat="YYYY-MM-DDTHH:MM:SS">
    };
    ```
    
    Using the `BuildEntityFromJson` rule, a customer entity can be filled from a JSON string like:
    ```json
    {"name":"John Doe","contact":{"email":"john.doe@example.com","phone":"+1234567890","birthday":"1992-06-10"},"hobbies":[{"name":"Reading"},{"name":"Hiking"},{"name":"Cooking"}],"products":[{"name":"Laptop","price":1200,"purchaseDate":"2022-10-06T17:30:00"},{"name":"Smartphone","price":800,"purchaseDate":"2025-12-20T16:10:00"}]}
    ```

    For clarity, the JSON value is formatted below with multiple lines as follows:
    ```json
    {
      "name": "John Doe",
      "contact": {
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "birthday": "1992-06-10"
      },
      "hobbies": [
        { "name": "Reading"},
        { "name": "Hiking"},
        { "name": "Cooking"}
      ],
      "products": [
        {
          "name": "Laptop",
          "price": 1200,
          "purchaseDate": "2022-10-06T17:30:00"
        },
        {
          "name": "Smartphone",
          "price": 800,
          "purchaseDate": "2025-12-20T16:10:00"
        }
      ]
    }
    ```

    Note:

    - In this example, where the Hobby dictionary contains a single Categorical variable, the JSON field could be simplified to 
    ```json
    "hobbies":["Reading", "Hiking", "Cooking"].
    ```
    
    - The `birthday` Date variable exploits the default format: no need for a `DateFormat` meta-data. Conversely, the `purchaseDate` Timestamp variable exploits a specific format, requiring a `TimestampFormat` meta-data.

### Method for specifying target Khiops dictionaries

In the case of a complex JSON structures, specifying the target Khiops dictionaries may seem complicated. 
However, it can be simplified by following these steps:

1.  Start with an empty target dictionary

    ```kdic-api-docs
    Dictionary CustomerJsonData
    {
      Text JsonCustomer;

      // Instance of Customer built from the JSON data
      Entity(Customer) customer = BuildEntityFromJson(JsonCustomer);
    };
    
    Dictionary Customer
    {
    };
    ```

2.  Specify the target variables, using warnings about missing target variables.

    Use the `Text` type initially to identify all variables without worrying about their precise types.
    
    ```kdic-api-docs
    Dictionary CustomerJsonData
    {
      Text JsonCustomer;

      // Instance of Customer built from the JSON data
      Entity(Customer) customer = BuildEntityFromJson(JsonCustomer);
    };

    Dictionary Customer
    {
      Text name;
      Text contact;
      Text hobbies;
      Text products;
    };
    ```

3.  Assign correct types based on the JSON structure, using warnings about invalid types to finalize the specifications.

    ```kdic-api-docs
    Dictionary CustomerJsonData
    {
      Text JsonCustomer;

      // Instance of Customer built from the JSON data
      Entity(Customer) customer = BuildEntityFromJson(JsonCustomer);
    };
    
    Dictionary Customer
    {
      Categorical name;
      Entity(Contact) contact;
      Table(Hobby) hobbies;
      Table(Product) products;
    };
    
    Dictionary Contact
    {
    };
    
    Dictionary Hobby
    {
    };
    
    Dictionary Product
    {
    };
    ```

  
4.  Repeat these steps iteratively until the entire Khiops dictionaries are fully specified, as shown in first star schema example.

### Extracting specific JSON values

If you want to extract only certain fields from JSON data, such as the customer's name, email, and phone, you can focus on the relevant parts of the target dictionaries.
To avoid warnings about missing variables, declare unused variables and assign them the `Text` type:

```kdic-api-docs
Dictionary CustomerJsonData
{
  Text JsonCustomer;

  // Instance of Customer built from the JSON data
  Entity(Customer) customer = BuildEntityFromJson(JsonCustomer);
};

Dictionary Customer
{
  Categorical name;
  Entity(Contact) contact;

  // Unused variables to prevent warnings
  Unused Text hobbies;
  Unused Text products;
};

Dictionary Contact
{
  Categorical email;
  Categorical phone;

  // Unused variable
  Unused Text birthday;
};
```

### Handling JSON array of values

JSON arrays containing objects naturally fit into Khiops Table variables, with each object used to fill an instance according to its Khiops dictionary.

For JSON arrays containing non-object values (e.g., numbers, strings), it is still possible to fill a Table variable if the Khiops dictionary contains exactly one native variable.

Examples of such usage are demonstrated with the `BuildTableFromJson` rule, including arrays of numbers or arrays of arrays of numbers.


## BuildTableFromJson

```kdic-api-docs
Table(TargetDic) BuildTableFromJson(Text jsonValue)
```

Creation of a table from a JSON field according to the structure defined in the target dictionary, provided that the hierarchical structure of the target dictionary, including its sub-entities and sub-tables, matches that of the JSON array values, with their nested objects and arrays.

This derivation rule is similar to `BuildEntityFromJson`, with an input JSON value of type `array` instead of `object`, and an ouput `Table` rather than `Entity`.

### Example with a simple table

!!! example

    Let us consider the following dictionary Customer, with a secondary table products built from a json field

    ```kdic-api-docs
    Dictionary Customer
    {
      Categorical name;
      Text JsonProducts;

      // Table of products built from the JSON data
      Table(Product) products = BuildTableFromJson(JsonProducts);
    };
    
    Dictionary Product
    {
      Categorical name;
      Numerical price;
      Timestamp purchaseDate; <TimestampFormat="YYYY-MM-DDTHH:MM:SS">
    };
    ```
    
    Using the `BuildTableFromJson` rule, the table of products can be filled from a JSON string like:
    ```json
    [{"name":"Laptop","price":1200,"purchaseDate":"2022-10-06T17:30:00"},{"name":"Smartphone","price":800,"purchaseDate":"2025-12-20T16:10:00"}]
    ```

    For clarity, the JSON value is formatted below with multiple lines as follows:
    ```json
    [
      {
          "name": "Laptop",
          "price": 1200,
          "purchaseDate":"2022-10-06T17:30:00"
      },
      {
          "name": "Smartphone",
          "price": 800,
          "purchaseDate":"2025-12-20T16:10:00"
      }
    ]
    ```

### Handling JSON array of numbers

For a JSON array of numbers, it is still possible to fill a Table variable, provided that the Khiops dictionary contains exactly one native Numerical variable.

!!! example

    Let us consider the following dictionary Movie, with a secondary table notes built from a json field

    ```kdic-api-docs
    Dictionary Movie
    {
      Categorical title;
      Text JsonNotes;

      // Table of notes built from the JSON data
      Table(Note) notes = BuildTableFromJson(JsonNotes);
    };
    
    Dictionary Note
    {
      Numerical note;
    };
    ```

    Using the BuildTableFromJson rule, the table of notes can be filled from a JSON string like
    `[3, 4, 3, 1, 4, 5, 3]`

    Each number in the JSON array creates an instance of `Note` and sets the value of its single Numerical variable. 
    The variable's name is not exploited in this process.

    *Null values*
    With null values, as shown below, the first two created notes will retain missing values:
    `[null, null, 3, 1, 4, 5, 3]`

    *Invalid values*
    In the following pathological example, an instance of `Note` is created for each value in the array, resulting in a Table of the same size as the array:
    `[3, 1, "4", 5, 3, true, false, {}, [], "NaN", null, null]`

    - The first part `[3, 1, "4", 5, 3, true, false]` includes numbers, strings containing valid numerical data, and boolean values (true -\>     1, false -\> 0), which are used to set Numerical values.

    - The second part `[{}, [], "NaN", null, null]` contains invalid JSON values, and all related notes will retain missing values.

### Handling JSON arrays of arrays of numbers

In the example above, a Table with exactly one Numerical variable is used as a target dictionary for a JSON array of numbers. This approach can also be applied to other Khiops types such as Categorical, Date, Time, Timestamp, TimestampTZ, or Text, in the case of a JSON array of values with compatible types.

It is also possible to handle a JSON array of arrays of numbers (or other JSON types), provided that the Khiops dictionary contains exactly one native Table variable, which itself is related to a Khiops dictionary containing exactly one Numerical variable.

!!! example

    Let us consider the following dictionary Movie, with a secondary table notesHistory built from a JSON field

    ```kdic-api-docs
    Dictionary Movie
    {
      Categorical title;
      Text JsonNotes;

      // Table of notes' history built from the JSON data
      Table(NotesHistory) notesHistory = BuildTableFromJson(JsonNotes);
    };
    
    Dictionary NotesHistory
    {
      Table(Note) notes; // Each instance corresponds to one array of notes
    };
    
    Dictionary Note
    {
      Numerical note; // Single note value
    };
    ```

    Using the BuildTableFromJson rule, the table of notes series can be filled from the values of a json text field containing the value:
    `[[3, 4], [3, 4, 3, 1, 4, 5, 3], [5, 5, 4, 3]]`

    This will create three instances of NoteSeries, each filled with the corresponding array:

    - The first instance is filled with `[3, 4]`

    - The second with `[3, 4, 3, 1, 4, 5, 3]`

    - The third with `[5, 5, 4, 3]`

### Handling string lists of values

Sometimes datasets include fields with lists of values in textual format.

You can use regex to convert these strings into JSON arrays, then apply `BuildTableFromJson`.

!!! example

    Consider the Food dictionary, with a secondary ingredients table built from a Text variable containing the list of ingredients.

    ```kdic-api-docs
    // Food products, with their list of ingredients
    Dictionary Food
    {
      Categorical product_name;
      Categorical brand;
      Text ingredients_text;

      // Transformation of a list of values into a JSON array
      // Example:
      //     Text value: "butter, floor, sugar, eggs, sea salt."
      //     JSON array: ["butter", "floor", "sugar", "eggs", "sea salt"]
      // A regex is used to match each ingredient
      // - (\w[ \w]*)
      //   - a word, optionnaly followed by a series of word with blannk separator
      //   - the recognized pattern, designated as $1, is replaced by "$1" (between double-quotes)
      // - [ \.]*
      //   - the other blank or dot characters are ignored
      // The result is then surrounded between brackets using concatanation
      Text	ingredients_json = TextConcat("[", TextRegexReplaceAll(ingredients_text, 1, "(\w[ \w]*)[ \.]*", """$1"""), "]");
    
      // Transform JSON data into a table of ingredients
      Table(Ingredient) ingredients = BuildTableFromJson(ingredients_json);
    };
    
    Dictionary Ingredient
    {
      Categorical ingredient;
    };
    ```

    Using preprocessing, the following textual value
    ```plaintext
    "organic hazelnuts, organic cashews, organic walnuts almonds, organic sunflower oil, sea salt."
    ```
    is transformed into a JSON array of strings:
    ```json
    ["organic hazelnuts", "organic cashews", "organic walnuts almonds", "organic sunflower oil", "sea salt"]
    ```

    Then, using the `BuildTableFromJson` rule, a table of ingredients is obtained:

    - organic hazelnuts

    - organic cashews

    - organic walnuts almonds

    - organic sunflower oil

    - sea salt
