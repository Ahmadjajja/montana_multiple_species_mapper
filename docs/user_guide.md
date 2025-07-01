# Montana Species Distribution Mapper - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Species Distribution Mapping](#species-distribution-mapping)
4. [Taxonomic Filtering](#taxonomic-filtering)
5. [Map Generation](#map-generation)
6. [Exporting Maps](#exporting-maps)
7. [Tips and Tricks](#tips-and-tricks)

## Getting Started

### Installation
1. Download the latest release
2. Double-click the executable
3. No additional installation required

### First Launch
1. The application loads Montana county boundaries
2. Ready to load species distribution data
3. No analysis type selection needed

### Loading Data
1. Click "Load Excel File"
2. Select your data file
3. Review the data summary
4. Check for any validation messages

## Interface Overview

### Main Window Components
1. Left Panel
   - Data input controls
   - Color settings
   - Year filters
   - Taxonomic selection
2. Right Panel
   - Map display area
   - Legend
3. Top Bar
   - Title
   - Navigation

### Control Sections
1. Data Input
   - Load Excel button
   - File info display
2. Color Settings
   - Species occurrence color
   - Custom color support
3. Taxonomic Selection
   - Family dropdown
   - Genus dropdown
   - Species dropdown
4. Map Controls
   - Generate Maps button
   - Pagination controls
   - Download options

## Species Distribution Mapping

### Purpose
Generate individual distribution maps for each species within selected taxonomic groups.

### Steps
1. Load your data file
2. Choose color for species occurrence
3. Select taxonomic filters:
   - Family (or "All")
   - Genus (or "All")
   - Species (or "all")
4. Generate maps for all species

### Map Features
- Individual map for each species
- Color-coded counties showing occurrence
- Scientific name formatting
- Specimen count information

## Taxonomic Filtering

### Purpose
Filter species data by taxonomic hierarchy for focused analysis.

### Steps
1. Select Family level:
   - Choose specific family or "All"
   - Updates available genera
2. Select Genus level:
   - Choose specific genus or "All"
   - Updates available species
3. Select Species level:
   - Choose specific species or "all"
   - Generates maps for selected taxa

### Filter Options
- "All" options for broader analysis
- Hierarchical filtering system
- Dynamic dropdown updates

## Map Generation

### Process
1. Configure all settings
2. Click "Generate Maps"
3. Browse through generated maps
4. Use pagination for large datasets

### Map Elements
1. County boundaries
2. Color-coded species occurrence
3. Scientific name formatting
4. Specimen and county count information
5. Publication-ready layout

### Validation
- County name matching
- Taxonomic data validation
- Color validation
- Data presence verification

## Exporting Maps

### Export Process
1. Generate maps for desired taxa
2. Choose export option:
   - Download Current Page (Single TIFF)
   - Download All Maps (ZIP)
3. Files save automatically to Downloads folder

### File Format
- Format: TIFF (individual) or ZIP (batch)
- Resolution: 300 DPI
- Filename format:
  - Current Page: `Genus-timestamp_pageX.tiff`
  - All Maps: `Genus-timestamp.zip`

### Quality Control
- Check legend visibility
- Verify color contrast
- Ensure text readability
- Confirm data accuracy

## Tips and Tricks

### Performance
- Clean data before importing
- Use appropriate file sizes
- Close unused windows

### Color Selection
- Use contrasting colors
- Test visibility
- Consider colorblind accessibility
- Use standard colors when possible

### Data Management
- Keep regular backups
- Use consistent naming
- Validate data before import
- Check county names carefully

### Troubleshooting
1. Missing Counties
   - Verify county names
   - Check standardization
   - Review error messages
2. Color Issues
   - Use valid color names
   - Try hex codes
   - Check contrast
3. No Maps Generated
   - Verify Family and Genus selections
   - Check that species exist for selected taxa
   - Ensure data contains valid records 