"""Tests for parser module."""

import pytest

from group_calculator.parser import parse_file, parse_score


class TestParseFile:
    """Tests for parse_file function."""

    def test_parse_valid_file(self, valid_group_file):
        """Test parsing a valid group file."""
        matches, errors = parse_file(str(valid_group_file))

        assert len(errors) == 0
        assert len(matches) == 6

        # Check first match
        assert matches[0].team_a == "Mexico"
        assert matches[0].team_b == "Haiti"
        assert matches[0].score_a == 4
        assert matches[0].score_b == 3

    def test_parse_file_not_found(self):
        """Test parsing non-existent file."""
        matches, errors = parse_file("/nonexistent/path/group_X.txt")

        assert len(matches) == 0
        assert len(errors) == 1
        assert "File not found" in errors[0]

    def test_parse_teams_with_spaces(self, tmp_path):
        """Test parsing team names with spaces."""
        content = "Costa Rica\tUnited States\t2:1\n"
        file_path = tmp_path / "group.txt"
        file_path.write_text(content)

        matches, errors = parse_file(str(file_path))

        assert len(errors) == 0
        assert len(matches) == 1
        assert matches[0].team_a == "Costa Rica"
        assert matches[0].team_b == "United States"

    def test_parse_skip_empty_lines(self, tmp_path):
        """Test that empty lines are skipped."""
        content = "Mexico\tHaiti\t4:3\n\nBrazil\tSweden\t1:1\n\n"
        file_path = tmp_path / "group.txt"
        file_path.write_text(content)

        matches, errors = parse_file(str(file_path))

        assert len(errors) == 0
        assert len(matches) == 2

    def test_parse_skip_comments(self, tmp_path):
        """Test that comment lines are skipped."""
        content = "# This is a comment\nMexico\tHaiti\t4:3\n# Another comment\nBrazil\tSweden\t1:1\n"
        file_path = tmp_path / "group.txt"
        file_path.write_text(content)

        matches, errors = parse_file(str(file_path))

        assert len(errors) == 0
        assert len(matches) == 2

    def test_parse_invalid_format_too_few_columns(self, tmp_path):
        """Test parsing line with too few columns."""
        content = "Mexico\tHaiti\n"  # Missing score
        file_path = tmp_path / "group.txt"
        file_path.write_text(content)

        matches, errors = parse_file(str(file_path))

        assert len(matches) == 0
        assert len(errors) == 1
        assert "Expected 3 tab-separated values" in errors[0]

    def test_parse_invalid_format_too_many_columns(self, tmp_path):
        """Test parsing line with too many columns."""
        content = "Mexico\tHaiti\t4:3\tExtra\n"
        file_path = tmp_path / "group.txt"
        file_path.write_text(content)

        matches, errors = parse_file(str(file_path))

        assert len(matches) == 0
        assert len(errors) == 1
        assert "Expected 3 tab-separated values" in errors[0]

    def test_parse_invalid_score_format(self, tmp_path):
        """Test parsing invalid score format."""
        content = "Mexico\tHaiti\t4-3\n"  # Uses hyphen instead of colon
        file_path = tmp_path / "group.txt"
        file_path.write_text(content)

        matches, errors = parse_file(str(file_path))

        assert len(matches) == 0
        assert len(errors) == 1
        assert "Invalid score format" in errors[0]

    def test_parse_multiple_errors(self, tmp_path):
        """Test that multiple errors are collected."""
        content = "Mexico\tHaiti\t4:3\nInvalid line\nBrazil\tSweden\tinvalid\n"
        file_path = tmp_path / "group.txt"
        file_path.write_text(content)

        matches, errors = parse_file(str(file_path))

        assert len(matches) == 1  # Only valid first line
        assert len(errors) == 2


class TestParseScore:
    """Tests for parse_score function."""

    def test_parse_standard_score(self):
        """Test parsing standard score format."""
        goals_a, goals_b = parse_score("4:3")
        assert goals_a == 4
        assert goals_b == 3

    def test_parse_zero_score(self):
        """Test parsing zero score."""
        goals_a, goals_b = parse_score("0:0")
        assert goals_a == 0
        assert goals_b == 0

    def test_parse_high_score(self):
        """Test parsing high score."""
        goals_a, goals_b = parse_score("10:5")
        assert goals_a == 10
        assert goals_b == 5

    def test_parse_invalid_separator_raises(self):
        """Test that invalid separator raises ValueError."""
        with pytest.raises(ValueError, match="Invalid score format"):
            parse_score("4-3")

    def test_parse_non_integer_raises(self):
        """Test that non-integer scores raise ValueError."""
        with pytest.raises(ValueError, match="Invalid score values"):
            parse_score("4:a")

    def test_parse_negative_score_raises(self):
        """Test that negative scores raise ValueError."""
        with pytest.raises(ValueError, match="Scores cannot be negative"):
            parse_score("-1:0")
