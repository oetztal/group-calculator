## Why

Create a Python CLI tool to calculate and display World Cup group stage results from simple text input files. This enables quick analysis of fictional soccer championship scenarios without manual calculation.

## What Changes

- New Python CLI project `group_calculator`
- New command-line interface to process `group_<letter>.txt` files
- New JSON output format for group standings
- New validation logic for group integrity
- New calculation engine for team statistics

## Capabilities

### New Capabilities
- `group-calculator`: Parse group match files, validate structure, calculate team statistics (matches, wins, draws, losses, points, goal difference, goals for/against), and output sorted JSON standings

### Modified Capabilities

## Impact

- New directory: `group_calculator/` with Python package structure
- New test suite for validation, parsing, and calculation logic
- New example fixture files for testing
