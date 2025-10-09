# Date Rules

`Date` values are encoded in data table files using Khiops native format `YYYY-MM-DD`. Other formats
are available, that allow to convert categorical values to date values.

|              |              |              |            |
| ------------ | ------------ | ------------ | ---------- |
| `YYYY-MM-DD` | `YYYY/MM/DD` | `YYYY.MM.DD` | `YYYYMMDD` |
| `DD-MM-YYYY` | `DD/MM/YYYY` | `DD.MM.YYYY` | `DDMMYYYY` |
| `YYYY-DD-MM` | `YYYY/DD/MM` | `YYYY.DD.MM` | `YYYYDDMM` |
| `MM-DD-YYYY` | `MM/DD/YYYY` | `MM.DD.YYYY` | `MMDDYYYY` |

Valid dates range from `0001-01-01` to `9999-12-31`, with validity according to Gregorian calendar.
`Date` rules return a missing value when their date operand is not valid or when a numerical operand
is missing.

## FormatDate

```kdic-api-docs
Categorical FormatDate(Date value, Categorical dateFormat)
```

Format a date into a categorical value using a date format. Date format is a categorical constant
value among the available date formats (for example: `YYYY-MM-DD`).

## AsDate

```kdic-api-docs
Date AsDate(Categorical dateString, Categorical dateFormat)
```

Recode a categorical value into a date using a date format.

!!! example

    ```kdic
    AsDate("2014-01-15", "YYYY-MM-DD").
    ```

## Year

```kdic-api-docs
Numerical Year(Date value)
```

Year in a date value.

## Month

```kdic-api-docs
Numerical Month(Date value)
```

Month in a date value, ranging from 1 (January) to 12 (December).

## Day

```kdic-api-docs
Numerical Day(Date value)
```

Day in a date value, ranging from 1 to 31.

## YearDay

```kdic-api-docs
Numerical YearDay(Date value)
```

Day in year in a date value, starting at 1 for January 1st and ending at 365 or 366 for December 31st, depending on whether it is a leap year.

## WeekDay

```kdic-api-docs
Numerical WeekDay(Date value)
```

Day in week in a date value.

Returns 1 for Monday, 2 for Tuesday ..., 7 for Sunday.

## DecimalYear

```kdic-api-docs
Numerical DecimalYear(Date value)
```

Year in a date value, including a decimal part representing the day of the year.

Precisely, `DecimalYear = Year + (YearDay-1)/365` (or 366 for leap years).


## AbsoluteDay

```kdic-api-docs
Numerical AbsoluteDay(Date value)
```

Total elapsed days since `2000-01-01`.

## DiffDate

```kdic-api-docs
Numerical DiffDate(Date value1, Date value2)
```

Difference in days between two date values.

## AddDays

```kdic-api-docs
Date AddDays(Date value, Numerical dayNumber)
```

Adds a number of days to a date value.

## IsDateValid

```kdic-api-docs
Numerical IsDateValid(Date value)
```

Checks if a date value is valid.

## BuildDate

```kdic-api-docs
Date BuildDate(Numerical year, Numerical month, Numerical day)
```

Builds a date value from year, month and day.

The year must be between 1 and 9999. The month must be between 1 and 12. The day must be between
1 and 31, and consistent with the month and year.
