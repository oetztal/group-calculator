# Group Calculator

Calculate group stage results from simple text input files.

## Installation

```bash
# From source
pip install -e .

# Or install directly
pip install .
```

## Usage

### Process a single group file

```bash
python -m group_calculator.cli group_A.txt
```

### Process all group files in current directory

```bash
python -m group_calculator.cli --all
```

### Save output to file

```bash
python -m group_calculator.cli group_A.txt --output results.json
```

## Input Format

Create text files named `group_<letter>.txt` with one match per line:

```
Mexico<TAB>Haiti<TAB>4:3
Brazil<TAB>Sweden<TAB>1:1
Mexico<TAB>Brazil<TAB>2:1
Mexico<TAB>Sweden<TAB>0:0
Haiti<TAB>Brazil<TAB>1:4
Haiti<TAB>Sweden<TAB>2:3
```

- Tab-separated values (use actual tab character, not spaces)
- Team names can contain spaces (e.g., "Costa Rica", "United States")
- Score format: `goals_a:goals_b`
- Empty lines and lines starting with `#` are ignored

## Output Format

JSON output with the following structure:

```json
{
  "group_A": {
    "teams": [
      {
        "name": "Brazil",
        "matches": 3,
        "wins": 2,
        "draws": 1,
        "losses": 0,
        "points": 7,
        "goal_difference": 3,
        "goals_for": 6,
        "goals_against": 3
      }
    ],
    "is_valid": true,
    "messages": []
  }
}
```

## Validation

The system validates:
- Exactly 4 unique teams per group
- Exactly 6 matches (all pairs must play once)
- No duplicate matches
- No team plays itself
- Score format is valid

If validation fails, `is_valid` will be `false` and `messages` will contain error descriptions. The exit code will be non-zero.

## Team Sorting

Teams are sorted by:
1. Points (descending)
2. Goal difference (descending)
3. Team name (ascending, alphabetical)
