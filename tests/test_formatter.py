"""Tests for formatter module."""

import json

from group_calculator.formatter import (
    format_all_groups,
    format_group_result,
    format_to_json,
)
from group_calculator.models import TeamStats


class TestFormatGroupResult:
    """Tests for format_group_result function."""

    def test_format_valid_group(self):
        """Test formatting a valid group result."""
        team_a = TeamStats(
            name="A",
            matches=3,
            wins=2,
            draws=1,
            losses=0,
            points=7,
            goals_for=5,
            goals_against=2,
        )
        team_b = TeamStats(
            name="B",
            matches=3,
            wins=1,
            draws=1,
            losses=1,
            points=4,
            goals_for=3,
            goals_against=3,
        )

        sorted_teams = [team_a, team_b]

        result = format_group_result(
            group_name="group_A", sorted_teams=sorted_teams, is_valid=True, messages=[]
        )

        assert "group_A" in result
        group_data = result["group_A"]

        assert group_data["is_valid"] is True
        assert group_data["messages"] == []
        assert len(group_data["teams"]) == 2

        team_a_data = group_data["teams"][0]
        assert team_a_data["name"] == "A"
        assert team_a_data["matches"] == 3
        assert team_a_data["wins"] == 2
        assert team_a_data["draws"] == 1
        assert team_a_data["losses"] == 0
        assert team_a_data["points"] == 7
        assert team_a_data["goal_difference"] == 3
        assert team_a_data["goals_for"] == 5
        assert team_a_data["goals_against"] == 2

    def test_format_invalid_group(self):
        """Test formatting an invalid group result."""
        team_a = TeamStats(name="A")

        result = format_group_result(
            group_name="group_B",
            sorted_teams=[team_a],
            is_valid=False,
            messages=["Expected 4 teams, found 1"],
        )

        assert "group_B" in result
        group_data = result["group_B"]

        assert group_data["is_valid"] is False
        assert "Expected 4 teams, found 1" in group_data["messages"]


class TestFormatToJson:
    """Tests for format_to_json function."""

    def test_format_to_json(self):
        """Test converting to JSON string."""
        team = TeamStats(name="A")
        result = format_group_result(
            group_name="group_A", sorted_teams=[team], is_valid=True, messages=[]
        )

        json_str = format_to_json(result, indent=2)

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert "group_A" in parsed


class TestFormatAllGroups:
    """Tests for format_all_groups function."""

    def test_combine_multiple_groups(self):
        """Test combining multiple group results."""
        team_a = TeamStats(name="A")
        team_b = TeamStats(name="B")

        group1 = format_group_result("group_A", [team_a], True, [])
        group2 = format_group_result("group_B", [team_b], True, [])

        combined = format_all_groups([group1, group2])

        assert "group_A" in combined
        assert "group_B" in combined
        assert len(combined) == 2

    def test_combine_empty_list(self):
        """Test combining empty list."""
        combined = format_all_groups([])
        assert combined == {}
