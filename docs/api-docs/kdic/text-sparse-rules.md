# Text Sparse Rules

The sparse text rules allow for tokenizing text values, as well as TextListValues. 
They produce a block of numerical variables, one for each token count, where each *VarKey** holds the value of the corresponding token to be extracted.


## TextWords

```kdic-api-docs
Block(Numerical) TextWords(Text value)
```

Tokenization of a Text value into a bag of words.
The words tokenization process uses separator or control characters as delimiters.
The obtained words are either sequences of punctuation characters or sequences of any other character.

!!! example 

	In this  example, the block of variables named *BlogWords* is filled from 
	the *Blog* variable using a word tokenization process.
	Each variable within the block has a *VarKey* corresponding to the specific word to count.
	For example, if the value of the Blog variable is "Hello world!", the sparse block 
	BlogWords will include variables *Count_Hello*, *Count_world* and *Count_!*, each with a value of 1.

	```kdic
	Dictionary Document
	{
		Categorical DocId;
		Text Blog;
		{
		Numerical	Count_hello		; <VarKey="hello">
		Numerical	Count_Hello		; <VarKey="Hello">
		Numerical	Count_world		; <VarKey="world">
		Numerical	`Count_.`		; <VarKey=".">
		Numerical	`Count_!`		; <VarKey="!">
		} BlogWords = TextWords(Blog) ;
	};
	```


## TextNgrams

```kdic-api-docs
Block(Numerical) TextNgrams(Text value)
```

Tokenization of a Text value into a bag of ngrams.
The ngrams are ngrams of bytes, from 1-grams to 8-grams.

!!! example 

	In this  example, the block of variables named *BlogNgrams* is filled from 
	the *Blog* variable using a ngrams tokenization process.
	Each variable within the block has a *VarKey* corresponding to the specific ngram to count.
	For example, if the value of the Blog variable is "Hello world!", the sparse block 
	BlogNgrams will include variable *Count1gram(l)* with a value of 3, and variables
	*Count3gram(lo )*, *Count6gram(world!)* and *Count1gram(!)* with a value of 1.

	```kdic
	Dictionary Document
	{
		Categorical DocId;
		Text Blog;
		{
		Numerical	`Count1gram(h)`		; <VarKey="h">
		Numerical	`Count1gram(l)`		; <VarKey="l">
		Numerical	`Count4gram(hell)`		; <VarKey="hell">
		Numerical	`Count3gram(lo )`		; <VarKey="lo ">
		Numerical	`Count6gram(world!)`		; <VarKey="world!">
		Numerical	`Count1gram(!)``		; <VarKey="!">
		} BlogNgrams = TextNgrams(Blog) ;
	};
	```


## TextTokens

```kdic-api-docs
Block(Numerical) TextTokens(Text value)
```

Tokenization of a Text value into a bag of tokens.
The tokens tokenization process simply uses the blank character as delimiter. 
This method assumes that the text has been already preprocessed (eg. lemmatization).

!!! example 

	In this  example, the block of variables named *BlogTokens* is filled from 
	the *Blog* variable using a word tokenization process.
	Each variable within the block has a *VarKey* corresponding to the specific word to count.
	For example, if the value of the Blog variable is "Hello world!", the sparse block 
	BlogTokens will include variables *Count_Hello* and *Count_world!* with a value of 1.

	```kdic
	Dictionary Document
	{
		Categorical DocId;
		Text Blog;
		{
		Numerical	Count_hello		; <VarKey="hello">
		Numerical	Count_Hello		; <VarKey="Hello">
		Numerical	Count_world		; <VarKey="world">
		Numerical	`Count_world!`	; <VarKey="world!">
		Numerical	`Count_.`		; <VarKey=".">
		Numerical	`Count_!`		; <VarKey="!">
		} BlogWords = TextWords(Blog) ;
	};
	```

## TextListWords

```kdic-api-docs
Block(Numerical) TextListWords(TextList value)
```

Tokenization of a TextList value into a bag of words.
The tokenization method used is the same as that of [`TextWords`](text-sparse-rules.md#textwords)), applied each Text values within the TextList.

## TextListNgrams

```kdic-api-docs
Block(Numerical) TextListNgrams(TextList value)
```

Tokenization of a TextList value into a bag of ngrams.
The tokenization method used is the same as that of [`TextNgrams`](text-sparse-rules.md#textngrams)), applied each Text values within the TextList.


## TextListTokens

```kdic-api-docs
Block(Numerical) TextListTokens(TextList value)
```

Tokenization of a TextList value into a bag of tokens.
The tokenization method used is the same as that of [`TextTokens`](text-sparse-rules.md#texttokens)), applied each Text values within the TextList.
