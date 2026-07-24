## Context

This is a new Python CLI project for calculating World Cup group stage results. No existing codebase exists for this functionality. The project will be self-contained with a modular architecture to allow for easy testing and potential future extensions.

## Goals / Non-Goals

**Goals:**
- Create a modular, testable CLI application
- Support tab-separated input files with team names containing spaces
- Validate group structure (4 teams, 6 matches, all pairs present)
- Calculate accurate team statistics (matches, wins, draws, losses, points, goal difference, goals for/against)
- Sort teams by standard World Cup tiebreaker rules (points, GD, alphabetical)
- Output clean JSON for consumption by other tools
- Collect all validation errors before reporting

**Non-Goals:**
- Support for other sports or competition formats
- Database persistence
- Web interface or API
- Real-time data fetching
- Streaming processing for large files (not needed for small group files)
- Fair play tiebreaker (not available in input data)

## Decisions

### Modular Architecture

**Decision**: Split into separate modules (parser, validator, calculator, sorter, formatter)

**Rationale**: Each component has a single responsibility, making the code easier to test, maintain, and extend. This follows the principle of separation of concerns.

**Alternatives considered**: Single monolithic script. Rejected because it would be harder to test individual components and would become unwieldy as features grow.

### Tab-Separated Input Format

**Decision**: Use tab character as delimiter between team names and score

**Rationale**: Tab characters are unlikely to appear in team names, allowing team names with spaces (e.g., "Costa Rica", "United States"). This is simpler than escaping or quoting.

**Alternatives considered**: CSV with quoting, space-separated with escaping. Rejected as more complex for the user and for parsing.

### Validation Error Collection

**Decision**: Collect all validation errors and report them together

**Rationale**: Users want to see all issues at once rather than fixing one error at a time. This provides better user experience.

**Alternatives considered**: Fail-fast on first error. Rejected as less user-friendly.

### Tiebreaker Order

**Decision**: Points (desc) → Goal Difference (desc) → Team Name (asc, alphabetical)

**Rationale**: Matches standard World Cup rules. Alphabetical sorting is used as the final tiebreaker since fair play data is not available in the input.

**Alternatives considered**: Include goals for as additional tiebreaker. Rejected as not requested by user and adds complexity.

### Data Classes for Type Safety

**Decision**: Use Python dataclasses for Match and TeamStats

**Rationale**: Provides type hints, better code readability, and easier testing. Dataclasses reduce boilerplate for simple data containers.

**Alternatives considered**: Plain dictionaries, namedtuples. Rejected as less maintainable and less type-safe.

### JSON Output Format

**Decision**: Output structured JSON with teams array, is_valid flag, and messages array

**Rationale**: JSON is widely supported, machine-readable, and easy to parse. Including is_valid and messages allows consumers to handle validation failures gracefully.

**Alternatives considered**: Plain text table, CSV. Rejected as less structured and harder for programmatic consumption.

### CLI Argument Parsing

**Decision**: Use argparse for CLI argument handling

**Rationale**: Standard library, no external dependencies, well-documented, handles --help automatically.

**Alternatives considered**: click, typer. Rejected as they would add external dependencies for a simple use case.

## Component Data Flow

```
                    ┌─────────────┐
        group_A.txt │             │
   ┌───────────────┤   Parser    ├──┐
   │               │             │  │
   ▼               └──────┬──────┘  ▼
┌─────────┐              │        ┌─────────┐
│ Match   │              │        │ Match   │
│ objects │              │        │ objects │
└─────────┘              ▼        └─────────┘
                 ┌─────────────────┐
                 │   Validator      │
                 │   (check 4 teams,│
                 │    6 matches,    │
                 │    all pairs)    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   Calculator     │
                 │   (accumulate    │
                 │    per-team     │
                 │    statistics)   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │     Sorter       │
                 │   (by points →   │
                 │    GD → name)    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │    Formatter     │
                 │   (to JSON)      │
                 └─────────────────┘
```

## File Structure

```
worldcup_group_calculator/
├── pyproject.toml
├── README.md
├── src/
│   └── wc_calculator/
│       ├── __init__.py
│       ├── models.py           # Match, TeamStats dataclasses
│       ├── parser.py           # File parsing logic
│       ├── validator.py        # Group validation
│       ├── calculator.py       # Statistics calculation
│       ├── sorter.py           # Team ranking logic
│       └── cli.py              # CLI entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_parser.py
│   ├── test_validator.py
│   ├── test_calculator.py
│   └── fixtures/
│       ├── group_A_valid.txt
│       ├── group_B_invalid_teams.txt
│       └── group_C_missing_matches.txt
└── examples/
    ├── group_A.txt
    └── group_B.txt
```

## Risks / Trade-offs

**[Risk] Team name edge cases** → Team names could theoretically contain tab characters, though this is extremely unlikely in practice. **Mitigation**: Document this limitation. If encountered, user must escape or use alternative delimiter.

**[Risk] Performance with many groups** → Processing many group files simultaneously could be slow. **Mitigation**: Not a concern for typical use case (few groups). If needed, can add parallel processing later.

**[Risk] Score format variations** → Users might use hyphen (-) instead of colon (:) in scores. **Mitigation**: Document required format. Could add flexible parsing in future.

**[Risk] Floating point precision** → Goal difference calculations use integers, so no precision issues. **Mitigation**: N/A - using integer arithmetic.

## Migration Plan

Not applicable for new project. Simply create the new directory structure and implement.

## Open Questions

- Should we support processing a directory of group files recursively, or just the current directory? **Current decision**: Current directory only via --all flag.
- Should we add a --pretty flag for formatted JSON output? **Current decision**: Use standard json.dumps with indent=2 by default.
- Should we include a --quiet flag to suppress stderr output? **Current decision**: Not implemented, can add later if needed.
