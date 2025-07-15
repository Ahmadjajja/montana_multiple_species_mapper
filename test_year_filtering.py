#!/usr/bin/env python3
"""
Test script for year-based color filtering logic
"""

import pandas as pd
import numpy as np

def test_year_based_color_logic():
    """Test the year-based color logic with sample data"""
    
    # Create sample data
    data = {
        'county': ['missoula', 'missoula', 'gallatin', 'gallatin', 'lewis and clark', 'flathead'],
        'year': [2010, 2015, 2012, 2018, 2008, np.nan],
        'species': ['rufa'] * 6
    }
    
    df = pd.DataFrame(data)
    print("Sample data:")
    print(df)
    print()
    
    # Test scenarios
    scenarios = [
        {
            'name': 'No year split (single color)',
            'split_year': '',
            'pre_color': 'green',
            'post_color': 'red', 
            'single_color': 'grey'
        },
        {
            'name': 'Year split at 2014',
            'split_year': '2014',
            'pre_color': 'green',
            'post_color': 'red',
            'single_color': 'grey'
        },
        {
            'name': 'Year split at 2010',
            'split_year': '2010', 
            'pre_color': 'blue',
            'post_color': 'orange',
            'single_color': 'grey'
        }
    ]
    
    for scenario in scenarios:
        print(f"=== {scenario['name']} ===")
        split_year_str = scenario['split_year']
        
        if not split_year_str:
            print("Result: All counties use single color")
            for county in df['county'].unique():
                print(f"  {county}: {scenario['single_color']}")
        else:
            try:
                split_year = int(split_year_str)
                print(f"Split year: {split_year}")
                
                for county in df['county'].unique():
                    county_records = df[df['county'] == county]
                    has_post_year = False
                    has_pre_year = False
                    
                    for _, record in county_records.iterrows():
                        record_year = record.get('year')
                        if record_year is not None and not pd.isna(record_year):
                            try:
                                record_year_int = int(record_year)
                                if record_year_int > split_year:
                                    has_post_year = True
                                else:
                                    has_pre_year = True
                            except (ValueError, TypeError):
                                pass
                    
                    # Determine color
                    if has_post_year:
                        color = scenario['post_color']
                    elif has_pre_year:
                        color = scenario['pre_color']
                    else:
                        color = scenario['single_color']
                    
                    print(f"  {county}: {color}")
                    
            except ValueError:
                print("Invalid split year - using single color")
                for county in df['county'].unique():
                    print(f"  {county}: {scenario['single_color']}")
        
        print()

def test_legend_generation():
    """Test legend text generation"""
    
    scenarios = [
        {'split_year': '', 'single_color': 'grey'},
        {'split_year': '2014', 'pre_color': 'green', 'post_color': 'red'},
        {'split_year': 'invalid', 'single_color': 'grey'}
    ]
    
    print("=== Legend Generation Tests ===")
    
    for scenario in scenarios:
        split_year_str = scenario['split_year']
        
        if not split_year_str:
            legend = f"Color Used: {scenario['single_color'].title()}"
        else:
            try:
                split_year = int(split_year_str)
                legend = f"Before or equal to {split_year} → {scenario['pre_color'].title()}\nAfter {split_year} → {scenario['post_color'].title()}"
            except ValueError:
                legend = f"Color Used: {scenario['single_color'].title()}"
        
        print(f"Split year: '{split_year_str}'")
        print(f"Legend: {legend}")
        print()

if __name__ == "__main__":
    print("Testing Year-Based Color Filtering Logic")
    print("=" * 50)
    print()
    
    test_year_based_color_logic()
    test_legend_generation()
    
    print("Tests completed!") 