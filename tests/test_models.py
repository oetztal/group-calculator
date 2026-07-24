"""Tests for data models."""

import pytest

from wc_calculator.models import Match, TeamStats


class TestMatch:
    """Tests for Match dataclass."""

    def test_create_valid_match(self):
        """Test creating a valid match."""
        match = Match(team_a="Mexico", team_b="Haiti", score_a=4, score_b=3)
        assert match.team_a == "Mexico"
        assert match.team_b == "Haiti"
        assert match.score_a == 4
        assert match.score_b == 3

    def test_create_match_with_zero_scores(self):
        """Test creating a match with zero scores."""
        match = Match(team_a="Brazil", team_b="Sweden", score_a=0, score_b=0)
        assert match.score_a == 0
        assert match.score_b == 0

    def test_match_is_immutable(self):
        """Test that Match is immutable (frozen)."""
        match = Match(team_a="A", team_b="B", score_a=1, score_b=0)
        with pytest.raises(AttributeError):
            match.team_a = "C"

    def test_create_match_with_empty_team_raises(self):
        """Test that empty team name raises ValueError."""
        with pytest.raises(ValueError, match="Team names cannot be empty"):
            Match(team_a="", team_b="Haiti", score_a=1, score_b=0)

    def test_create_match_with_negative_score_raises(self):
        """Test that negative score raises ValueError."""
        with pytest.raises(ValueError, match="Scores cannot be negative"):
            Match(team_a="Mexico", team_b="Haiti", score_a=-1, score_b=0)


class TestTeamStats:
    """Tests for TeamStats dataclass."""

    def test_create_team_stats(self):
        """Test creating TeamStats with defaults."""
        stats = TeamStats(name="Mexico")
        assert stats.name == "Mexico"
        assert stats.matches == 0
        assert stats.wins == 0
        assert stats.draws == 0
        assert stats.losses == 0
        assert stats.points == 0
        assert stats.goals_for == 0
        assert stats.goals_against == 0
        assert stats.goal_difference == 0

    def test_create_team_stats_with_values(self):
        """Test creating TeamStats with initial values."""
        stats = TeamStats(
            name="Brazil",
            matches=3,
            wins=2,
            draws=1,
            losses=0,
            points=7,
            goals_for=6,
            goals_against=3
        )
        assert stats.matches == 3
        assert stats.wins == 2
        assert stats.draws == 1
        assert stats.losses == 0
        assert stats.points == 7
        assert stats.goals_for == 6
        assert stats.goals_against == 3
        assert stats.goal_difference == 3

    def test_update_win(self):
        """Test updating stats for a win."""
        stats = TeamStats(name="Mexico")
        stats.update(goals_scored=2, goals_conceded=1, result="win")
        
        assert stats.matches == 1
        assert stats.wins == 1
        assert stats.draws == 0
        assert stats.losses == 0
        assert stats.points == 3
        assert stats.goals_for == 2
        assert stats.goals_against == 1
        assert stats.goal_difference == 1

    def test_update_draw(self):
        """Test updating stats for a draw."""
        stats = TeamStats(name="Sweden")
        stats.update(goals_scored=1, goals_conceded=1, result="draw")
        
        assert stats.matches == 1
        assert stats.wins == 0
        assert stats.draws == 1
        assert stats.losses == 0
        assert stats.points == 1
        assert stats.goals_for == 1
        assert stats.goals_against == 1
        assert stats.goal_difference == 0

    def test_update_loss(self):
        """Test updating stats for a loss."""
        stats = TeamStats(name="Haiti")
        stats.update(goals_scored=1, goals_conceded=3, result="loss")
        
        assert stats.matches == 1
        assert stats.wins == 0
        assert stats.draws == 0
        assert stats.losses == 1
        assert stats.points == 0
        assert stats.goals_for == 1
        assert stats.goals_against == 3
        assert stats.goal_difference == -2

    def test_update_multiple_matches(self):
        """Test updating stats across multiple matches."""
        stats = TeamStats(name="Mexico")
        
        # Win 2:1
        stats.update(goals_scored=2, goals_conceded=1, result="win")
        # Draw 0:0
        stats.update(goals_scored=0, goals_conceded=0, result="draw")
        # Loss 1:3
        stats.update(goals_scored=1, goals_conceded=3, result="loss")
        
        assert stats.matches == 3
        assert stats.wins == 1
        assert stats.draws == 1
        assert stats.losses == 1
        assert stats.points == 4
        assert stats.goals_for == 3
        assert stats.goals_against == 4
        assert stats.goal_difference == -1

    def test_update_invalid_result_raises(self):
        """Test that invalid result raises ValueError."""
        stats = TeamStats(name="Mexico")
        with pytest.raises(ValueError, match="Unknown result"):
            stats.update(goals_scored=1, goals_conceded=0, result="unknown")
