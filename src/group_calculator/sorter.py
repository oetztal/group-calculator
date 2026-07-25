"""Sort teams according to ranking rules."""

from group_calculator.models import TeamStats


def sort_teams(team_stats: list[TeamStats]) -> list[TeamStats]:
    """Sort teams by World Cup ranking criteria.

    Args:
        team_stats: List of TeamStats objects

    Returns:
        New list of TeamStats sorted by:
        1. Points (descending)
        2. Goal difference (descending)
        3. Team name (ascending, alphabetical)
    """
    return sorted(team_stats, key=lambda t: (-t.points, -t.goal_difference, t.name))
