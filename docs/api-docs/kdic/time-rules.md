# Time Rules
`Time` values are encoded in data table files using Khiops native format `HH:MM:SS.`,
or an alternative format specified by the
`TimeFormat` meta-data (see [`Meta-data`](../kdic/dictionary-files.md#meta-data)).

The `.` at the end of the format means that fractions of seconds are optional. The use of parenthesis in time formats means
that the corresponding digit is optional when it is null (e.g. `9:30:8` with format `(H)H:(M)M:(S)S`
corresponds to `09:30:08` with format `HH:MM:SS`):


All available formats are described below:

|                  |                   |             |
| ---------------- | ----------------- | ----------- |
| `HH:MM:SS`       | `HH:MM:SS.`       | `HH:MM`     |
| `HH.MM.SS`       | `HH.MM.SS.`       | `HH.MM`     |
| `(H)H:(M)M:(S)S` | `(H)H:(M)M:(S)S.` | `(H)H:(M)M` |
| `(H)H.(M)M.(S)S` | `(H)H.(M)M.(S)S.` | `(H)H.(M)M` |
| `HHMMSS`         | `HHMMSS.`         | `HHMM`      |

Valid times range from `00:00:00` to `23:59:59`, with optional fractions of seconds up to 1/1000 of
a second. Time rules return a missing value when their time operand is not valid or when a numerical
operand is missing.

## FormatTime

```kdic-api-docs
Categorical FormatTime(Time value, Categorical timeFormat)
```

Formats a time into a categorical value using a time format. Time format is a categorical constant
value among the available time formats (for example: `HH:MM:SS`).

## AsTime

```kdic-api-docs
Time AsTime(Categorical timeString, Categorical timeFormat)
```

Recodes a categorical value into a time using a time format.

!!! example

    ```kdic
    AsTime("18:25:00", "HH:MM:SS")
    ```

## Hour

```kdic-api-docs
Numerical Hour(Time value)
```

Hour in a time value, ranging from 0 to 23.

## Minute

```kdic-api-docs
Numerical Minute(Time value)
```

Minute in a time value, ranging from 0 to 59.

## Second

```kdic-api-docs
Numerical Second(Time value)
```

Second in a time value, ranging from 0 to 59.999.

!!! note

    Seconds can be precise up to one thousandth of a second (i.e., milliseconds).

## DaySecond

```kdic-api-docs
Numerical DaySecond(Time value)
```

Total second in a time value, since 00:00:00.

## DecimalTime

```kdic-api-docs
Numerical DecimalTime(Time value)
```

Decimal representation of the time within a day, ranging from 0.0 to approximately 23.999999 for 23:59:59.999.

Precisely, `DecimalTime := DaySecond/(24 * 60 * 60)`.

## DiffTime

```kdic-api-docs
Numerical DiffTime(Time value1, Time value2)
```

Difference in seconds between two time values.

## IsTimeValid

```kdic-api-docs
Numerical IsTimeValid(Time value)
```

Checks if a time value is valid.

## BuildTime

```kdic-api-docs
Time BuildTime(Numerical hour, Numerical minute, Numerical second)
```

Builds a time value from `hour`, `minute` and `second`.

The rule uses the floor value of hour and minute, and the full value of second. The hour must be
between 0 and 23. The minute must be between 0 and 59. The second must be between 0 and 59, with
optional fraction of second.


