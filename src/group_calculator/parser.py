"""Parse group match files into Match objects."""

from group_calculator.models import Match


def parse_file(filepath: str) -> tuple[list[Match], list[str]]:
    """Parse a group match file into a list of Match objects.

    Args:
        filepath: Path to the group file (e.g., 'group_A.txt')

    Returns:
        Tuple of (list of Match objects, list of parsing error messages)

    The file format is tab-separated: TeamA<TAB>TeamB<TAB>Score
    where Score is in format "goals_a:goals_b"

    Empty lines and lines starting with '#' are ignored.
    """
    matches = []
    errors = []

    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        errors.append(f"File not found: {filepath}")
        return matches, errors
    except PermissionError:
        errors.append(f"Permission denied: {filepath}")
        return matches, errors
    except Exception as e:
        errors.append(f"Error reading file {filepath}: {e}")
        return matches, errors

    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Split by tab
        parts = line.split("\t")

        # Check we have exactly 3 parts
        if len(parts) != 3:
            errors.append(
                f"Line {line_num}: Expected 3 tab-separated values, found {len(parts)}"
            )
            continue

        team_a, team_b, score_str = parts

        # Check team names are not empty
        if not team_a.strip():
            errors.append(f"Line {line_num}: Team A name is empty")
            continue
        if not team_b.strip():
            errors.append(f"Line {line_num}: Team B name is empty")
            continue

        # Parse score
        try:
            score_a, score_b = map(int, score_str.split(":"))
        except ValueError:
            errors.append(
                f"Line {line_num}: Invalid score format '{score_str}'. Expected 'x:y' format."
            )
            continue

        try:
            match = Match(
                team_a=team_a.strip(),
                team_b=team_b.strip(),
                score_a=score_a,
                score_b=score_b,
            )
            matches.append(match)
        except ValueError as e:
            errors.append(f"Line {line_num}: {e}")
            continue

    return matches, errors


def parse_score(score_str: str) -> tuple[int, int]:
    """Parse a score string in format 'x:y' into two integers.

    Args:
        score_str: Score string like "4:3" or "0:0"

    Returns:
        Tuple of (goals_a, goals_b)

    Raises:
        ValueError: If score format is invalid
    """
    parts = score_str.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid score format: '{score_str}'. Expected 'x:y'.")

    try:
        goals_a = int(parts[0])
        goals_b = int(parts[1])
    except ValueError:
        raise ValueError(f"Invalid score values in '{score_str}'. Must be integers.")

    if goals_a < 0 or goals_b < 0:
        raise ValueError(f"Scores cannot be negative: '{score_str}'.")

    return goals_a, goals_b
