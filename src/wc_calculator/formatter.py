"""Format group results as JSON."""

import json
from typing import Dict, List, Any

from wc_calculator.models import TeamStats


def format_group_result(
    group_name: str,
    sorted_teams: List[TeamStats],
    is_valid: bool,
    messages: List[str]
) -> Dict[str, Any]:
    """Format group results into JSON-serializable dictionary.
    
    Args:
        group_name: Name of the group (e.g., "group_A")
        sorted_teams: List of TeamStats sorted by ranking
        is_valid: Whether the group passed validation
        messages: List of validation error messages
        
    Returns:
        Dictionary with structure:
        {
            group_name: {
                "teams": [
                    {
                        "name": str,
                        "matches": int,
                        "wins": int,
                        "draws": int,
                        "losses": int,
                        "points": int,
                        "goal_difference": int,
                        "goals_for": int,
                        "goals_against": int
                    },
                    ...
                ],
                "is_valid": bool,
                "messages": List[str]
            }
        }
    """
    teams_data = []
    for team in sorted_teams:
        teams_data.append({
            "name": team.name,
            "matches": team.matches,
            "wins": team.wins,
            "draws": team.draws,
            "losses": team.losses,
            "points": team.points,
            "goal_difference": team.goal_difference,
            "goals_for": team.goals_for,
            "goals_against": team.goals_against
        })
    
    return {
        group_name: {
            "teams": teams_data,
            "is_valid": is_valid,
            "messages": messages
        }
    }


def format_to_json(
    group_results: Dict[str, Any],
    indent: int = 2
) -> str:
    """Convert group results dictionary to JSON string.
    
    Args:
        group_results: Dictionary from format_group_result
        indent: JSON indentation level
        
    Returns:
        JSON string
    """
    return json.dumps(group_results, indent=indent, ensure_ascii=False)


def format_all_groups(
    all_group_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Combine multiple group results into a single dictionary.
    
    Args:
        all_group_results: List of group result dictionaries
        
    Returns:
        Combined dictionary with all groups
    """
    result = {}
    for group_result in all_group_results:
        result.update(group_result)
    return result
