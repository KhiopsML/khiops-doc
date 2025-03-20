# Numerical precision

Numerical precision:

- in memory, the numerical values are stored on 8 bytes, with an exponent between 10<sup>-100</sup> and 10<sup>100</sup>, and a mantissa of 10 significant digits,

- risk of loss of numerical precision when using some derivation rules (for example, adding a very small value and a very large value),

- risk of loss of numerical precision during a database deployment if input values use a mantissa of more than 10 digits.

# End of line encoding

Ends of line are encoded using CR (Carriage Return) LF (Line Feed) on Windows, LF on linux. Both formats are supported.

But Mac OS Classic format (now deprecated, since Mac OS X in 2001) that encoded ends of lines using CR (without LF) is not supported.

# Character encodings

Management of categorical values:

- in memory, the categorical values are stored using null-terminated strings, which is compatible with ANSI files, UTF-8 files, but not with double-bytes character sets such as Unicode that may contain null bytes insides strings,

- categorical values are kept at most once in memory,

- for example, a variable "address" of average length 100 characters and containing 10,000 different values will requires about 1 MB RAM,

- risk of lacking from RAM in case of categorical variables containing large numbers of different values of large size (for example: managing 100,000 different values of average length 10,000 characters requires about 1 GB RAM).

Graphical Interface Issues:

- some data dependent parameters (e.g. variable names with UTF8 characters) may produce errors when modifying them with the Khiops GUI because of inconsistent encodings between Java and input data. Note that this is not a problem in batch mode.

File names issues:

- File names with non ANSI characters are not supported.

Data sets and categorical values:

- when a categorical value is read from a data set, it is trimmed and its tab characters are replaced by blanks,

- this means for example that "Mr", "<space\>Mr" or "Mr<space\>", "<space\><tab\>Mr" are treated as the same value,

