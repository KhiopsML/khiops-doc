# Scenario Recording and Replay

Khiops can be operated in batch mode via the command line, allowing users to launch the tool from a shell session or integrate 
it with various programming languages such as C, C++, Java, Python, and Matlab.

Key command-line features include:

- recording a session into an output scenario file,
  
- replaying a session from an input scenario file,
  
- advanced control through parameterized scenarios combined with JSON parameter files.

## Khiops Command Line Options

Usage: khiops [OPTIONS], or khiops_coclustering [OPTIONS]

Available options are:

- -e <file\>:                 	 store logs in the file

- -b:                        	 batch mode, with no GUI

- -i <file\>:                 	 replay commands stored in the file

- -j <file\>:                    json file used to set replay parameter

- -o <file\>:                	 record commands in the file

- -O <file\>:                    same as -o option, but without replay

- (-r <string\>:<string\>)...:   search and replace in the command file

- -p <file\>:                	 stores last progression messages

- -v:                        	 print version

- -s:                            print system information

- -h:                        	 print help

!!! example "Examples"

	```
	khiops -e log.txt

    khiops -o scenario.txt

    khiops -i scenario.txt -r less:more -r 70:90
	```

	In the first example all the logs are stored in the file log.txt.

	In the second example, khiops records all user interactions in the file scenario.txt.

	In the last example, khiops replays all user interactions stored in the
	file scenario.txt after having replaced 'less' by 'more' and '70' by '90'.

## Standard Use of Scenarios

Scenarios can easily be recorded and replayed using Khiops or Khiops coclustering applications.
Using the search and replace feature, they can be made more generic for seamless integration with any programming langaguage.

### Recording a Scenario

Begin by opening a Khiops shell, which can be done by selecting the `Shell Khiops` option from the `Khiops menu`, accessible via the `Start` button in Windows.

To record a scenario file using Khiops GUI: `khiops –o my_script._kh`.

This command launches the Khiops GUI, and all user interactions, such as entering data into fields or initiating actions via menus or buttons,
are recorded into the scenario file.
Each interaction is recorded using an internal tool key, the field value, and a comment prefixed by `//` that references the GUI GUI label or action associated with the interaction.


!!!	example "Example"

	For example, to train a classifier on the Iris dataset available in the sammples (see [`Khiops Guide`](../ui-docs/khiops.md)):

	- Click on the **Open** sub-menu of the **Data dictionary** menu 

	- Choose the dictionary file (extentions .kdic): `C:\Users\Public\khiops_data\samples\Iris\Iris.kdic`

	- Enter the name the dictionary in the **Analysis dictionary** field of the **Train database** pane: `Iris`

	- Enter the name of the file in the **Data table file** field of the **Train database** pane: `C:\Users\Public\khiops_data\samples\Iris\Iris.txt`  

	- Click on the **Detect file format** button for automatic format detection

	- Enter the name of the variable to predict in the **Target variable** field of the **Parameters** pane

	- Click on the **Train model** button

	- Close the tool

	![](../assets/images-khiops-guides/khiops/Khiops_TrainDatabase.png)

	You obtain the following scenario file

	```
	// -> Khiops
	ClassManagement.OpenFile       // Open...

	// -> Open
	ClassFileName C:\Users\Public\khiops_data\samples\Iris\Iris.kdic  // Dictionary file
	OK                             // Open
	// <- Open

	TrainDatabase.ClassName Iris   // Analysis dictionary
	TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key  // List item selection
	TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName 
		C:\Users\Public\khiops_data\samples\Iris\Iris.txt  // Data table file
	TrainDatabase.DatabaseSpec.Data.DatabaseFormatDetector.DetectFileFormat   // Detect file format
	AnalysisSpec.TargetAttributeName Class  // Target variable
	ComputeStats                   // Train model

	Exit                           // Close
	// <- Khiops

	// -> Khiops
	OK                             // Yes
	// <- Khiops
	```

### Replaying a Scenario

To replay a scenario file from a Khiops shell: `khiops –i my_script._kh`

Alternatively, in Windows, you can replay a scenario by right-clicking the file in `File Explorer` and choosing `Execute Khiops Script`.

Note that the same functionalities  are available for  Khiops Coclustering tools, using the `._khc` suffix instead of `._kh`.

### Managing Scenarios

You can edit a scenario using a text editor to apply it to a different dataset. 

