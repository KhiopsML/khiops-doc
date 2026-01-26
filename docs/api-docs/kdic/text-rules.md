# Text Rules

Most text rules are similar to [`String Rules`](string-rules.md), with the main difference that their name is prefixed by
'Text', and either the first operand or the return value is of type Text instead of Categorical.

Only three rules are specific to Text variables:
[`FromText`](text-rules.md#fromtext), [`ToText`](text-rules.md#totext) and [`TextLoadFile`](text-rules.md#textloadfile), 

As a reminder, Text values are limited to 1,000,000 characters, instead of 1,000 characters for Categorical values.

## FromText

```kdic-api-docs
Categorical FromText(Text value)
```

Conversion of a text value to a categorical value


## ToText

```kdic-api-docs
Text TextLength(Categorical value)
```

Conversion of a categorical value to a text value


## TextLoadFile

```kdic-api-docs
Text TextLoadFile(Categorical value)
```

Loading a file as a text variable

Loading is performed up to the maximum size allowed for a Text variable.
The characters '\0', '\r', and '\n' are replaced with spaces to prevent issues when writing the data to output files.

The file can be local or referenced by a URI, provided that cloud file drivers are loaded: see [`Cloud Storage`](../../tutorials/storage.md).


## TextLength

```kdic-api-docs
Numerical TextLength(Text value)
```

Length in chars of a text value.


## TextLeft

```kdic-api-docs
Text TextLeft(Text value, Numerical charNumber)
```

Extraction of the left substring of a text value.

If `charNumber` is less than 0, returns an empty value.

If `charNumber` is beyond the value length, returns the input value.

## TextRight

```kdic-api-docs
Text TextRight(Text value, Numerical charNumber)
```

Extraction of the right substring of a text value

If `charNumber` is less than 0, returns an empty value.

If `charNumber` is beyond the value length, returns the input value.

## TextMiddle

```kdic-api-docs
Text TextMiddle(Text value, Numerical startChar, Numerical charNumber)
```

Extraction of the middle substring of a text value.

If `startChar` is not valid (must start at 1), returns and empty value.

If `charNumber` is less than 0, returns an empty value.

If the end of the extraction is beyond the value length, returns the end of the input value.

## TextTokenLength

```kdic-api-docs
Numerical TextTokenLength(Text value, Categorical separators)
```

Length in tokens of a text value.

A token is a non-empty substring that does not contain any separator character. The tokens are
separated by one or many separator characters, which definition is given in the separator parameter.

If the separator parameter is empty, there is at most one token in the input value.

!!! example

    Using separators `" ,"` (blank and comma), the text value `" Numbers: 1, 2, 3.14, 4,5"`
    contains exactly six tokens: `Numbers:`,  `1` `2` `3.14` `4` `5`.

## TextTokenLeft

```kdic-api-docs
Text TextTokenLeft(Text value, Categorical separators, Numerical tokenNumber)
```

Extraction of the left tokens in a text value.

If several tokens are extracted, they remain separated by the initial separator characters used in
the input value.

If the `tokenNumber` is less than 0, returns an empty value.

If the number of tokens is beyond the token length, returns the input value (cleaned from its begin
and end separators).

## TextTokenRight

```kdic-api-docs
Text TextTokenRight(Text value, Categorical separators, Numerical tokenNumber)
```

Extraction of the right tokens in a text value.

If several tokens are extracted, they remain separated by the initial separator characters used in
the input value.

If the `tokenNumber` is less than 0, returns an empty value.

If the number of tokens is beyond the token length, returns the input value (cleaned from its begin
and end separators).

## TextTokenMiddle

```kdic-api-docs
Text TextTokenMiddle(
    Text value, Text separators, Numerical startToken, Numerical tokenNumber
)
```

Extraction of the middle tokens in a text value.

If `startToken` is not valid (must start at 1), returns and empty value.

If several tokens are extracted, they remain separated by the initial separator characters used in
the input value.

If the `tokenNumber` is less than 0, returns an empty value.

If the number of tokens is beyond the token length, returns the input value (cleaned from its begin
and end separators).

## TextTranslate

```kdic-api-docs
Text TextTranslate(
    Text value, Structure(VectorC) searchValues, Structure(VectorC) replaceValues
)
```

Replace substrings in a text value. The replacement is performed in sequence with each search
value in the first parameter vector replaced by its corresponding value in the second parameter
vector.
Both vectors in the operands must contain only literal values (no variables or rules).

!!! example

    The following rule allows to replace accented characters with regular characters:

    ```kdic
    TextTranslate(inputValue, VectorC("é", "è", "ê", "à", "ï", "ç"), VectorC("e", "e", "e", "a", "i", "c"))
    ```

## TextSearch

```kdic-api-docs
Numerical TextSearch(Text value, Numerical startChar, Categorical searchValue)
```

Searches the position of a substring in a text value.

If `startChar` is not valid (must start at 1), returns -1.

If the substring is not found, returns -1.

## TextReplace

```kdic-api-docs
Text TextReplace(
    Text value, Numerical startChar, Categorical searchValue, Categorical replaceValue
)
```

Replaces a substring in a text value.

If `startChar` is not valid (must start at 1), returns the input value.

If the substring is not found, returns the input value, otherwise returns the modified value.

## TextReplaceAll

```kdic-api-docs
Text TextReplaceAll(
    Text value, Numerical startChar, Categorical searchValue, Categorical replaceValue
)
```

Replaces all substring in a text value.

It is the same as the [`TextReplace`](#textreplace) rule, except that `TextReplace` applies only to the first
found searched values, whereas `TextReplaceAll` applies to all found searched values

## TextRegexMatch

```kdic-api-docs
Numerical TextRegexMatch(Text value, Categorical regexValue)
```

Returns 1 if the entire value matches the regex, 0 otherwise.

The syntax for regular expressions is that of ECMAScript syntax (JavaScript).

For more details, [see the reference](https://www.cplusplus.com/reference/regex/ECMAScript).

## TextRegexSearch

```kdic-api-docs
Numerical TextRegexSearch(Text value, Numerical startChar, Categorical regexValue)
```

Searches the position of a regular expression in a text value.

If `startChar` is not valid (must start at 1), returns -1.

If the regular expression is not found, returns -1.

## TextRegexReplace

```kdic-api-docs
Text TextRegexReplace(
    Text value, Numerical startChar, Categorical regexValue, Categorical replaceValue
)
```

Replaces a regular expression in a text value.

If `startChar` is not valid (must start at 1), returns the input value.

If the regular expression is not found, returns the input value, otherwise returns the modified
value.

## TextRegexReplaceAll

```kdic-api-docs
Text TextRegexReplaceAll(Text value, Numerical startChar, Categorical regexValue, Categorical replaceValue)
```

Replaces all found regular expression in a text value.

It is the same as the [`TextRegexReplace`](#textregexreplace)
rule, except that `TextRegexReplace` applies only to the first found searched values, whereas
`TextRegexReplaceAll` applies to all found searched values

## TextToUpper

```kdic-api-docs
Text TextToUpper(Text value)
```

Conversion to upper case of a text value.

## TextToLower

```kdic-api-docs
Text TextToLower(Text value)
```

Conversion to lower case of a text value.

## TextConcat

```kdic-api-docs
Text TextConcat(Text value1,...)
```

Concatenation of text values.

## TextHash

```kdic-api-docs
Numerical TextHash(Text value, Numerical max)
```

Computes a hash value of a text value, between 0 and max-1.

## TextEncrypt

```kdic-api-docs
Text TextEncrypt(Text value, Categorical key)
```

Encryption of a text value using an encryption key.

The encryption method used a "randomized" version of the input value. This is not a public
encryption method, and it is convenient for basic use such as making the data anonymous. The
encrypted value contains only alphanumeric characters. No reverse encryption method is provided.

!!! warning

     Non printable characters are first replaced by blank characters, prior to encryption.
