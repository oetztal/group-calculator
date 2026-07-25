"""Calculate team statistics from match data."""

from group_calculator.models import Match, TeamStats


def calculate_stats(matches: list[Match]) -> dict[str, TeamStats]:
    """Calculate statistics for all teams based on match results.

    Args:
        matches: List of Match objects

    Returns:
        Dictionary mapping team names to TeamStats objects
    """
    stats: dict[str, TeamStats] = {}

    for m in matches:
        # Initialize team stats if not present
        for team_name in [m.team_a, m.team_b]:
            if team_name not in stats:
                stats[team_name] = TeamStats(name=team_name)

        # Update both teams' statistics
        team_a_stats = stats[m.team_a]
        team_b_stats = stats[m.team_b]

        # Update match count
        team_a_stats.matches += 1
        team_b_stats.matches += 1

        # Update goals
        team_a_stats.goals_for += m.score_a
        team_a_stats.goals_against += m.score_b
        team_b_stats.goals_for += m.score_b
        team_b_stats.goals_against += m.score_a

        # Update results
        if m.score_a > m.score_b:
            # team_a wins
            team_a_stats.wins += 1
            team_a_stats.points += 3
            team_b_stats.losses += 1
        elif m.score_a < m.score_b:
            # team_b wins
            team_b_stats.wins += 1
            team_b_stats.points += 3
            team_a_stats.losses += 1
        else:
            # draw
            team_a_stats.draws += 1
            team_a_stats.points += 1
            team_b_stats.draws += 1
            team_b_stats.points += 1

    # Recalculate goal differences (in case goals were updated after init)
    for team_stats in stats.values():
        team_stats.goal_difference = team_stats.goals_for - team_stats.goals_against

    return stats


def update_team_stats(
    team_stats: TeamStats, goals_scored: int, goals_conceded: int, result: str
) -> None:
    """Update a single team's statistics.

    Args:
        team_stats: TeamStats object to update
        goals_scored: Goals scored by this team
        goals_conceded: Goals conceded by this team
        result: One of 'win', 'draw', or 'loss'
    """
    team_stats.update(goals_scored, goals_conceded, result)