!!!	example "Example"

	For example, you can adapt the previous scenario related to the `Iris` dataset for the `Adult` dataset,
	by replacing the related field values accordingly

	- dictionary file: `C:\Users\Public\khiops_data\samples\Adult\Adult.kdic`

	- name the dictionary: `Adult`

	- name of the file: `C:\Users\Public\khiops_data\samples\Adult\Adult.txt`  

	- name of the target variable: `class`  

	You obtain the following scenario file, which you can replay to explore the data in the Adult dataset.

	```
	// -> Khiops
	ClassManagement.OpenFile       // Open...

	// -> Open
	ClassFileName C:\Users\Public\khiops_data\samples\Adult\Adult.kdic  // Dictionary file
	OK                             // Open
	// <- Open

	TrainDatabase.ClassName Adult   // Analysis dictionary
	TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key  // List item selection
	TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName 
		C:\Users\Public\khiops_data\samples\Adult\Adult.txt  // Data table file
	TrainDatabase.DatabaseSpec.Data.DatabaseFormatDetector.DetectFileFormat   // Detect file format
	AnalysisSpec.TargetAttributeName class  // Target variable
	ComputeStats                   // Train model
	
	Exit                           // Close
	// <- Khiops

	// -> Khiops
	OK                             // Yes
	// <- Khiops
	```

