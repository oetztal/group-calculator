"""Tests for calculator module."""

from group_calculator.calculator import calculate_stats
from group_calculator.models import Match


class TestCalculateStats:
    """Tests for calculate_stats function."""

    def test_single_win(self):
        """Test calculation for a single win."""
        matches = [Match("A", "B", 2, 1)]
        stats = calculate_stats(matches)

        assert len(stats) == 2

        team_a = stats["A"]
        assert team_a.matches == 1
        assert team_a.wins == 1
        assert team_a.draws == 0
        assert team_a.losses == 0
        assert team_a.points == 3
        assert team_a.goals_for == 2
        assert team_a.goals_against == 1
        assert team_a.goal_difference == 1

        team_b = stats["B"]
        assert team_b.matches == 1
        assert team_b.wins == 0
        assert team_b.draws == 0
        assert team_b.losses == 1
        assert team_b.points == 0
        assert team_b.goals_for == 1
        assert team_b.goals_against == 2
        assert team_b.goal_difference == -1

    def test_single_draw(self):
        """Test calculation for a single draw."""
        matches = [Match("A", "B", 1, 1)]
        stats = calculate_stats(matches)

        team_a = stats["A"]
        assert team_a.matches == 1
        assert team_a.wins == 0
        assert team_a.draws == 1
        assert team_a.losses == 0
        assert team_a.points == 1
        assert team_a.goals_for == 1
        assert team_a.goals_against == 1
        assert team_a.goal_difference == 0

        team_b = stats["B"]
        assert team_b.points == 1
        assert team_b.draws == 1

    def test_full_group(self):
        """Test calculation for a full group of 4 teams."""
        matches = [
            Match("Mexico", "Haiti", 4, 3),
            Match("Mexico", "Brazil", 1, 2),
            Match("Mexico", "Sweden", 0, 0),
            Match("Haiti", "Brazil", 1, 4),
            Match("Haiti", "Sweden", 2, 1),
            Match("Brazil", "Sweden", 3, 3),
        ]

        stats = calculate_stats(matches)

        assert len(stats) == 4

        # Mexico: 3 matches, 2 wins, 1 draw, 0 losses
        mexico = stats["Mexico"]
        assert mexico.matches == 3
        assert mexico.wins == 1  # Only beat Haiti 4:3
        assert mexico.draws == 1  # Drew with Sweden 0:0
        assert mexico.losses == 1  # Lost to Brazil 1:2
        assert mexico.points == 4  # 3 + 1 + 0
        assert mexico.goals_for == 5  # 4 + 1 + 0
        assert mexico.goals_against == 5  # 3 + 2 + 0

        # Brazil: 3 matches, 2 wins, 1 draw
        brazil = stats["Brazil"]
        assert brazil.matches == 3
        assert brazil.wins == 2  # Beat Mexico 2:1, Haiti 4:1
        assert brazil.draws == 1  # Drew with Sweden 3:3
        assert brazil.losses == 0
        assert brazil.points == 7

        # Haiti: 3 matches, 1 win, 0 draws, 2 losses
        # Haiti beat Sweden 2:1, lost to Mexico 3:4 and Brazil 1:4
        haiti = stats["Haiti"]
        assert haiti.matches == 3
        assert haiti.wins == 1
        assert haiti.draws == 0
        assert haiti.losses == 2
        assert haiti.points == 3
        assert haiti.goals_for == 6  # 3 + 1 + 2
        assert haiti.goals_against == 9  # 4 + 4 + 1

        # Sweden: 3 matches, 0 wins, 2 draws, 1 loss
        # Sweden drew with Mexico 0:0 and Brazil 3:3, lost to Haiti 1:2
        sweden = stats["Sweden"]
        assert sweden.matches == 3
        assert sweden.wins == 0
        assert sweden.draws == 2
        assert sweden.losses == 1
        assert sweden.points == 2
        assert sweden.goals_for == 4  # 0 + 3 + 1
        assert sweden.goals_against == 5  # 0 + 3 + 2

    def test_goals_accumulate_correctly(self):
        """Test that goals accumulate correctly across multiple matches."""
        matches = [
            Match("A", "B", 2, 1),
            Match("A", "C", 3, 0),
        ]

        stats = calculate_stats(matches)

        team_a = stats["A"]
        assert team_a.goals_for == 5  # 2 + 3
        assert team_a.goals_against == 1  # 1 + 0
        assert team_a.goal_difference == 4
