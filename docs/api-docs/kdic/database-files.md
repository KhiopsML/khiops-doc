# Format of the database files

A database file is a text file, containing one line per record. By default, the first line contains the names of the variables. 
If no header line is used, the fields in the database file must appear in the same order as the variables in the related dictionary.

The values of the variables are separated by a field separator. The field separator is tabulation by default (empty), and can be space (S), semi-colon (;), comma (,) or any character.

Fields can contain separator chars provided that they are surrounded by double-quotes:

- any field can be surrounded by double-quotes (e.g. "city" for city),

- for fields which content is surrounded by double-quotes:

	- the separator char can be used inside the field (e.g. "NY, city" for NY, city)
  
	- the double-quote can be used if it is paired (e.g. """NY"", city" for "NY", city),
  
	- the end of line character cannot be used inside a field (multiple-line fields are not allowed).

The numerical values may use the scientific notation (for example: 1.3E7). The decimal separator can be either the dot or the comma (the commas are recoded into dots). 
Missing or erroneous numerical values are replaced by a missing system value ($- \infty$, to avoid collision with any valid value).

Tabulations inside categorical values are replaced by blank characters, since they raise problem in visualisation tools that are based on text files with tabulation 
separated fields. The special char Ctrl-Z (ascii 26) is also replaced by a blank character. Space characters are discarded at the beginning and end of categorical values.

Date values are stored using the YYYY-MM-DD format, Time values using the HH:MM:SS. format and Timestamp values using the YYYY-MM-DD HH:MM:SS. format. 
Numerous other formats are available for [`Time`](time-rules.md), [`Timestamp`](timestamp-rules.md) and [`TimestampTz`](timestamp-tz-rules.md) . 
For these formats, the variable must be declared with a meta-data (with key DateFormat, TimeFormat or TimestampFormat) 
to specify the external format (see [`here`](dictionary-files.md)).

Note that Khiops also exploits an extended tabular format with sparse fields. This advanced feature, used internally by Khiops for the management of sparse data, 
is detailed [`here`](block-sparse-rules.md).

For *multi-table* databases, database files must be sorted by key for efficiency reasons. 
<!--- [](../../assets/images-khiops-guides/khiops/Multi-tablePicto.png) ---> 
