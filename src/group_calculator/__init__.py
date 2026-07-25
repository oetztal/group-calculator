"""Group Calculator - Core module."""

from group_calculator.models import Match, TeamStats
from group_calculator.parser import parse_file
from group_calculator.validator import validate_group
from group_calculator.calculator import calculate_stats
from group_calculator.sorter import sort_teams
from group_calculator.formatter import format_group_result

__all__ = [
    "Match",
    "TeamStats", 
    "parse_file",
    "validate_group",
    "calculate_stats",
    "sort_teams",
    "format_group_result",
]

__version__ = "0.1.0"
