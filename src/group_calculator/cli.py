"""Command-line interface for Group Calculator."""

import argparse
import glob
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from group_calculator.parser import parse_file
from group_calculator.validator import validate_group
from group_calculator.calculator import calculate_stats
from group_calculator.sorter import sort_teams
from group_calculator.formatter import format_group_result, format_to_json, format_all_groups


def process_group_file(filepath: str) -> Dict[str, Any]:
    """Process a single group file and return formatted results.
    
    Args:
        filepath: Path to the group file
        
    Returns:
        Dictionary with group name as key and result data as value
    """
    # Get group name from filename
    path_obj = Path(filepath)
    group_name = path_obj.stem  # e.g., "group_A" from "group_A.txt"
    
    # Parse file
    matches, parse_errors = parse_file(filepath)
    all_errors = list(parse_errors)
    
    # Validate group
    is_valid, validation_errors = validate_group(matches)
    all_errors.extend(validation_errors)
    
    # Calculate stats (even if invalid, for partial output)
    stats = calculate_stats(matches)
    sorted_teams = sort_teams(list(stats.values()))
    
    # Format result
    return format_group_result(
        group_name=group_name,
        sorted_teams=sorted_teams,
        is_valid=is_valid and len(parse_errors) == 0,
        messages=all_errors
    )


def process_all_groups(directory: str = ".") -> List[Dict[str, Any]]:
    """Process all group_*.txt files in a directory.
    
    Args:
        directory: Directory to search for group files
        
    Returns:
        List of formatted group result dictionaries
    """
    pattern = Path(directory) / "group_*.txt"
    group_files = glob.glob(str(pattern))
    
    if not group_files:
        print(f"No group_*.txt files found in {directory}", file=sys.stderr)
        return []
    
    results = []
    for filepath in sorted(group_files):
        result = process_group_file(filepath)
        results.append(result)
    
    return results


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point.
    
    Args:
        argv: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, 1 for validation errors)
    """
    parser = argparse.ArgumentParser(
        description="Calculate group stage results from text files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s group_A.txt                         Process single file
  %(prog)s group_A.txt -o results.json        Save output to file
  %(prog)s --all                              Process all group_*.txt files
  %(prog)s --all -o all_results.json         Save all results to file
"""
    )
    
    parser.add_argument(
        "group_file",
        nargs="?",
        help="Path to a group file (e.g., group_A.txt)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all group_*.txt files in current directory"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output JSON file path (default: stdout)"
    )
    
    args = parser.parse_args(argv)
    
    # Determine what to process
    results: List[Dict[str, Any]] = []
    if args.all:
        if args.group_file:
            print("Error: Cannot specify both --all and a group file.", file=sys.stderr)
            return 1
        
        results = process_all_groups()
        if not results:
            return 1
        
        combined = format_all_groups(results)
        
    elif args.group_file:
        if not Path(args.group_file).exists():
            print(f"Error: File not found: {args.group_file}", file=sys.stderr)
            return 1
        
        result = process_group_file(args.group_file)
        combined = result
        
    else:
        print("Error: Specify a group file or use --all", file=sys.stderr)
        parser.print_help()
        return 1
    
    # Output
    json_output = format_to_json(combined, indent=2)
    
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"Results written to {args.output}")
        except Exception as e:
            print(f"Error writing to {args.output}: {e}", file=sys.stderr)
            return 1
    else:
        print(json_output)
    
    # Check for validation errors
    all_messages = []
    if args.all:
        for r in results:
            for group_name, group_data in r.items():
                if not group_data.get("is_valid", True):
                    all_messages.extend(group_data.get("messages", []))
    else:
        for group_name, group_data in combined.items():
            if not group_data.get("is_valid", True):
                all_messages.extend(group_data.get("messages", []))
    
    if all_messages:
        print("\nValidation errors:", file=sys.stderr)
        for msg in all_messages:
            print(f"  - {msg}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
