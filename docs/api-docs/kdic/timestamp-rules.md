# Timestamp Rules

`Timestamp` values are encoded in data table files using Khiops native format `YYYY-MM-DD HH:MM:SS.`.
Other formats are available, that allow to convert categorical values to timestamp values:

- `<Date format> <Time format>`: A date format followed by a blank and a time format
- `<Date format>-<Time format>`: A date format followed by a `-` and a time format
- `<Date format>_<Time format>`: A date format followed by an `_` and a time format
- `<Date format>T<Time format>`: A date format followed by a `T` and a time format
- `<Date format><Time format>`: A date format directly followed by a time format. Valid only in the
  case of date and time formats with not separator character (e.g. `YYYYMMDDHHMMSS`).

`Timestamp` rules return a missing value when their timestamp operand is not valid or when
a numerical operand is missing.

## FormatTimestamp

```kdic-api-docs
Categorical FormatTimestamp(Timestamp value, Categorical timestampFormat)
```

Formats a timestamp into a categorical value using a timestamp format. Timestamp format is
a categorical constant value among the available timestamp formats (for example: `YYYY-MM-DD
HH:MM:SS`).

## AsTimestamp

```kdic-api-docs
Timestamp AsTimestamp(Categorical timestampString, Categorical timestampFormat)
```

Recodes a categorical value into a timestamp value using a timestamp format.

!!! example

  ```kdic
  AsTimestamp(“2014-01-15 18:25:00”, “YYYY-MM-DD HH:MM:SS”).
  ```

## GetDate

```kdic-api-docs
Date GetDate(Timestamp value)
```

Date in a timestamp value.

## GetTime

```kdic-api-docs
Time GetTime(Timestamp value)
```

Time in a timestamp value.

## DecimalYearTS

```kdic-api-docs
Numerical DecimalYearTS(Timestamp value)
```

Year in a timestamp value, with decimal part for day in year, at a timestamp precision.

## AbsoluteSecond

```kdic-api-docs
Numerical AbsoluteSecond(Timestamp value)
```

Total elapsed seconds since `2000-01-01 00:00:00`.

## DecimalWeekDay

```kdic-api-docs
Numerical DecimalWeekDay(Timestamp value)
```

Week day of the date of the timestamp value, plus decimal day of the time.

Precisely, `DecimalWeekDay := WeekDay(date) + DecimalTime(time)/24`.

## DiffTimestamp

```kdic-api-docs
Numerical DiffTimestamp(Timestamp value1, Timestamp value2)
```

Difference in seconds between two timestamp values.

## AddSeconds

```kdic-api-docs
Timestamp AddSeconds(Timestamp value, Numerical secondNumber)
```

Adds a number of seconds to a timestamp value.

## IsTimestampValid

```kdic-api-docs
Numerical IsTimestampValid(Timestamp value)
```

Checks if a timestamp value is valid.

## BuildTimestamp

```kdic-api-docs
Timestamp BuildTimestamp(Date dateValue, Time timeValue)
```

Builds a timestamp from a date and time values.