You can easily make a scenario more generic by replacing specific field values with your own keywords and
using the search and replace feature (`-r`) available in the [`Khiops Command Line Options`](scenario.md#khiops-command-line-options).

!!!	example "Example"

	For example, use your keywords for the field values of interest

	- dictionary file: `__dictionaryFile__`

	- name the dictionary: `__dictionaryName__`

	- name of the data file: `__dataFile__`  

	- name of the target variable: `__targetVariable__`

	You obtain the following generic scenario file named `train_script._kh`, which you can use to train a classifier on any dataset.
	
	```
	// -> Khiops
	ClassManagement.OpenFile       // Open...

	// -> Open
	ClassFileName __dictionaryFile__  // Dictionary file
	OK                             // Open
	// <- Open

	TrainDatabase.ClassName __dictionaryName__   // Analysis dictionary
	TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key  // List item selection
	TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName __dataFile__  // Data table file
	TrainDatabase.DatabaseSpec.Data.DatabaseFormatDetector.DetectFileFormat   // Detect file format
	AnalysisSpec.TargetAttributeName __targetVariable__  // Target variable
	ComputeStats                   // Train model

	Exit                           // Close
	// <- Khiops

	// -> Khiops
	OK                             // Yes
	// <- Khiops
	```

	You can then train a classifier on the Iris and Adult datasets using the following command lines:

	- Iris dataset
	```
	khiops -i train_script._kh ^
	  -r __dictionaryFile__:C:\Users\Public\khiops_data\samples\Iris\Iris.kdic ^
	  -r __dictionaryName__:Iris ^
	  -r __dataFile__:C:\Users\Public\khiops_data\samples\Iris\Iris.txt ^
	  -r __targetVariable__:Class ^
	  -e train_log.txt
	```

	- Adult dataset
	```
	khiops -i train_script._kh ^
	  -r __dictionaryFile__:C:\Users\Public\khiops_data\samples\Adult\Adult.kdic ^
	  -r __dictionaryName__:Adult ^
	  -r __dataFile__:C:\Users\Public\khiops_data\samples\Adult\Adult.txt ^
	  -r __targetVariable__:class ^
	  -e train_log.txt
	```


!!! note

	Any keyword can be used with the search and replace option. However, it is recommended to use delimiters like `__`, 
	as shown in the previous example, to prevent ambiguities, such as confusion between `DATA` and `DATA_PATH`.

### Tips and Tricks	

- Each session of the Khiops GUI is saved automatically in a default scenario file called `scenario._kh`. 
  On Windows, this file is stored in the directory: `C:\Users\<username>\khiops_data\lastrun`.
  On Linux, it is located in: `/tmp/khiops/<username>`.

- Want to add features to your scenario but are unsure of the syntax?
  Simply click on the Khiops buttons and open the scenario file located in the lastrun directory.

- To replay scenarios silently (without a user interface), use the `-b` option together with `-i` and `-r`.

- To save the results logs in a file, use the `-e <file>` option.


### Integration with Other Programming Languages

If you need to start a Khiops process from your preferred programming language, such as C++, Java, Java script, MATLAB, R, etc., follow these steps:

- record a scenario using Khiops application,

- make the scenario more generic,

- prepare a Khiops command line with options `-i`, `-r`, `-b`, `-e`,

- execute Khiops with this command line and the generic scenario from your chosen language.

!!! example

	C++: `system(command);`

	Java: `Process process = Runtime.getRuntime().exec(command);`

	…

!!! note "Note on backwards compatibility"

	Khiops scenarios are not backwards compatible.

	In the event of a new version of Khiops:
	
	- simply re-register a scenario and make it generic,

	- reuse the same integration process by just updating the scenario files.



## Advanced Use of Scenarios

For a more sophisticated  integration, scenarios can be enhanced with basic control structures such as `if` or `loop` statements,
and can be used in conjunction with JSON parameter files.

!!! note

	Whereas the [`Standard Use of Scenarios`](scenario.md#standard-use-of-scenarios) allows a quick integration suitable for one-shot needs,
	the [`Advanced Use Of Scenarios`](scenario.md#advanced-use-of-scenarios) provides a more flexible and comprehensive solution, 
	particularly useful when dealing with a variable number of parameters, such as in multi-table settings.

### Control Structures in Scenarios

Basic control structures are introduced within scenarios to enable comprehensive management of search/replace operations.
Control structures are represented by instructions in **UPPER CASE** on dedicated lines.

#### Loop

A loop structure surrounds a block of scenario lines with:

- `LOOP <loop key>`

- `END LOOP`

All lines within this block are repeated as many times as necessary, based on the input data.

#### Conditional Test

A conditional test surrounds a block of scenario lines with:

- `IF <if key>`

- `END IF`

Lines within this block are conditionally executed depending on the test result.

### Parameterization via a JSON File

The [`Khiops Command Line Options`](scenario.md#khiops-command-line-options) `-j <file>` enables specifying 
a [`JSON`](https://www.json.org/json-en.html) parameter file alongside the `-i <file>` option related to the input scenario file.

The JSON file contains key/value pairs:

- Values of type **string**, **number** or **boolean**:

	- keys in the scenario are replaced with these values (`true` or `false` for booleans),
	
- Values of type **array**, related to a loop block (`LOOP`):

  - The array key identifies (`<loop key>`) a list of scenario lines within a loop.
	
  - The array contains JSON objects with a consistent structure, each with key/value pairs of type **string**, **number** or **boolean**.
	
  - Lines within the loop are duplicated for each object, with search/replace performed according to the current object's key/value pairs
	
- Values of type **boolean**, related to a conditional block (`IF`),

  - The boolean key identifies (`<if key>`) a list of scenario lines inside a conditional block.
	
  - The block is included or skipped based on the boolean value (`true` or `false`).

### Constraints

The `-O <file>` command line option simplifies scenario debugging.
It behaves like the `-o <file>` ption by executing all search and replace operations on the output scenario file, but without replaying the commands.
Additionally, it performs extra consistency checks between the keys in the input scenario and those in the JSON parameter file.

- Options `-r` (basic search/replace) and `-j` (json-driven search/replace) are mutually exclusive.

- Options `-o` and `-O` are mutually exclusive.

Only a subset of JSON's expressiveness is supported:

- No recursion between control structures.

- Keys must be unique within:

	- The main json object,
	
    - Each array (locally within the array),
	
    - Between array keys and their parent object key.
	
- Keys follow variable naming conventions:

    - Only alphanumeric characters,
	
    - Use camelCase format, aligned with [`JSON API Recommandations`](https://jsonapi.org/recommendations/),
	
    - Must not be substrings of other keys to prevent ambiguity during replacements.


The JSON keys must align with the scenario parameters:

- Each key in the JSON file corresponds to a parameter in the scenario, identified by the key enclosed in double underscores (__).
  For example, a JSON key `name` maps to the `__name__` parameter in the scenario file.

- Every scenario parameter should be defined in the JSON file, aand vice versa.
        
	- Exception: If a JSON key is missing or its value is `null`, the associated scenario lines will be ignored,
	  either a single line for standard search/replace operations or a block of lines in the case of loops or conditional blocks.

- Keys within an array are only valid within their respective loop context.

- Each scenario line should end with `// comment` to allow JSON string values to contain `//` substrings without issues.



!!! note

	Using the `-j` command line option with a JSON that contains only simple key/value pairs (no loop or conditional blocks)
	is equivalent to multiple `-r` operations, making it easy to switch from standard to advanced parameterization.

### Usage Example

In the following example, we exploit a scenario file named `advanced_train_script._kh` 
with a conditional block to execute the **Detect file format** action,
and a loop to specify all tables in a multi-table schema.

We then present a JSON file named `accidents.json` for the `Accidents` multi-table dataset available in the samples,
which consists of four tables organized according a [`snowflake schema`](kdic_multi_table.md#snowflake-relational-schemas).
```
Accident
|
| -- 1:n -- Vehicle
|             |
|             |-- 1:n -- User
|
| -- 1:1 -- Place
```

The classifier can then be trained using the following command line:
```
khiops -i advanced_train_script._kh -j accidents.json -e train_log.txt -b
```

A raw output scenario can be obtained using the additional `-o output_script._kh` option.


#### Input scenario file

```
// -> Khiops
ClassManagement.OpenFile       // Open...

// -> Open
ClassFileName __dictionaryFile__  // Dictionary file
OK                             // Open
// <- Open

TrainDatabase.ClassName __dictionaryName__   // Analysis dictionary

LOOP __dataTables__
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key __dataPath__ // List item selection
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName __dataFile__  // Data table file
END LOOP

IF __detectFormat__
TrainDatabase.DatabaseSpec.Data.DatabaseFormatDetector.DetectFileFormat   // Detect file format
END IF

AnalysisSpec.TargetAttributeName __targetVariable__  // Target variable
ComputeStats                   // Train model

Exit                           // Close
// <- Khiops

// -> Khiops
OK                             // Yes
// <- Khiops
```

#### Input JSON file

C:\Users\Public\khiops_data\samples\Iris\Iris.kdic

```json
{
  "dictionaryFile": "C:\\Users\\Public\\khiops_data\\samples\\Accidents\\Accidents.kdic",
  "dictionaryName": "Accident",
  "dataTables": [
    {
      "dataPath": "",
      "dataFile": "C:\\Users\\Public\\khiops_data\\samples\\Accidents\\Accidents.txt"
    },
    {
      "dataPath": "Place",
      "dataFile": "C:\\Users\\Public\\khiops_data\\samples\\Accidents\\Places.txt"
    },
    {
      "dataPath": "Vehicles",
      "dataFile": "C:\\Users\\Public\\khiops_data\\samples\\Accidents\\Vehicles.txt"
    },
    {
      "dataPath": "Vehicles/Users",
      "dataFile": "C:\\Users\\Public\\khiops_data\\samples\\Accidents\\Users.txt"
    }
  ],
  "detectFormat": true,
  "targetVariable": "Gravity"
}
```

#### Output scenario file

```
// -> Khiops
ClassManagement.OpenFile       // Open...

// -> Open
ClassFileName C:\Users\Public\khiops_data\samples\Accidents\Accidents.kdic       // Dictionary file
OK                             // Open
// <- Open

TrainDatabase.ClassName Accident         // Analysis dictionary
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key       // List item selection
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName C:\Users\Public\khiops_data\samples\Accidents\Accidents.txt  // Data table file
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key Place // List item selection
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName C:\Users\Public\khiops_data\samples\Accidents\Places.txt     // Data table file
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key Vehicles        // List item selection
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName C:\Users\Public\khiops_data\samples\Accidents\Vehicles.txt   // Data table file
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.List.Key Vehicles/Users  // List item selection
TrainDatabase.DatabaseSpec.Data.DatabaseFiles.DataTableName C:\Users\Public\khiops_data\samples\Accidents\Users.txt      // Data table file
TrainDatabase.DatabaseSpec.Data.DatabaseFormatDetector.DetectFileFormat          // Detect file format
AnalysisSpec.TargetAttributeName Gravity // Target variable
ComputeStats                   // Train model
Exit                           // Close
// <- Khiops

// -> Khiops
OK                             // Yes
// <- Khiops
```

### Handling Non-UTF8 Values in JSON Files

Khiops accepts any kind of data, including:

- arbitrary file names (e.g., on Linux, filenames are byte sequences),

- database variable names or values encoded in extended ANSI, not UTF-8.

A standard UTF-8 encoding is used for JSON parameters, per JSON specifications.  
For parameters whose values can be either UTF-8 strings or raw byte sequences, the format of JSON files is extended using a key variant
prefixed with `byte`, with the value encoded according to [Base64](https://fr.wikipedia.org/wiki/Base64) encoding.

For example, considering a specific parameter (e.g., `dataFile`):

- The scenario file remains unchanged, using `__dataFile__`.

- The JSON parameter file can contain two types of value representations:

	- A UTF-8 string: the variable name and its value are directly in plain text, without encoding.  
      Example: `"dataFile" = "/tmp/journées.txt"`.

    - A byte string: the variable name is prefixed with `byte`, with the first letter capitalized, and the value is encoded in Base64.  
      Example: `"byteDataFile" = "L3RtcC9qb3VybsOpZXMudHh0"` (where `L3RtcC9qb3VybsOpZXMudHh0` is the Base64-encoded value of `/tmp/journées.txt`).  

When writing the output scenario, Khiops looks for the key or its `byte` variant in the JSON file to 
determine whether to decode the value during search and replace operations.
