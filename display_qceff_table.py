
#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Script to read and pretty print QCEFF table information 
"""

import csv
import sys
from typing import Dict, List, Any


def read_qceff_table(filename: str) -> Dict[str, Any]:
    """
    Read the QCEFF table CSV file and parse its contents.
    
    Args:
        filename: Path to the CSV file
        
    Returns:
        Dictionary containing parsed table data
    """
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Header
    version_info = rows[0][0]  # "QCEFF table version: X"
    
    # column headers 1 in qceff table v1
    headers = rows[1]
    
    # data rows
    data_rows = rows[2:]
    
    return {
        'version': version_info,
        'headers': headers,
        'data': data_rows
    }


def display_quantity_info(qty_name: str, row: List[str]) -> None:
    """
    Display information for a single quantity in a nicely formatted way.
    
    Args:
        qty_name: Name of the quantity
        row: Row data from CSV
    """
    print(f"\n{'='*80}")
    print(f"QUANTITY: {qty_name}")
    print(f"{'='*80}")
    
    # obs_error_info
    print(f"\nOBS ERROR INFO:")
    print(f"  Bounded Below: {row[1]}")
    print(f"  Bounded Above: {row[2]}")
    print(f"  Lower Bound:   {row[3]}")
    print(f"  Upper Bound:   {row[4]}")

    # probit_inflation
    print(f"\nPROBIT INFLATION:")
    print(f"  Dist Type:     {row[5]}")
    print(f"  Bounded Below: {row[6]}")
    print(f"  Bounded Above: {row[7]}")
    print(f"  Lower Bound:   {row[8]}")
    print(f"  Upper Bound:   {row[9]}")

    # probit_state
    print(f"\nPROBIT STATE:")
    print(f"  Dist Type:     {row[10]}")
    print(f"  Bounded Below: {row[11]}")
    print(f"  Bounded Above: {row[12]}")
    print(f"  Lower Bound:   {row[13]}")
    print(f"  Upper Bound:   {row[14]}")

    # probit_extended_state
    print(f"\nPROBIT EXTENDED STATE:")
    print(f"  Dist Type:     {row[15]}")
    print(f"  Bounded Below: {row[16]}")
    print(f"  Bounded Above: {row[17]}")
    print(f"  Lower Bound:   {row[18]}")
    print(f"  Upper Bound:   {row[19]}")

    # obs_inc_info
    print(f"\nOBS INC INFO:")
    print(f"  Filter Kind:   {row[20]}")
    print(f"  Bounded Below: {row[21]}")
    print(f"  Bounded Above: {row[22]}")
    print(f"  Lower Bound:   {row[23]}")
    print(f"  Upper Bound:   {row[24]}")


def display_summary_table(data: List[List[str]]) -> None:
    """
    Display a summary table of all quantities.
    
    Args:
        data: List of data rows from CSV
    """
    print(f"\n{'='*144}")
    print("SUMMARY TABLE")
    print(f"{'='*144}")
    
    # Header
    print(f"{'QUANTITY':<30} {'PROBIT_INFL':<30} {'PROBIT_STATE':<30} {'PROBIT_EXT':<30} {'OBS_INC_INFO':<20}")
    print(f"{'-'*30} {'-'*30} {'-'*30} {'-'*30} {'-'*20}")

    def format_dist(dist, bounded_below, bounded_above, lower, upper):
        # Shorten BOUNDED_NORMAL_RH_DISTRIBUTION
        dist = dist.replace('BOUNDED_NORMAL_RH_DISTRIBUTION', 'BNRH_DISTRIBUTION')
        # Truncate long names
        dist_short = dist[:18] + '..' if len(dist) > 20 else dist
        # If normal_distribution, do not show bounds
        if dist.strip().upper() == 'NORMAL_DISTRIBUTION':
            return dist_short
        # Format bounds
        if bounded_below.strip().upper() == 'TRUE' or bounded_below.strip() == '.true.':
            left_bracket = '['
        else:
            left_bracket = '('
        if bounded_above.strip().upper() == 'TRUE' or bounded_above.strip() == '.true.':
            right_bracket = ']'
        else:
            right_bracket = ')'
        # Handle inf/-inf
        lower_str = lower.strip()
        upper_str = upper.strip()
        if lower_str == '' or lower_str.lower() == 'none' or lower_str == '-888888':
            lower_str = '-inf'
        if upper_str == '' or upper_str.lower() == 'none' or upper_str == '-888888':
            upper_str = 'inf'
        return f"{dist_short} {left_bracket}{lower_str},{upper_str}{right_bracket}"

    for row in data:
        qty_name = row[0].replace('QTY_', '')
        # Probit inflation
        probit_infl_dist = row[5] if len(row) > 5 else 'N/A'
        probit_infl_below = row[6] if len(row) > 6 else ''
        probit_infl_above = row[7] if len(row) > 7 else ''
        probit_infl_low = row[8] if len(row) > 8 else ''
        probit_infl_up = row[9] if len(row) > 9 else ''
        probit_infl = format_dist(probit_infl_dist, probit_infl_below, probit_infl_above, probit_infl_low, probit_infl_up)

        # Probit state
        probit_state_dist = row[10] if len(row) > 10 else 'N/A'
        probit_state_below = row[11] if len(row) > 11 else ''
        probit_state_above = row[12] if len(row) > 12 else ''
        probit_state_low = row[13] if len(row) > 13 else ''
        probit_state_up = row[14] if len(row) > 14 else ''
        probit_state = format_dist(probit_state_dist, probit_state_below, probit_state_above, probit_state_low, probit_state_up)

        # Probit extended state
        probit_ext_dist = row[15] if len(row) > 15 else 'N/A'
        probit_ext_below = row[16] if len(row) > 16 else ''
        probit_ext_above = row[17] if len(row) > 17 else ''
        probit_ext_low = row[18] if len(row) > 18 else ''
        probit_ext_up = row[19] if len(row) > 19 else ''
        probit_ext = format_dist(probit_ext_dist, probit_ext_below, probit_ext_above, probit_ext_low, probit_ext_up)

        obs_inc_info = row[20] if len(row) > 20 else 'N/A'
        obs_inc_info = obs_inc_info[:18] + '..' if len(obs_inc_info) > 20 else obs_inc_info

        print(f"{qty_name:<30} {probit_infl:<30} {probit_state:<30} {probit_ext:<30} {obs_inc_info:<20}")


def main():
    """Main function to run the script."""
    import argparse
    parser = argparse.ArgumentParser(description="Display QCEFF table summary and details.")
    parser.add_argument("csv_file", help="Path to QCEFF table CSV file")
    parser.add_argument("--details", action="store_true", help="Print detailed information for each quantity")
    args = parser.parse_args()

    filename = args.csv_file

    try:
        # Read the CSV file
        table_data = read_qceff_table(filename)

        print(f"QCEFF Table Display")
        print(f"File: {filename}")
        print(f"Version: {table_data['version']}")

        # Display summary table first
        display_summary_table(table_data['data'])

        if args.details:
            # Display detailed information for each quantity
            print(f"\n{'='*80}")
            print("DETAILED INFORMATION")
            print(f"{'='*80}")

            for row in table_data['data']:
                qty_name = row[0]
                display_quantity_info(qty_name, row)

            print(f"\n{'='*80}")
            print("END OF REPORT")
            print(f"{'='*80}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
