# Montana Multiple Species Distribution Mapper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A powerful visualization tool for analyzing and mapping species distribution across Montana counties. This application helps researchers, biologists, and conservationists visualize species occurrence patterns and generate high-quality distribution maps for publication and analysis.

## 🚀 Quick Start

1. Download the latest release
2. Load your Excel data with species records
3. Select taxonomic filters
4. Generate publication-ready distribution maps

## Overview

The Montana Multiple Species Distribution Mapper is a desktop application designed to help researchers, biologists, and conservationists visualize and analyze species distribution patterns across Montana counties. The application supports taxonomic filtering and generates publication-ready distribution maps with customizable color schemes.

## Features

### 1. Species Distribution Mapping
- Generate individual distribution maps for each species
- Color-coded counties showing species occurrence
- **NEW: Year-based color filtering** - Distinguish between historical and recent records
- Customizable color schemes for different species or groups
- Publication-ready scientific name formatting
- Specimen count and county coverage information

### 2. Taxonomic Filtering
- Filter by Family, Genus, and Species levels
- Hierarchical selection system with dynamic dropdowns
- Support for all taxonomic groups (not limited to bees)
- "All" options for broader analysis

### 3. Map Export & Management
- High-resolution map export (300 DPI TIFF format)
- Pagination system for large datasets (15 maps per page)
- Batch export capabilities (ZIP format)
- Individual page downloads
- Publication-ready map layouts with proper scientific formatting
- **NEW: Dynamic legends** showing year-based color explanations

### 4. User Experience
- User-friendly interface with tooltips and helper text
- Real-time map generation with progress indicators
- Comprehensive data validation and error reporting
- County name standardization and matching
- Toast notifications for user feedback
- Responsive design with scrollable controls

## 📁 Project Structure

```
Montana_Multiple_Species_Distribution_Mapper/
├── Montana_Multiple_Species_Distribution_Mapper.py  # Main application
├── MT_Base_Map_Generator.py      # Base map utility
├── requirements.txt              # Python dependencies
├── app_icon.ico                 # Application icon
├── README.md                    # This file
├── LICENSE                      # MIT License
├── docs/                        # Documentation
│   ├── user_guide.md           # Detailed user guide
│   └── example_data_format.md  # Data format specifications
├── MontanaCounties_shp/         # Montana county shapefiles
├── shapefiles/                  # Additional shapefile data
└── example_data/               # Example datasets
```

## Installation

### Prerequisites
- Windows 10 or later
- Python 3.8 or later (if installing from source)

### Method 1: Using the Executable (Recommended)
1. Download the latest `Montana_Multiple_Species_Distribution_Mapper.exe` from the releases page
2. Double-click the executable to run the application
3. No additional installation steps required

### Method 2: Installing from Source
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/Montana_Multiple_Species_Distribution_Mapper.git
cd Montana_Multiple_Species_Distribution_Mapper
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python Montana_Multiple_Species_Distribution_Mapper.py
   ```

## Data Requirements

### Excel File Format
Your Excel file must include the following columns:
- `county`: Montana county names (required)
- `family`: Taxonomic family names (required)
- `genus`: Taxonomic genus names (required)
- `species`: Species names (required)
- `year`: Collection year (YYYY format) - **optional but enables year-based color filtering**
- `subgenus`: Subgenus names - optional

### Data Validation
- County names are automatically standardized
- Taxonomic names are processed for consistency
- Invalid or missing data is reported
- Montana-only records are filtered automatically

### County Names
- County names must match Montana county names exactly
- The application will standardize county names by:
  - Converting to lowercase
  - Removing extra whitespace
  - Converting '&' to 'and'

## Usage Guide

### Quick Start
1. **Launch the Application**
   - Run the executable or start from source
   - The application will load Montana county boundaries automatically

2. **Load Data**
   - Click "Load Excel File"
   - Select your Excel file (.xlsx format)
   - Review the data summary and validation results
   - Check for any county name mismatches

3. **Configure Settings**
   - **Year-Based Color Filtering** (NEW):
     - Set "Pre-Year Color" (e.g., green for historical records)
     - Set "Post-Year Color" (e.g., red for recent records)
     - Set "Single Color" (e.g., grey for records without year data)
     - Enter "Split by Year" (e.g., 2014) to enable temporal filtering
     - Leave year empty to use single color for all records
   - Choose taxonomic filters:
     - Select Family (or "All" for all families)
     - Select Genus (or "All" for all genera in family)
     - Select Species (or "all" for all species in genus)

4. **Generate and Export Maps**
   - Click "Generate Maps" to create visualizations
   - Browse through generated maps using pagination (15 maps per page)
   - Download options:
     - "Download Current Page" for single TIFF file
     - "Download All Maps" for ZIP archive
   - Files are automatically saved to your Downloads folder

### Advanced Features
- **Color Customization**: Use any valid color name or hex code
- **Pagination**: Navigate through large datasets efficiently
- **Batch Export**: Download all maps as a single ZIP file
- **Scientific Formatting**: Maps include proper italicized scientific names

## Troubleshooting

### Common Issues
1. **Missing Counties**
   - Ensure county names match exactly
   - Check console output for valid county names
   - Review standardization rules (e.g., "&" becomes "and")
   - Verify county names are in the Montana dataset

2. **No Data Shown**
   - Verify Excel file format (.xlsx)
   - Check required columns exist (county, family, genus, species)
   - Ensure data contains Montana records
   - Check for empty or invalid cells

3. **No Maps Generated**
   - Verify Family and Genus selections
   - Check that species exist for selected taxa
   - Ensure data contains valid records
   - Try selecting "All" for broader results

4. **Export Issues**
   - Ensure you have write permissions in Downloads folder
   - Check available disk space
   - Verify no files are open in other applications

### Error Messages
- "Missing required columns": Check Excel file format and column names
- "No valid Montana county records": Verify county names match Montana counties
- "Invalid colors": Use valid color names or hex codes (e.g., #FF5733)
- "No species found": Check Family and Genus selections
- "County name mismatch": Review console output for valid county names

## Support

For bug reports and feature requests, please open an issue on the GitHub repository.

## Contributing

We welcome contributions! Please feel free to submit pull requests or open issues for:
- Bug fixes
- New features
- Documentation improvements
- Performance optimizations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Montana State University
- Montana Geographic Information Clearinghouse for county boundary data
- All contributors to the Montana biodiversity research community
- The scientific community for feedback and testing

## Version History

- v1.0.0 (2024-03-XX)
  - Initial release
  - Species distribution mapping with individual species maps
  - Taxonomic filtering with hierarchical selection
  - High-resolution map export (300 DPI TIFF)
  - Pagination system for large datasets
  - Batch export capabilities (ZIP format)
  - Publication-ready scientific name formatting
  - Comprehensive data validation and error reporting