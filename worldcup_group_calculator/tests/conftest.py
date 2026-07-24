"""Pytest configuration and fixtures for World Cup Group Calculator."""

import os
import pytest
from pathlib import Path

# Root directory of the project
PROJECT_ROOT = Path(__file__).parent.parent

# Fixture directory
FIXTURES_DIR = PROJECT_ROOT / "tests" / "fixtures"


@pytest.fixture
def fixtures_dir():
    """Return the path to the fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture
def valid_group_file(tmp_path):
    """Create a valid group file with 4 teams and 6 matches."""
    content = (
        "Mexico\tHaiti\t4:3\n"
        "Mexico\tBrazil\t1:2\n"
        "Mexico\tSweden\t0:0\n"
        "Haiti\tBrazil\t1:4\n"
        "Haiti\tSweden\t2:1\n"
        "Brazil\tSweden\t3:3\n"
    )
    file_path = tmp_path / "group_A.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def group_file_with_3_teams(tmp_path):
    """Create a group file with only 3 teams."""
    content = (
        "Mexico\tHaiti\t4:3\n"
        "Mexico\tBrazil\t1:2\n"
        "Haiti\tBrazil\t1:4\n"
    )
    file_path = tmp_path / "group_B.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def group_file_with_5_teams(tmp_path):
    """Create a group file with 5 teams."""
    content = (
        "Mexico\tHaiti\t4:3\n"
        "Mexico\tBrazil\t1:2\n"
        "Mexico\tSweden\t0:0\n"
        "Mexico\tFrance\t2:1\n"
        "Haiti\tBrazil\t1:4\n"
        "Haiti\tSweden\t2:1\n"
        "Haiti\tFrance\t0:0\n"
        "Brazil\tSweden\t3:3\n"
        "Brazil\tFrance\t1:0\n"
        "Sweden\tFrance\t2:2\n"
    )
    file_path = tmp_path / "group_C.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def group_file_with_duplicate_match(tmp_path):
    """Create a group file with a duplicate match."""
    content = (
        "Mexico\tHaiti\t4:3\n"
        "Mexico\tBrazil\t1:2\n"
        "Mexico\tSweden\t0:0\n"
        "Haiti\tBrazil\t1:4\n"
        "Haiti\tSweden\t2:1\n"
        "Mexico\tHaiti\t2:1\n"  # Duplicate
    )
    file_path = tmp_path / "group_D.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def group_file_with_self_match(tmp_path):
    """Create a group file where a team plays itself."""
    content = (
        "Mexico\tHaiti\t4:3\n"
        "Mexico\tBrazil\t1:2\n"
        "Mexico\tSweden\t0:0\n"
        "Haiti\tBrazil\t1:4\n"
        "Haiti\tSweden\t2:1\n"
        "Mexico\tMexico\t5:0\n"  # Self match
    )
    file_path = tmp_path / "group_E.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def group_file_with_missing_matches(tmp_path):
    """Create a group file with missing matches."""
    content = (
        "Mexico\tHaiti\t4:3\n"
        "Mexico\tBrazil\t1:2\n"
        "Mexico\tSweden\t0:0\n"
        "Haiti\tBrazil\t1:4\n"
        # Missing: Haiti vs Sweden, Brazil vs Sweden
    )
    file_path = tmp_path / "group_F.txt"
    file_path.write_text(content)
    return file_path


@pytest.fixture
def group_file_with_comments(tmp_path):
    """Create a group file with comment lines."""
    content = (
        "# This is a comment\n"
        "Mexico\tHaiti\t4:3\n"
        "# Another comment\n"
        "Mexico\tBrazil\t1:2\n"
        "Mexico\tSweden\t0:0\n"
        "Haiti\tBrazil\t1:4\n"
        "Haiti\tSweden\t2:1\n"
        "Brazil\tSweden\t3:3\n"
    )
    file_path = tmp_path / "group_G.txt"
    file_path.write_text(content)
    return file_path
