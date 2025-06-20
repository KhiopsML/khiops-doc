# Data files with sparse data format

Khiops exploits temporary data files during the data mining process, for example when data does not fit in RAM or to efficiently handle parallel processing. 
In the case of variable blocks, Khiops exploits a proprietary sparse data format to exploit the potential sparsity of variable blocks.

As a reminder, in the standard case, Khiops exploits a tabular format, with or without a header line and using a field separator. 
Fields can contain the separator character provided that they are surrounded by double-quotes.

This is extended to the sparse format by considering each numerical or categorical variable block as a sparse field. 
The name of the variable block is used in the header line, and for each record, all sparse values in the same block are stored in the same field as a list
of key-value pairs. Sparse fields are managed as following:

- list of pairs ‘*VarKey:value’* separated by the blank character,

- special cases:
  
	- *Varkey* : for a numerical variable with missing value or a categorical variable with empty value
  
	- *VarKey* : for a numerical variable with value 1 or a categorical variable with value "1"

- constraints on VarKeys within a sparse field :
	
	- must be unique within the field
	
	- must be sorted in the case of a numerical VarKey
	
	- value associated to VarKeys that do not exist in the dictionary are ignored without error message,

- VarKeys are stored :
  
	- as is if they are alpha-numerical
  
	- between simple quotes otherwise
	
- values are stored : 
  
	- as is if they are alpha-numerical
	
	- between simple quotes otherwise

!!! example

	Numerical sparse fields:

		- with numerical VarKeys

		8:4965 1123:350 3069:6795 3972:7531 4100:7603

		1:0 2:3.7 3:5.2

		- with categorical VarKeys

		mon:1 nom:1.0 est:1 personne:1

		mon nom est personne

		'aujourdh''hui' il:1 fait 'très': beau

	Categorical sparse fields:

		- with numerical VarKeys

		1:bleu 2:blanc 3:rouge

		- with categorical VarKeys

		un:bleu deux:blanc trois:rouge

		10:rouge 20:bleu trente:'vert pommes' 40:rose


!!! example 

	Sparse files with two fields, one is a categorical variable named Class and the other is a numerical variable block named Words, which 
	contains counts per word, with one sparse variable per word declared in the dictionary:

	- with numerical VarKeys and a default value (1) per sparse variable :

	| Class   |  Words                                                                                               |
	| --------- | ------------------------------------------------------------------------------------------------------ |
	| 0         | 191 367 614 634 711 1202 1220 1311 1472 1730 2281 2572 2602 2611 2824 2855 2940 3149 3313 3560 3568 …  |
	| 0         | 118 307 367 478 505 512 807 878 939 1024 1095 1836 1915 1961 2261 2474 2521 2633 2673 2969 3143 3193 … |
	| 0         | 10 184 284 297 320 375 445 588 658 1108 1411 1471 1684 1787 1878 1889 1958 1986 2133 2208 2432 2460 …  |
	| 1         | 87 149 433 704 711 892 988 1056 1070 1234 1246 1289 1642 1669 1861 1924 1956 2081 2150 2909 3038 307 … |
	| 1         | 84 118 279 316 435 505 584 629 849 1029 1082 1176 1324 1327 1472 1504 1849 2004 2005 2240 2519 2568 …  |

	- with numerical VarKeys :

	| Class | Words                                                                                              |
	| --------- | ------------------------------------------------------------------------------------------------------ |
	| atheism   | 3:1 10:1 12:8 17:1 23:8 27:1 29:6 30:7 33:10 42:12 48:2 51:2 52:3 60:4 67:3 73:2 81:6 83:1 99:1 100: … |
	| atheism   | 23:2 27:1 29:3 30:1 33:5 42:3 48:1 51:1 60:7 71:1 72:1 81:1 122:4 131:1 144:2 291:1 297:1 335:1 368: … |
	| atheism   | 10:1 12:8 17:2 23:9 27:8 28:1 29:15 30:8 33:10 42:5 44:4 46:1 48:2 49:1 51:3 52:2 60:6 67:1 72:1 81: … |
	| graphics  | 297:1 27:2 29:3 30:3 33:1 80:2 131:1 233:1 235:2 304:1 355:1 365:1 474:1 475:1 770:2 775:2 778:2 813 … |
	| politics  | 29:4 30:1 33:1 35:1 51:1 143:1 245:1 388:1 466:1 467:1 511:1 747:1 748:1 770:1 775:2 778:1 850:1 23: … |
	| politics  | 9:2 12:3 23:1 27:1 29:3 30:2 33:4 42:1 48:1 51:1 54:1 60:1 72:1 73:1 76:1 81:3 122:2 137:1 144:1 1 …   |
	| politics  | 8:1 12:3 23:5 29:3 30:1 33:6 42:6 44:1 51:1 52:3 60:4 72:2 81:1 100:2 104:1 122:3 142:1 144:2 179: …   |

	- with categorical VarKeys :

	| Class | Words                                                                                              |
	| --------- | ------------------------------------------------------------------------------------------------------ |
	| atheism   | archive:4 name:2 atheism:10 resources:4 alt:2 last:1 modified:1 december:1 version:3 atheist:9 addre … |
	| atheism   | of:7 other:1 are:7 the:19 in:7 to:13 it:3 like:1 on:2 but:7 is:16 people:2 get:1 com:1 so:2 one:4 su … |
	| atheism   | of:6 and:7 are:2 the:13 in:5 us:1 to:4 it:6 on:1 but:2 is:3 people:2 can:2 for:3 one:1 or:1 society: … |
	| graphics  | of:1 and:2 the:9 in:1 to:3 like:1 on:1 but:1 with:2 is:5 people:1 for:7 who:1 one:1 address:1 black: … |
	| politics  | of:5 freedom:1 from:1 the:8 in:2 us:1 to:5 it:1 but:1 with:2 is:1 can:1 com:1 go:1 so:1 one:1 east:1 … |
	| politics  | of:11 from:4 and:21 are:5 the:38 in:10 to:17 it:17 like:1 on:2 their:1 but:2 with:4 is:18 north:1 pe … |
	| politics  | of:5 and:3 are:3 the:5 in:4 us:1 to:3 it:2 on:1 is:2 ca:2 people:2 for:3 who:1 by:3 see:3 they:2 tha … |

## Khiops versus SVMLight sparse format

The SVMLight tool exploits a sparse format that mainly consists of the target value followed by a list of key-value pairs with integer keys:

<target\> <feature\>:<value\> <feature\>:<value\> ... <feature\>:<value\> \# <info\>

Khiops can handle any number of fields, either for dense variables or for blocks of sparse variables. In the case of one dense field followed by one block of sparse variables with numerical VarKeys, Khiops format is very close from SVMLight format:

<target\> SEP <feature\>:<value\> <feature\>:<value\> ... <feature\>:<value\>

The main difference is that there must be a separator character (SEP) between the two fields. This separator character can be a tab or ‘;’ for example. If the separator character is the space character, the second field that contains the block of sparse variables must be surrounded by double-quotes, as it contains the space character.

The other difference is that the dictionary must explicitly specify all the variables in the block, with their names and VarKeys.
