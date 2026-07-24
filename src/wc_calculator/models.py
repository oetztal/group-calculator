"""Data models for World Cup Group Calculator."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Match:
    """Represents a single match between two teams.
    
    Attributes:
        team_a: Name of the first team
        team_b: Name of the second team
        score_a: Goals scored by team_a
        score_b: Goals scored by team_b
    """
    team_a: str
    team_b: str
    score_a: int
    score_b: int
    
    def __post_init__(self):
        """Validate that team names are not empty and scores are non-negative."""
        if not self.team_a or not self.team_b:
            raise ValueError("Team names cannot be empty")
        if self.score_a < 0 or self.score_b < 0:
            raise ValueError("Scores cannot be negative")


@dataclass
class TeamStats:
    """Statistics for a single team in a group.
    
    Attributes:
        name: Team name
        matches: Total matches played
        wins: Number of matches won
        draws: Number of matches drawn
        losses: Number of matches lost
        points: Total points (3 per win, 1 per draw)
        goals_for: Total goals scored
        goals_against: Total goals conceded
        goal_difference: goals_for - goals_against (computed property)
    """
    name: str
    matches: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    points: int = 0
    goals_for: int = 0
    goals_against: int = 0
    goal_difference: int = field(init=False, default=0)
    
    def __post_init__(self):
        """Compute goal_difference after initialization."""
        self.goal_difference = self.goals_for - self.goals_against
    
    def update(self, goals_scored: int, goals_conceded: int, result: str) -> None:
        """Update statistics based on a match result.
        
        Args:
            goals_scored: Goals scored by this team in the match
            goals_conceded: Goals conceded by this team in the match
            result: One of 'win', 'draw', or 'loss'
        """
        self.matches += 1
        self.goals_for += goals_scored
        self.goals_against += goals_conceded
        self.goal_difference = self.goals_for - self.goals_against
        
        if result == 'win':
            self.wins += 1
            self.points += 3
        elif result == 'draw':
            self.draws += 1
            self.points += 1
        elif result == 'loss':
            self.losses += 1
        else:
            raise ValueError(f"Unknown result: {result}. Must be 'win', 'draw', or 'loss'.")
