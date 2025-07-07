# TextList Rules

A TextList value is a list of Text values.

The TextList type is primarily a technical construct designed to address scalability issues when handling a large number of Text variables.
Its rules are mainly used internally by Khiops to gather all Text variables within a [`Multi-Table`](multi-table-rules-introduction.md) schema.


## TextList

```kdic-api-docs
TextList TextList(Text value1, ...)
```

Builds a list of text values.

## TextListSize

```kdic-api-docs
Numerical TextListSize(TextList value)
```

Number of text values in a list.

## TextListAt

```kdic-api-docs
Text TextListAt(TextList value, Numerical index)
```

Returns a text value at given index (index starts at 1). 
Returns `""` if the index is out of bounds.


## TextListConcat

```kdic-api-docs
TextList TextListConcat(TextList value1, ...)
```

Concatenation of TextList values.


## GetTextList

```kdic-api-docs
TextList GetTextList(Entity entityValue, TextList value)
```

Access to a `TextList` value of an entity. Returns an empty `TextList` value if the entity
does not exist.
This rule extends the [`Entity Rules`](entity-rules.md) to `TextList` variables.

## TableAllTexts


Numerical TableCountDistinct(Table table, Categorical value)

```kdic-api-docs
TextList TableAllTexts(Table table, TextList)
```

Aggregates all `Text` values from a secondary variable in a `TextList`.
This rule extends the [`Table Rules`](table-rules.md) to `Text` variables.

## TableAllTextLists

```kdic-api-docs
TextList TextList(Text value, ...)
```

Concatenates all `TextList` values from a secondary variable into a single `TextList`.
This rule extends the [`Table Rules`](table-rules.md) to `Text` variables.
