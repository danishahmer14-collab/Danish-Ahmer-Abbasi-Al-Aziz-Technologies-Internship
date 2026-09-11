# Dataset Documentation

## Source

The Titanic dataset, loaded via `seaborn.load_dataset("titanic")`. This is a
well-known, publicly available dataset describing passengers aboard the RMS
Titanic, which sank in 1912. It's commonly used as a beginner-friendly
real-world dataset for classification tasks.

## Size

- **891 rows** (passengers)
- **15 columns** (before cleaning)

## Column Descriptions

| Column | Type | Description |
|---|---|---|
| `survived` | int (0/1) | **Target/label.** 0 = did not survive, 1 = survived |
| `pclass` | int (1/2/3) | Passenger class (1 = 1st/highest, 3 = 3rd/lowest) |
| `sex` | text | Passenger's sex (male/female) |
| `age` | float | Passenger's age in years (missing for ~177 passengers) |
| `sibsp` | int | Number of siblings/spouses aboard |
| `parch` | int | Number of parents/children aboard |
| `fare` | float | Ticket fare paid |
| `embarked` | text | Port of embarkation code (C/Q/S) |
| `class` | text | Same as `pclass`, but as text (First/Second/Third) |
| `who` | text | man / woman / child |
| `adult_male` | bool | Whether the passenger was an adult male |
| `deck` | text | Deck letter (mostly missing — 688 of 891 rows) |
| `embark_town` | text | Full name of the port of embarkation |
| `alive` | text | Same as `survived`, but as text (yes/no) |
| `alone` | bool | Whether the passenger was traveling alone |

## Features Used in This Project

For modeling, we selected 6 numeric/encodable features:
`pclass, sex, age, fare, sibsp, parch` → predicting `survived`.

Columns like `class`, `who`, `alive` were excluded because they duplicate
information already captured by `pclass`/`survived`, and `deck` was dropped
due to excessive missing data (77% missing).

## Known Data Quality Issues

- **`age`**: ~177 missing values (~20%) — filled with the median age during
  cleaning, since median is robust to outliers/skew.
- **`deck`**: ~688 missing values (~77%) — dropped entirely; not enough data
  to be reliably useful.
- **`embarked` / `embark_town`**: 2 missing values each — filled with the
  most common port (mode).

## License / Usage

This dataset is widely used for educational purposes (e.g., via Kaggle's
"Titanic - Machine Learning from Disaster" competition) and is included as a
built-in sample dataset in the Seaborn library.