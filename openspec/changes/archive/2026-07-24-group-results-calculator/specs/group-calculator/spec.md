## ADDED Requirements

### Requirement: Parse tab-separated group match files

The system SHALL parse input files named `group_<letter>.txt` where each line contains tab-separated values: TeamA<TAB>TeamB<TAB>Score (e.g., `Mexico<TAB>Haiti<TAB>4:3`).

#### Scenario: Valid file with spaces in team names
- **WHEN** file contains `Costa Rica<TAB>United States<TAB>2:1`
- **THEN** system correctly identifies team names as "Costa Rica" and "United States" with score 2:1

#### Scenario: Empty lines are skipped
- **WHEN** file contains empty lines
- **THEN** system ignores empty lines and processes only valid match lines

#### Scenario: Comment lines starting with # are ignored
- **WHEN** file contains lines starting with `#`
- **THEN** system skips comment lines

### Requirement: Validate group structure

The system SHALL validate that each group has exactly 4 unique teams and exactly 6 matches (one per each pair of teams).

#### Scenario: Valid group with 4 teams and 6 matches
- **WHEN** file contains exactly 4 teams (A, B, C, D) and all 6 pairings (A-B, A-C, A-D, B-C, B-D, C-D)
- **THEN** system marks group as valid

#### Scenario: Invalid group with 3 teams
- **WHEN** file contains only 3 unique teams
- **THEN** system reports error "Expected 4 teams, found 3"

#### Scenario: Invalid group with 5 teams
- **WHEN** file contains 5 unique teams
- **THEN** system reports error "Expected 4 teams, found 5"

#### Scenario: Missing match between two teams
- **WHEN** file has 4 teams but only 5 matches, missing one pairing
- **THEN** system reports error listing the missing match

#### Scenario: Duplicate match
- **WHEN** file contains same pair of teams twice (e.g., A-B appears twice)
- **THEN** system reports error "Duplicate match: A vs B"

#### Scenario: Team plays itself
- **WHEN** file contains a match where team_a equals team_b
- **THEN** system reports error "Team cannot play itself: <team_name>"

### Requirement: Parse score format x:y

The system SHALL parse scores in format `<goals_a>:<goals_b>` where both values are non-negative integers.

#### Scenario: Standard score format
- **WHEN** score is "4:3"
- **THEN** system parses as team_a goals=4, team_b goals=3

#### Scenario: Zero score
- **WHEN** score is "0:0"
- **THEN** system parses as team_a goals=0, team_b goals=0

#### Scenario: High score
- **WHEN** score is "10:5"
- **THEN** system parses as team_a goals=10, team_b goals=5

### Requirement: Calculate team statistics

The system SHALL calculate for each team: matches played, wins, draws, losses, points, goals for, goals against, and goal difference.

#### Scenario: Win increases points by 3
- **WHEN** team wins a match
- **THEN** team gains 3 points, 1 win, goals_for += goals_scored, goals_against += goals_conceded

#### Scenario: Draw increases points by 1
- **WHEN** team draws a match
- **THEN** team gains 1 point, 1 draw, goals_for += goals_scored, goals_against += goals_conceded

#### Scenario: Loss gives 0 points
- **WHEN** team loses a match
- **THEN** team gains 0 points, 1 loss, goals_for += goals_scored, goals_against += goals_conceded

#### Scenario: Goal difference calculation
- **WHEN** team has goals_for=10 and goals_against=6
- **THEN** goal_difference = 4

#### Scenario: Full tournament statistics
- **WHEN** team plays 3 matches: win 2:1, draw 0:0, loss 1:3
- **THEN** team has matches=3, wins=1, draws=1, losses=1, points=4, goals_for=3, goals_against=4, goal_difference=-1

### Requirement: Sort teams by ranking criteria

The system SHALL sort teams in descending order by: points, then goal difference, then ascending alphabetical order.

#### Scenario: Sort by points descending
- **WHEN** Team A has 7 points, Team B has 4 points
- **THEN** Team A appears before Team B in output

#### Scenario: Sort by goal difference when points equal
- **WHEN** Team A and Team B both have 4 points, but A has GD=+3 and B has GD=+1
- **THEN** Team A appears before Team B in output

#### Scenario: Sort alphabetically when points and GD equal
- **WHEN** Team A and Team B have identical points and goal difference
- **THEN** Team A appears before Team B if A < B alphabetically

### Requirement: Output JSON format

The system SHALL output results as JSON with structure: group name containing teams array with statistics, is_valid boolean, and messages array.

#### Scenario: Valid group output
- **WHEN** group_A.txt is valid
- **THEN** output contains group_A with teams sorted, is_valid=true, messages=[]

#### Scenario: Invalid group output
- **WHEN** group_A.txt has validation errors
- **THEN** output contains group_A with is_valid=false, messages containing all error descriptions

#### Scenario: JSON structure for each team
- **WHEN** team statistics are calculated
- **THEN** each team object contains: name, matches, wins, draws, losses, points, goal_difference, goals_for, goals_against

### Requirement: CLI interface

The system SHALL provide a CLI that accepts a group file path or --all flag to process all group_*.txt files in current directory.

#### Scenario: Process single group file
- **WHEN** user runs `cli.py group_A.txt`
- **THEN** system processes only group_A.txt and outputs JSON result

#### Scenario: Process all group files
- **WHEN** user runs `cli.py --all`
- **THEN** system finds and processes all group_*.txt files in current directory

#### Scenario: Output to file
- **WHEN** user runs `cli.py group_A.txt --output results.json`
- **THEN** system writes JSON output to results.json

#### Scenario: Exit code on validation failure
- **WHEN** group file has validation errors
- **THEN** system exits with non-zero code

### Requirement: Collect all validation errors

The system SHALL collect all validation errors and report them together, not failing on the first error.

#### Scenario: Multiple validation errors
- **WHEN** file has 3 teams AND duplicate matches AND missing pairs
- **THEN** system reports all three error types in messages array

#### Scenario: Partial output with errors
- **WHEN** file has validation errors
- **THEN** system still calculates and outputs statistics, but marks is_valid=false
