# Year-Based Color Filtering Feature

## Overview

The Montana Species Distribution Mapper now includes a powerful year-based color filtering system that allows users to visualize temporal patterns in species distribution data. This feature enables researchers to distinguish between historical and recent records by applying different colors based on collection dates.

## Feature Components

### 1. Color Configuration
The system provides three color settings:

- **Pre-Year Color**: Applied to records collected before or equal to the specified year
- **Post-Year Color**: Applied to records collected after the specified year  
- **Single Color**: Applied when no year is specified or when records lack year data

### 2. Year Input
- **Split by Year**: An optional numeric input field where users can specify a year to split the data
- **Dynamic**: The split year can be changed at any time and maps will be regenerated accordingly

## How It Works

### Color Logic
1. **No Year Specified**: All counties use the Single Color
2. **Year Specified**: 
   - Records ≤ split year → Pre-Year Color
   - Records > split year → Post-Year Color
   - Records without year data → Single Color

### County-Level Coloring
For each county, the system analyzes all records for that species:
- If **any** record in the county has a year > split year → Post-Year Color
- If **only** records ≤ split year exist → Pre-Year Color  
- If **no** records have valid years → Single Color

This ensures that counties with mixed temporal data are properly represented.

## User Interface

### Color Selection Panel
The interface includes:
- Three color picker dropdowns with common color options
- Support for custom color names and hex codes
- Real-time color validation
- Helpful tooltips explaining the feature

### Year Input
- Simple numeric input field
- Optional - can be left empty for single-color mode
- Validates input and provides feedback

## Data Requirements

### Excel File Format
Your Excel file should include:
- `county`: Montana county names (required)
- `family`: Taxonomic family names (required) 
- `genus`: Taxonomic genus names (required)
- `species`: Species names (required)
- `year`: Collection year in YYYY format (optional)
- `subgenus`: Subgenus names (optional)

### Year Data Processing
- Years are automatically converted to numeric format
- Invalid years become NaN and use Single Color
- Missing year data uses Single Color
- The system reports how many records have valid year data

## Usage Examples

### Example 1: Single Color Mode
- Leave "Split by Year" empty
- Set "Single Color" to "grey"
- All counties with records will be colored grey

### Example 2: Year-Based Split
- Set "Split by Year" to "2014"
- Set "Pre-Year Color" to "green" 
- Set "Post-Year Color" to "red"
- Set "Single Color" to "grey"
- Result:
  - Counties with records ≤ 2014 → Green
  - Counties with records > 2014 → Red
  - Counties with no year data → Grey

### Example 3: Mixed Temporal Data
If a county has records from both 2010 and 2018 with split year 2014:
- The county will be colored with Post-Year Color (red)
- This indicates the county has recent records

## Export Features

### Legend Generation
Downloaded maps automatically include a dynamic legend:
- **With Year Split**: Shows "Before or equal to 2014 → Green" and "After 2014 → Red"
- **Without Year Split**: Shows "Color Used: Grey"

### Export Formats
- **Current Page**: Single TIFF/SVG file with legend
- **All Maps**: ZIP archive with multiple pages, each including the legend

## Technical Implementation

### Color Validation
- All colors are validated against matplotlib's color system
- Invalid colors trigger error messages
- Real-time validation during user input

### Performance
- Efficient county-level color determination
- Minimal impact on map generation speed
- Optimized for large datasets

### Error Handling
- Graceful handling of invalid year data
- Fallback to single color for problematic records
- Clear user feedback for data issues

## Best Practices

### Color Selection
- Use contrasting colors for pre/post year distinction
- Consider colorblind accessibility
- Test color visibility on different backgrounds

### Year Selection
- Choose meaningful split years (e.g., major events, policy changes)
- Consider data distribution when selecting split points
- Document the reasoning for year selection

### Data Quality
- Ensure year data is consistent and accurate
- Use 4-digit year format (YYYY)
- Validate year ranges are reasonable for your taxa

## Troubleshooting

### Common Issues
1. **No color change**: Check if year data exists in your Excel file
2. **Invalid colors**: Use standard color names or valid hex codes
3. **Unexpected coloring**: Verify year format and split year value

### Data Validation
The system provides feedback on:
- Number of records with valid years
- County name mismatches
- Missing required columns

## Future Enhancements

Potential improvements could include:
- Multiple year thresholds (e.g., 3-color system)
- Custom legend text
- Year range visualization
- Temporal trend analysis tools 