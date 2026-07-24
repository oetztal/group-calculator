"""Tests for validator module."""

import pytest

from wc_calculator.models import Match
from wc_calculator.validator import validate_group, get_expected_pairs


class TestValidateGroup:
    """Tests for validate_group function."""

    def test_valid_group(self):
        """Test validation of a valid group with 4 teams and 6 matches."""
        matches = [
            Match("Mexico", "Haiti", 4, 3),
            Match("Mexico", "Brazil", 1, 2),
            Match("Mexico", "Sweden", 0, 0),
            Match("Haiti", "Brazil", 1, 4),
            Match("Haiti", "Sweden", 2, 1),
            Match("Brazil", "Sweden", 3, 3),
        ]
        
        is_valid, errors = validate_group(matches)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_invalid_3_teams(self):
        """Test validation fails with only 3 teams."""
        matches = [
            Match("Mexico", "Haiti", 4, 3),
            Match("Mexico", "Brazil", 1, 2),
            Match("Haiti", "Brazil", 1, 4),
        ]
        
        is_valid, errors = validate_group(matches)
        
        assert is_valid is False
        assert len(errors) == 1
        assert "Expected 4 teams, found 3" in errors[0]

    def test_invalid_5_teams(self):
        """Test validation fails with 5 teams."""
        matches = [
            Match("A", "B", 1, 0),
            Match("A", "C", 1, 0),
            Match("A", "D", 1, 0),
            Match("A", "E", 1, 0),
            Match("B", "C", 1, 0),
        ]
        
        is_valid, errors = validate_group(matches)
        
        assert is_valid is False
        assert any("Expected 4 teams, found 5" in e for e in errors)

    def test_self_match(self):
        """Test validation fails when a team plays itself."""
        matches = [
            Match("Mexico", "Haiti", 4, 3),
            Match("Mexico", "Brazil", 1, 2),
            Match("Mexico", "Sweden", 0, 0),
            Match("Haiti", "Brazil", 1, 4),
            Match("Haiti", "Sweden", 2, 1),
            Match("Mexico", "Mexico", 5, 0),  # Self match
        ]
        
        is_valid, errors = validate_group(matches)
        
        assert is_valid is False
        assert any("cannot play itself" in e for e in errors)

    def test_duplicate_match(self):
        """Test validation fails with duplicate matches."""
        matches = [
            Match("Mexico", "Haiti", 4, 3),
            Match("Mexico", "Brazil", 1, 2),
            Match("Mexico", "Sweden", 0, 0),
            Match("Haiti", "Brazil", 1, 4),
            Match("Haiti", "Sweden", 2, 1),
            Match("Mexico", "Haiti", 2, 1),  # Duplicate of first
        ]
        
        is_valid, errors = validate_group(matches)
        
        assert is_valid is False
        assert any("Duplicate match" in e for e in errors)

    def test_missing_matches(self):
        """Test validation fails when matches are missing."""
        matches = [
            Match("Mexico", "Haiti", 4, 3),
            Match("Mexico", "Brazil", 1, 2),
            Match("Mexico", "Sweden", 0, 0),
            Match("Haiti", "Brazil", 1, 4),
            # Missing: Haiti vs Sweden, Brazil vs Sweden
        ]
        
        is_valid, errors = validate_group(matches)
        
        assert is_valid is False
        assert any("Missing matches" in e for e in errors)

    def test_collects_all_errors(self):
        """Test that all validation errors are collected."""
        matches = [
            Match("A", "B", 1, 0),
            Match("A", "C", 1, 0),
            # Only 3 teams, missing matches, duplicate would need more
        ]
        
        is_valid, errors = validate_group(matches)
        
        assert is_valid is False
        assert len(errors) >= 1  # At least team count error


class TestGetExpectedPairs:
    """Tests for get_expected_pairs function."""

    def test_4_teams(self):
        """Test getting expected pairs for 4 teams."""
        teams = {"A", "B", "C", "D"}
        expected = get_expected_pairs(teams)
        
        assert len(expected) == 6
        assert ("A", "B") in expected
        assert ("A", "C") in expected
        assert ("A", "D") in expected
        assert ("B", "C") in expected
        assert ("B", "D") in expected
        assert ("C", "D") in expected

    def test_3_teams(self):
        """Test getting expected pairs for 3 teams."""
        teams = {"A", "B", "C"}
        expected = get_expected_pairs(teams)
        
        assert len(expected) == 3
        assert ("A", "B") in expected
        assert ("A", "C") in expected
        assert ("B", "C") in expected
