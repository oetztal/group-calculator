"""Validate group structure and match integrity."""

from typing import List, Tuple, Set

from wc_calculator.models import Match


def validate_group(matches: List[Match]) -> Tuple[bool, List[str]]:
    """Validate that a group has the correct structure.
    
    Args:
        matches: List of Match objects for the group
        
    Returns:
        Tuple of (is_valid, list of error messages)
        
    Validation rules:
    1. Exactly 4 unique teams
    2. Exactly 6 matches (for 4 teams)
    3. No team plays itself
    4. No duplicate matches (same pair of teams)
    5. All expected pairs are present
    """
    errors = []
    
    # Collect all unique team names
    all_teams = set()
    for m in matches:
        all_teams.add(m.team_a)
        all_teams.add(m.team_b)
    
    num_teams = len(all_teams)
    num_matches = len(matches)
    
    # Rule 1: Exactly 4 unique teams
    if num_teams != 4:
        errors.append(f"Expected 4 teams, found {num_teams}: {sorted(all_teams)}")
    
    # Rule 2: Exactly 6 matches (only check if we have 4 teams)
    if num_teams == 4 and num_matches != 6:
        errors.append(f"Expected 6 matches for 4 teams, found {num_matches}")
    
    # Rule 3: No team plays itself
    for m in matches:
        if m.team_a == m.team_b:
            errors.append(f"Team cannot play itself: {m.team_a}")
    
    # Rule 4: No duplicate matches
    # Track pairs as sorted tuples to catch duplicates regardless of order
    played_pairs = set()
    for m in matches:
        pair = tuple(sorted([m.team_a, m.team_b]))
        if pair in played_pairs:
            errors.append(f"Duplicate match: {m.team_a} vs {m.team_b}")
        played_pairs.add(pair)
    
    # Rule 5: All expected pairs present (only if we have 4 teams)
    if num_teams == 4:
        teams_list = sorted(all_teams)
        expected_pairs = set()
        for i in range(4):
            for j in range(i + 1, 4):
                expected_pairs.add((teams_list[i], teams_list[j]))
        
        missing_pairs = expected_pairs - played_pairs
        if missing_pairs:
            missing_str = ", ".join(f"{a} vs {b}" for a, b in sorted(missing_pairs))
            errors.append(f"Missing matches: {missing_str}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def get_expected_pairs(teams: Set[str]) -> Set[Tuple[str, str]]:
    """Get all expected pairings for a set of teams.
    
    Args:
        teams: Set of team names
        
    Returns:
        Set of tuples representing all unique pairings
    """
    teams_list = sorted(teams)
    expected = set()
    for i in range(len(teams_list)):
        for j in range(i + 1, len(teams_list)):
            expected.add((teams_list[i], teams_list[j]))
    return expected
