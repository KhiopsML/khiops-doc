# TimestampTZ Rules

`TimestampTZ` values are encoded in data table files using Khiops native format
`YYYY-MM-DD HH:MM:SS.zzzzzz`.

`TimestampTZ` values consist of a local timestamp value together with time zone information, using
the ISO 8601 time zone format:

- `<Timestamp format>zzzzz`: Basic time zone format (Z or +hhmm or –hhmm)
- `<Timestamp format>zzzzzz`: Extended time zone format (Z or +hh:mm or –hh:mm), with hours and
  minutes separated by `:`

`TimestampTZ` values are time zone-aware whereas Timestamp values are not.

`TimestampTZ` values can be transformed to `Timestamp` values using either the `LocalTimestamp` or
`UtcTimestamp` rules. Then, the `Timestamp` rules that extract information can be used (ex:
`GetDate`, `GetTime`, `DecimalYearTS`, `DecimalWeekDay`, `AbsoluteSecond`).

TimestampTZ rules return a missing value when their timestampTZ operand is not valid or when a numerical operand is missing or invalid.

## FormatTimestampTZ

```kdic-api-docs
Categorical FormatTimestampTZ(TimestampTZ value, Categorical timestampTZFormat)
```

Formats a `TimestampTZ` value into a `Categorical` value using a `TimestampTZ` format. `TimestampTZ`
format is a categorical constant value among the available `TimestampTZ` formats (for example:
`YYYY-MM-DD HH:MM:SSzzzzzz`).

## AsTimestampTZ

```kdic-api-docs
TimestampTZ AsTimestampTZ(Categorical timestampTZString, Categorical timestampFormat)
```

Recodes a categorical value into a `TimestampTZ` value using a `TimestampTZ` format.

!!! example

    ```kdic
    AsTimestampTZ("2014-01-15 18:25:00+02:00", "YYYY-MM-DD HH:MM:SSzzzzzz")
    ```

## UtcTimestamp

```kdic-api-docs
Timestamp UtcTimestamp(TimestampTZ value)
```

Builds a `Timestamp` value from a `TimestampTZ` value after conversion to UTC time zone.

!!! example

  Applying `UtcTimestamp` to `2020-03-21 12:15:30+02:00` returns the timestamp `2020-03-21
  10:15:30`.


## LocalTimestamp

```kdic-api-docs
Timestamp LocalTimestamp(TimestampTZ value)
```

Builds a `Timestamp` value from a `TimestampTZ` value after conversion to local time zone.

!!! example

    Applying `LocalTimestamp` to the `TimestampTZ` value  `2020-03-21 12:15:30+02:00` returns the
    `Timestamp` value `2020-03-21 12:15:30`.

## SetTimeZoneMinutes

```kdic-api-docs
TimestampTZ SetTimeZoneMinutes(Timestamp value, Numerical minutes)
```

Modify the time zone information of a timestampTZ value. The minutes must be between -12\*60 and +14\*60.

!!! example

    Applying `SetTimestampMinutes` to the `TimestampTZ` `2020-03-21 12:15:30-03:00` with 120 for the
    `minutes` argument returns the `TimestampTZ` `2020-03-21 12:15:30+02:00`.

## GetTimeZoneMinutes

```kdic-api-docs
Numerical GetTimeZoneMinutes(TimestampTZ value)
```

Returns the total minutes of the time zone (+- (hh \* 60 + mm)) from a timestampTZ value.

!!! example

    Applying `GetTimestampMinutes` to the timestampTZ `2020-03-21 12:15:30+02:00` returns 120.

## DiffTimestampTZ

```kdic-api-docs
Numerical DiffTimestampTZ(TimestampTZ value1, TimestampTZ value2)
```

Difference in seconds between two timestampTZ values.

## AddSecondsTSTZ

```kdic-api-docs
Timestamp AddSecondsTSTZ(TimestampTZ value, Numerical secondNumber)
```

Adds a number of seconds to a timestampTZ value.

## IsTimestampTZValid

```kdic-api-docs
Numerical IsTimestampTZValid(TimestampTZ value)
```

Returns 1 if a `TimestampTZ` value is valid.

## BuildTimestampTZ

```kdic-api-docs
TimestampTZ BuildTimestampTZ(Timestamp timestampValue, Time timeValue)
```

Builds a timestampTZ value from a timestamp value and time zone information in minutes. The minutes
must be between `-12*60` and `+14*60`.
