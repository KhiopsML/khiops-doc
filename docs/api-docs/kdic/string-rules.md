# String Rules

If a missing value is used as operand for a rule returning a `Categorical` value, the return value
is the empty string.

## Length

```kdic-api-docs
Numerical Length(Categorical value)
```

Length in chars of a categorical value.

## Left

```kdic-api-docs
Categorical Left(Categorical value, Numerical charNumber)
```

Extraction of the left substring of a categorical value.

If `charNumber` is less than 0, returns an empty value.

If `charNumber` is beyond the value length, returns the input value.

## Right

```kdic-api-docs
Categorical Right(Categorical value, Numerical charNumber)
```

Extraction of the right substring of a categorical value

If `charNumber` is less than 0, returns an empty value.

If `charNumber` is beyond the value length, returns the input value.

## Middle

```kdic-api-docs
Categorical Middle(Categorical value, Numerical startChar, Numerical charNumber)
```

Extraction of the middle substring of a categorical value.

If `startChar` is not valid (must start at 1), returns and empty value.

If `charNumber` is less than 0, returns an empty value.

If the end of the extraction is beyond the value length, returns the end of the input value.

## TokenLength

```kdic-api-docs
Numerical TokenLength(Categorical value, Categorical separators)
```

Length in tokens of a categorical value.

A token is a non-empty substring that does not contain any separator character. The tokens are
separated by one or many separator characters, which definition is given in the separator parameter.

If the separator parameter is empty, there is at most one token in the input value.

!!! example

    Using separators `" ,"` (blank and comma), the categorical value `" Numbers: 1, 2, 3.14, 4,5"`
    contains exactly six tokens: `Numbers:`,  `1` `2` `3.14` `4` `5`.

## TokenLeft

```kdic-api-docs
Categorical TokenLeft(Categorical value, Categorical separators, Numerical tokenNumber)
```

Extraction of the left tokens in a categorical value.

If several tokens are extracted, they remain separated by the initial separator characters used in
the input value.

If the `tokenNumber` is less than 0, returns an empty value.

If the number of tokens is beyond the token length, returns the input value (cleaned from its begin
and end separators).

## TokenRight

```kdic-api-docs
Categorical TokenRight(Categorical value, Categorical separators, Numerical tokenNumber)
```

Extraction of the right tokens in a categorical value.

If several tokens are extracted, they remain separated by the initial separator characters used in
the input value.

If the `tokenNumber` is less than 0, returns an empty value.

If the number of tokens is beyond the token length, returns the input value (cleaned from its begin
and end separators).

## TokenMiddle

```kdic-api-docs
Categorical TokenMiddle(
    Categorical value, Categorical separators, Numerical startToken, Numerical tokenNumber
)
```

Extraction of the middle tokens in a categorical value.

If `startToken` is not valid (must start at 1), returns and empty value.

If several tokens are extracted, they remain separated by the initial separator characters used in
the input value.

If the `tokenNumber` is less than 0, returns an empty value.

If the number of tokens is beyond the token length, returns the input value (cleaned from its begin
and end separators).

## Translate

```kdic-api-docs
Categorical Translate(
    Categorical value, Structure(VectorC) searchValues, Structure(VectorC) replaceValues
)
```

Replace substrings in a categorical value. The replacement is performed in sequence with each search
value in the first parameter vector replaced by its corresponding value in the second parameter
vector.

!!! example

    The following rule allows to replace accented characters with regular characters:

    ```kdic
    Translate(inputValue, VectorC("é", "è", "ê", "à", "ï", "ç"), VectorC("e", "e", "e", "a", "i", "c"))
    ```

## Search

```kdic-api-docs
Numerical Search(Categorical value, Numerical startChar, Categorical searchValue)
```

Searches the position of a substring in a categorical value.

If `startChar` is not valid (must start at 1), returns -1.

If the substring is not found, returns -1.

## Replace

```kdic-api-docs
Categorical Replace(
    Categorical value, Numerical startChar, Categorical searchValue, Categorical replaceValue
)
```

Replaces a substring in a categorical value.

If `startChar` is not valid (must start at 1), returns the input value.

If the substring is not found, returns the input value, otherwise returns the modified value.

## ReplaceAll

```kdic-api-docs
Categorical ReplaceAll(
    Categorical value, Numerical startChar, Categorical searchValue, Categorical replaceValue
)
```

Replaces all substring in a categorical value.

It is the same as the [`Replace`](#replace) rule, except that Replace applies only to the first
found searched values, whereas `ReplaceAll` applies to all found searched values

## RegexMatch

```kdic-api-docs
Numerical RegexMatch(Categorical value, Categorical regexValue)
```

Returns 1 if the entire value matches the regex, 0 otherwise.

The syntax for regular expressions is that of ECMAScript syntax (JavaScript).

For more details, [see the reference](https://www.cplusplus.com/reference/regex/ECMAScript).

## RegexSearch

```kdic-api-docs
Numerical RegexSearch(Categorical value, Numerical startChar, Categorical regexValue)
```

Searches the position of a regular expression in a categorical value.

If `startChar` is not valid (must start at 1), returns -1.

If the regular expression is not found, returns -1.

## RegexReplace

```kdic-api-docs
Categorical RegexReplace(
    Categorical value, Numerical startChar, Categorical regexValue, Categorical replaceValue
)
```

Replaces a regular expression in a categorical value.

If `startChar` is not valid (must start at 1), returns the input value.

If the regular expression is not found, returns the input value, otherwise returns the modified
value.

## RegexReplaceAll

```kdic-api-docs
Categorical RegexReplaceAll(Categorical value, Numerical startChar, Categorical regexValue, Categorical replaceValue)
```

Replaces all found regular expression in a categorical value.

It is the same as the [`RegexReplace`](#regexreplace)
rule, except that `RegexReplace` applies only to the first found searched values, whereas
`RegexReplaceAll` applies to all found searched values

## ToUpper

```kdic-api-docs
Categorical ToUpper(Categorical value)
```

Conversion to upper case of a categorical value.

## ToLower

```kdic-api-docs
Categorical ToLower(Categorical value)
```

Conversion to lower case of a categorical value.

## Concat

```kdic-api-docs
Categorical Concat(Categorical value1,...)
```

Concatenation of categorical values.

## Hash

```kdic-api-docs
Numerical Hash(Categorical value, Numerical max)
```

Computes a hash value of a categorical value, between 0 and max-1.

## Encrypt

```kdic-api-docs
Categorical Encrypt(Categorical value, Categorical key)
```

Encryption of a categorical value using an encryption key.

The encryption method used a "randomized" version of the input value. This is not a public
encryption method, and it is convenient for basic use such as making the data anonymous. The
encrypted value contains only alphanumeric characters. No reverse encryption method is provided.

!!! warning

     Non printable characters are first replaced by blank characters, prior to encryption.
