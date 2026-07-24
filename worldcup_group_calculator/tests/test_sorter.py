"""Tests for sorter module."""

import pytest

from wc_calculator.models import TeamStats
from wc_calculator.sorter import sort_teams


class TestSortTeams:
    """Tests for sort_teams function."""

    def test_sort_by_points_descending(self):
        """Test that teams are sorted by points descending."""
        team_a = TeamStats(name="A", points=7)
        team_b = TeamStats(name="B", points=4)
        team_c = TeamStats(name="C", points=1)
        
        sorted_teams = sort_teams([team_a, team_b, team_c])
        
        assert sorted_teams[0].name == "A"
        assert sorted_teams[1].name == "B"
        assert sorted_teams[2].name == "C"

    def test_sort_by_gd_when_points_equal(self):
        """Test that teams with equal points are sorted by GD descending."""
        team_a = TeamStats(name="A", points=4, goals_for=5, goals_against=2)
        team_b = TeamStats(name="B", points=4, goals_for=3, goals_against=2)
        team_c = TeamStats(name="C", points=4, goals_for=1, goals_against=3)
        
        sorted_teams = sort_teams([team_a, team_b, team_c])
        
        assert sorted_teams[0].name == "A"  # GD = 3
        assert sorted_teams[1].name == "B"  # GD = 1
        assert sorted_teams[2].name == "C"  # GD = -2

    def test_sort_alphabetically_when_points_and_gd_equal(self):
        """Test that teams with equal points and GD are sorted alphabetically."""
        # All have same points and same GD (goals_for - goals_against = 2)
        team_b = TeamStats(name="B", points=4, goals_for=3, goals_against=1)
        team_a = TeamStats(name="A", points=4, goals_for=3, goals_against=1)
        team_c = TeamStats(name="C", points=4, goals_for=3, goals_against=1)
        
        sorted_teams = sort_teams([team_b, team_a, team_c])
        
        assert sorted_teams[0].name == "A"
        assert sorted_teams[1].name == "B"
        assert sorted_teams[2].name == "C"

    def test_full_sort_complex_case(self):
        """Test complex sorting with multiple tiebreakers."""
        teams = [
            TeamStats(name="Brazil", points=7, goals_for=8, goals_against=5),  # GD=3
            TeamStats(name="Mexico", points=7, goals_for=7, goals_against=5),  # GD=2
            TeamStats(name="Sweden", points=4, goals_for=4, goals_against=4),  # GD=0
            TeamStats(name="Haiti", points=0, goals_for=2, goals_against=8),  # GD=-6
            TeamStats(name="Argentina", points=4, goals_for=4, goals_against=4),  # GD=0, same as Sweden
        ]
        
        sorted_teams = sort_teams(teams)
        
        # Brazil and Mexico both have 7 points, Brazil has better GD (3 vs 2)
        assert sorted_teams[0].name == "Brazil"
        assert sorted_teams[1].name == "Mexico"
        
        # Sweden and Argentina both have 4 points and 0 GD, sorted alphabetically
        assert sorted_teams[2].name == "Argentina"
        assert sorted_teams[3].name == "Sweden"
        
        # Haiti at bottom
        assert sorted_teams[4].name == "Haiti"

    def test_empty_list(self):
        """Test sorting empty list."""
        sorted_teams = sort_teams([])
        assert sorted_teams == []

    def test_single_team(self):
        """Test sorting single team."""
        team = TeamStats(name="A", points=3)
        sorted_teams = sort_teams([team])
        assert len(sorted_teams) == 1
        assert sorted_teams[0].name == "A"
