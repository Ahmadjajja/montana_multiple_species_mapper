# Data Format Requirements

## Excel File Format

The Montana Species Distribution Mapper requires a specific Excel file format to function correctly. This document outlines the required structure and provides examples.

### Required Columns

Your Excel file must contain the following columns:

| Column Name | Description | Format | Example |
|------------|-------------|---------|---------|
| county | Montana county name | Text | Gallatin |
| family | Taxonomic family name | Text | Apidae |
| genus | Taxonomic genus name | Text | Bombus |
| species | Species name | Text | nevadensis |
| year | Collection year | YYYY | 1998 |

### Example Data

```
county      | family    | genus     | species     | year
------------|-----------|-----------|-------------|------
Gallatin    | Apidae    | Bombus    | nevadensis  | 1998
Missoula    | Halictidae| Lasioglossum| pruinosum | 2005
Flathead    | Apidae    | Apis      | mellifera   | 2015
Ravalli     | Vespidae  | Vespula   | vulgaris    | 2010
```

### Data Validation Rules

1. County Names
   - Must match Montana county names exactly (case-insensitive)
   - Will be standardized by:
     - Converting to lowercase
     - Removing extra whitespace
     - Converting '&' to 'and'

2. Taxonomic Names
   - Family: Capitalized (will be auto-formatted)
   - Genus: Capitalized (will be auto-formatted)
   - Species: Lowercase (will be auto-formatted)

3. Year Format
   - Must be 4-digit year (YYYY)
   - Must be a valid year (e.g., 1900-2024)
   - Can include decimal points for specific dates (e.g., 1998.0)

### Valid Montana County Names

```
Beaverhead     | Gallatin      | Park
Big Horn       | Garfield      | Petroleum
Blaine         | Glacier       | Phillips
Broadwater     | Golden Valley | Pondera
Carbon         | Granite       | Powder River
Carter         | Hill          | Powell
Cascade        | Jefferson     | Prairie
Chouteau       | Judith Basin  | Ravalli
Custer         | Lake          | Richland
Daniels        | Lewis and Clark| Roosevelt
Dawson         | Liberty       | Rosebud
Deer Lodge     | Lincoln       | Sanders
Fallon         | Madison       | Sheridan
Fergus         | McCone        | Silver Bow
Flathead       | Meagher       | Stillwater
```

### Common Data Issues and Solutions

1. **Missing Data**
   - Empty cells are allowed but will be filtered out
   - Use consistent formatting for missing data (leave blank)

2. **Invalid County Names**
   - Check for typos
   - Ensure proper spacing
   - Remove any special characters

3. **Year Format Issues**
   - Remove any text from year field
   - Ensure year is in YYYY format
   - Remove any time components

### Best Practices

1. **Data Preparation**
   - Clean your data before importing
   - Remove any formatting
   - Save as .xlsx format

2. **Quality Control**
   - Verify county names against the list
   - Check for consistent capitalization
   - Validate year formats

3. **File Management**
   - Keep backup copies of your data
   - Use descriptive filenames
   - Include version numbers if needed 