- however, non-trimmed values can be created using derivation rules (ex: Concat("Mr", "<space\>"): this may be convenient for data transformation, but this results in an inconsistent behaviour in the data preparation and modelling processes, with preprocessing results based on non-trimmed values and deployment based on trimmed values

Data files and BOM:

- some tools add a BOM (byte order mark) at the beginning text files in the case of UTF8, UTF16, UTF32 encodings. BOM are encoded with special characters that are invisible but can cause problems, for example when recognizing field names in a header line. BOM are not accepted as valid formats by Khiops, which raises an error in this case.

Character encoding of JSON files:

- JSON files are used to export analysis results, in .khj files for Khiops, .khcj for Khiops coclustering; dictionary files (.kdic) can also be exported to JSON (.kdicj)

- standard-compliant JSON files require the use of UTF8 characters. However, UTF8 is incompatible with still widely used encodings such as Windows-1252 ("ANSI”) and ISO-8859-1. To address this incompatibility, Khiops produces valid UTF8 JSON files with the following rules:
  
	- The ASCII range (0 to 127) is UTF8 compatible so they are written directly
  
	- The ANSI-only range (or "extended ASCII", 128 to 255) is encoded using a slightly modified version of the [Unicode translation table for Windows-1252](https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP1252.TXT) that encodes even undefined ANSI characters. We refer to the resulting character set as ANSI-as-UTF8.
  
	- Valid UTF8 characters are written directly

- note that if your data or dictionary files have characters in the ANSI-only range but were interpreted with a code page other than Windows-1252 the resulting JSON file will not have the correct locale.

- the Khiops JSON files contain the necessary information to detect and diagnose any character encoding problem :

	- The field "khiops\_encoding" at the top level of the JSON file allows to know which character sets are present in it. The following table summarizes the field values

	<table>
	<thead>
	<tr class="header">
	<th><p>Character set present /</p>
	<p>"khiops_encoding" value</p></th>
	<th>ASCII</th>
	<th><p>ANSI-as-UTF8</p>
	<p>(ANSI origin)</p></th>
	<th><p>ANSI-as-UTF8</p>
	<p>(UTF8 origin)</p></th>
	<th><p>Other</p>
	<p>UTF8</p></th>
	</tr>
	</thead>
	<tbody>
	<tr class="odd">
	<td>ascii</td>
	<td>Yes</td>
	<td></td>
	<td></td>
	<td></td>
	</tr>
	<tr class="even">
	<td>ansi</td>
	<td>Yes</td>
	<td>Yes</td>
	<td></td>
	<td></td>
	</tr>
	<tr class="odd">
	<td>utf8</td>
	<td>Yes</td>
	<td></td>
	<td>Yes</td>
	<td>Maybe</td>
	</tr>
	<tr class="even">
	<td>mixed_ansi_utf8</td>
	<td>Yes</td>
	<td>Yes</td>
	<td></td>
	<td>Yes</td>
	</tr>
	<tr class="odd">
	<td>colliding_ansi_utf8</td>
	<td>Yes</td>
	<td>Yes</td>
	<td>Yes</td>
	<td>Maybe</td>
	</tr>
	</tbody>
	</table>

	- All cases can be unambiguously encoded back to ANSI except for the last, which is rare. In the latter case two extra fields provide additional diagnostic information:
  
		- "ansi\_chars": The list of ANSI-only characters present in the JSON file (as UTF8). They are written with Unicode escape sequences "\\uXXXX" using the aforementioned Windows-1252 to Unicode translation.
  
		- "colliding\_utf8\_chars": The list of UTF-8 characters that collide with the Unicode representation some characters in "ansi\_chars". They are written as normal UTF-8 characters. Note that this field may be absent, if no character from the ANSI-as-UTF8 set with UTF-8 origin collides with an ansi character.

# Scalability limits

Let N be the number of instances C the number of class values and K the number of variables. The RAM (in bytes) required for data analysis is about:

- Min memory = $N.(50+8.C) + K.(1000+250.C)$

- Optimal memory = $N.(50+8.C+8.K) + K.(1000+250.C)$

Thus, a database containing 100 000 instances, 1000 variables and 2 class values can be processed on a PC with 512 MB RAM. A PC with one GB RAM allows to speed up the processing, by avoiding data chunking.

Scalability tests have been performed on a PC with 2 GB RAM in the case of 2 class values, with databases containing tens of millions of records and few variables, or hundreds of thousands of records and tens of thousands of variables. Scalability tests on database files have been performed up to files with tens of GB.

Computation time for data preparation:

- $K.C.N.log(N)$

- about 5 to 10 min on a PC 2 Ghz, for a database containing 100 000 records and 1000 variables, or 1000 records and 100 000 variables.

Computation time to train the Selective Naive Bayes predictor:

- $K.N.C.log(K.N)$

- about 5 to 10 min on a PC 2 Ghz, for a database containing 100 000 records and 1000 variables, or 1000 records and 100 000 variables.

In regression analysis, the limitations are similar to those of classification analysis, with an equivalent of $C ~ \sqrt{N}$ class values during data preparation, 
and up to N class values during modeling. Thus, regression analysis may require much more memory and computation time than classification analysis. 
A potential trade-off between accuracy and computational efficiency is to preprocess the numerical target variable using an equal frequency method 
(with for example at most $\sqrt{N}$ intervals).

Limitation of database deployment:

- no known limitation: the databases are processed one record at a time.

# Temporary files

Khiops uses temporary files for various internal tasks and stores them in the environment’s temporary directory (usually ‘\\Users\\{username}\\AppData\\Local\\Temp’ on Windows and ‘/tmp’ on Linux).

Khiops prefix its temporary file names with a tilde (‘~’) and stores them in a sub-directory prefixed by ‘~Khiops’.

If Khiops exits successfully, it deletes all temporary files generated in the session. In case the application is forcibly killed or another uncontrollable event occurs (such as a power or disk failure), Khiops might not remove these files. When this happens, the following Khiops sessions will search for the ‘~~anchor~~’ file in old temporary directories, check the expiration date stored there and delete them if this date is before one day. If the undeleted files are too large and the user needs to free the space immediately, he can delete them manually.

In very rare cases, errors in the Khiops execution will corrupt the temporary files and the tool will not work properly. If this is the case, the easiest solution is to exit Khiops and restart it.

# Known problems

Memory overflow: in spite of conservative evaluation of required memory, Khiops may crash down with memory overflow. In this case, a "memory overflow" message is present in the tool log file. Asking Khiops to use less memory (see [`System parameters`](../../ui-docs/khiops/parameters.md) is likely to solve this problem.

Some file with UTF-8 encoding may cause problems in rare and unusual cases. Actually, the encoding of the characters differs between the data files and the user interface of Khiops, written in Java. In this case, use Khiops in batch mode rather than in user interface mode.

The user interface, written in Java, may crash in some rare cases (sometimes in case of Java known bugs like screen savers with some graphic cards). In this case, use Khiops in batch mode rather than in user interface mode.

Khiops can be started many times simultaneously on the same machine. However, it is recommended to use Khiops in batch mode when tens of instances of Khiops are used in the same time, to avoid potential problems caused by too many opened java virtual machines.

Under Windows, Khiops can be started using the "Execute Khiops Script” context menu, by a right-click on Khiops script file (".\_kh"). However, this does not work for UNC paths (ex: [\\\\server\\filename](file:\\\\server\\filename)), since they are not supported by Windows cmd.exe.

