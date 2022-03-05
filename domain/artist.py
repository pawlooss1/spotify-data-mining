from dataclasses import dataclass


@dataclass
class Artist:
    api_id: str
    name: str
    followers: int
    genres: list
    popularity: int
