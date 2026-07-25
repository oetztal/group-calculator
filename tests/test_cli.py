"""Integration tests for CLI."""

import json
import pytest
import sys
from pathlib import Path

from group_calculator.cli import main, process_group_file, process_all_groups


class TestProcessGroupFile:
    """Tests for process_group_file function."""

    def test_process_valid_file(self, valid_group_file):
        """Test processing a valid group file."""
        result = process_group_file(str(valid_group_file))
        
        assert "group_A" in result
        group_data = result["group_A"]
        
        assert group_data["is_valid"] is True
        assert len(group_data["teams"]) == 4
        assert len(group_data["messages"]) == 0

    def test_process_invalid_file(self, group_file_with_3_teams):
        """Test processing a file with invalid team count."""
        result = process_group_file(str(group_file_with_3_teams))
        
        assert "group_B" in result
        group_data = result["group_B"]
        
        assert group_data["is_valid"] is False
        assert len(group_data["messages"]) > 0


class TestProcessAllGroups:
    """Tests for process_all_groups function."""

    def test_process_all_in_directory(self, tmp_path):
        """Test processing all group files in a directory."""
        # Create multiple group files
        for i, content in enumerate([
            "A\tB\t1:0\nA\tC\t1:0\nA\tD\t1:0\nB\tC\t1:0\nB\tD\t1:0\nC\tD\t1:0\n",
            "E\tF\t1:0\nE\tG\t1:0\nE\tH\t1:0\nF\tG\t1:0\nF\tH\t1:0\nG\tH\t1:0\n",
        ]):
            file_path = tmp_path / f"group_{chr(65 + i)}.txt"
            file_path.write_text(content)
        
        results = process_all_groups(str(tmp_path))
        
        assert len(results) == 2
        assert "group_A" in results[0]
        assert "group_B" in results[1]


class TestMain:
    """Tests for main CLI function."""

    def test_single_file_success(self, valid_group_file, capsys):
        """Test CLI with a single valid file."""
        result = main([str(valid_group_file)])
        
        assert result == 0
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Should be valid JSON
        data = json.loads(output)
        assert "group_A" in data

    def test_single_file_invalid(self, group_file_with_3_teams, capsys):
        """Test CLI with a single invalid file."""
        result = main([str(group_file_with_3_teams)])
        
        assert result == 1
        
        captured = capsys.readouterr()
        assert "Validation errors:" in captured.err

    def test_all_flag(self, tmp_path, capsys):
        """Test CLI with --all flag."""
        # Create a group file
        file_path = tmp_path / "group_A.txt"
        content = (
            "Mexico\tHaiti\t4:3\n"
            "Mexico\tBrazil\t1:2\n"
            "Mexico\tSweden\t0:0\n"
            "Haiti\tBrazil\t1:4\n"
            "Haiti\tSweden\t2:1\n"
            "Brazil\tSweden\t3:3\n"
        )
        file_path.write_text(content)
        
        # Change to temp directory
        old_cwd = Path.cwd()
        try:
            import os
            os.chdir(str(tmp_path))
            
            result = main(["--all"])
            
            assert result == 0
            
            captured = capsys.readouterr()
            output = captured.out
            
            data = json.loads(output)
            assert "group_A" in data
        finally:
            os.chdir(str(old_cwd))

    def test_output_to_file(self, valid_group_file, tmp_path):
        """Test CLI with --output flag."""
        output_file = tmp_path / "results.json"
        
        result = main([str(valid_group_file), "--output", str(output_file)])
        
        assert result == 0
        assert output_file.exists()
        
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert "group_A" in data

    def test_no_arguments(self, capsys):
        """Test CLI with no arguments."""
        result = main([])
        
        assert result == 1
        
        captured = capsys.readouterr()
        assert "Specify a group file or use --all" in captured.err

    def test_file_not_found(self, capsys):
        """Test CLI with non-existent file."""
        result = main(["/nonexistent/group_X.txt"])
        
        assert result == 1
        
        captured = capsys.readouterr()
        assert "File not found" in captured.err

    def test_all_and_file_together(self, capsys):
        """Test CLI with both --all and file argument."""
        result = main(["--all", "group_A.txt"])
        
        assert result == 1
        
        captured = capsys.readouterr()
        assert "Cannot specify both" in captured.err
