## 1. Project Setup

- [x] 1.1 Create project directory structure (src/group_calculator, tests, examples)
- [x] 1.2 Create pyproject.toml with project metadata and dependencies
- [x] 1.3 Create README.md with usage instructions
- [x] 1.4 Set up test framework (pytest)

## 2. Core Models

- [x] 2.1 Create models.py with Match dataclass (team_a, team_b, score_a, score_b)
- [x] 2.2 Create TeamStats dataclass (name, matches, wins, draws, losses, points, goals_for, goals_against, goal_difference)

## 3. Parser Module

- [x] 3.1 Implement parse_file() function to read and parse group_*.txt files
- [x] 3.2 Handle tab-separated format (TeamA<TAB>TeamB<TAB>Score)
- [x] 3.3 Parse score in x:y format into integers
- [x] 3.4 Skip empty lines and comment lines (starting with #)
- [x] 3.5 Handle parsing errors gracefully
- [x] 3.6 Create test fixtures (valid group, invalid formats)
- [x] 3.7 Write unit tests for parser module

## 4. Validator Module

- [x] 4.1 Implement validate_group() function to check group structure
- [x] 4.2 Validate exactly 4 unique teams
- [x] 4.3 Validate exactly 6 matches
- [x] 4.4 Check no team plays itself
- [x] 4.5 Check no duplicate matches
- [x] 4.6 Check all expected pairs are present
- [x] 4.7 Collect all validation errors (not fail-fast)
- [x] 4.8 Write unit tests for validator module

## 5. Calculator Module

- [x] 5.1 Implement calculate_stats() function to compute team statistics
- [x] 5.2 For each match, update both teams' statistics
- [x] 5.3 Calculate matches played count
- [x] 5.4 Calculate wins, draws, losses
- [x] 5.5 Calculate points (3 for win, 1 for draw, 0 for loss)
- [x] 5.6 Calculate goals_for and goals_against
- [x] 5.7 Calculate goal_difference (goals_for - goals_against)
- [x] 5.8 Write unit tests for calculator module

## 6. Sorter Module

- [x] 6.1 Implement sort_teams() function
- [x] 6.2 Sort by points descending
- [x] 6.3 Sort by goal_difference descending (when points equal)
- [x] 6.4 Sort by team name ascending (when points and GD equal)
- [x] 6.5 Write unit tests for sorter module

## 7. Formatter Module

- [x] 7.1 Implement format_group_result() function
- [x] 7.2 Create JSON structure with group name as key
- [x] 7.3 Include teams array with all statistics
- [x] 7.4 Include is_valid boolean
- [x] 7.5 Include messages array with validation errors
- [x] 7.6 Write unit tests for formatter module

## 8. CLI Interface

- [x] 8.1 Implement cli.py with argparse
- [x] 8.2 Add argument for single group file path
- [x] 8.3 Add --all flag to process all group_*.txt files
- [x] 8.4 Add --output/-o flag for output file path
- [x] 8.5 Wire up parser → validator → calculator → sorter → formatter pipeline
- [x] 8.6 Exit with code 1 if any validation errors
- [x] 8.7 Print validation errors to stderr
- [x] 8.8 Default output to stdout if no --output specified
- [x] 8.9 Write integration tests for CLI

## 9. Test Fixtures

- [x] 9.1 Create group_A_valid.txt with 4 teams and all 6 matches
- [x] 9.2 Create group_B_invalid_teams.txt with wrong number of teams
- [x] 9.3 Create group_C_missing_matches.txt with incomplete pairings
- [x] 9.4 Create group_D_duplicate_matches.txt with duplicate entries
- [x] 9.5 Create group_E_self_match.txt with a team playing itself

## 10. Example Files

- [x] 10.1 Create examples/group_A.txt with realistic World Cup group data
- [x] 10.2 Create examples/group_B.txt with another example group

## 11. Final Integration

- [x] 11.1 Run all tests and verify they pass
- [x] 11.2 Test CLI with example files
- [x] 11.3 Test CLI with invalid files
- [x] 11.4 Test --all flag with multiple group files
- [x] 11.5 Verify JSON output format matches specification
- [x] 11.6 Verify exit codes (0 for success, 1 for validation errors)
