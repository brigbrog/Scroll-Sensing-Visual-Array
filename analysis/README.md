# Scroll Sense

## 📁 Structure
```
├── raw/
│   ├── p1/
│   ├── p2/
│   ├── ...
│   └── pN/
├── edited/
│   ├── p1/
│   ├── p2/
│   ├── ...
│   └── pN/
├── finalized/
│   ├── p1/
│   ├── p2/
│   ├── ...
│   └── pN/
├── scripts/
│   ├── clean_data.py
└── README.md
```

## Descriptions

### `raw/`
- Contains the anonymized CSV files from the study
- Each participant folder (`p1`, `p2`, …, `pN`) includes five files in each folder named using the format:

```
p{number}{content_type}{condition_type}.csv
```

- number: Participant ID (e.g., `1`, `2`, `3`)
- content_type: `short` or `long`
- condition_type: `none`, `vis`, `vib`, `aud`, `all`

### `edited/`
- Stores cleaned and filtered versions
- Includes:
  - Removing ectra columns  
  - Converting time from milliseconds to seconds  
  - Renaming columns

### `finalized/`
- Contains data ready for analysis/visualization  

## Scripts

### `clean_data.py`
Purpose: Cleans all files for each participant and stores them in `edited/`

command:
```bash
python scripts/clean_data.py
```