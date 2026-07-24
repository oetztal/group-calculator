"""World Cup Group Calculator - Core module."""

from wc_calculator.models import Match, TeamStats
from wc_calculator.parser import parse_file
from wc_calculator.validator import validate_group
from wc_calculator.calculator import calculate_stats
from wc_calculator.sorter import sort_teams
from wc_calculator.formatter import format_group_result

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
