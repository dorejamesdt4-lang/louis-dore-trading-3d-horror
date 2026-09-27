"""Procedural nightmare-room director for The Shifting Mansion.

The director keeps the horror route deterministic for a run while randomising
which doorway is the trap, puzzle, and progression route. It is deliberately
engine-only and contains no rendering code so it can be unit tested.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field

ROLES = ("trap", "puzzle", "next")
PUZZLES = (
    ("CLOCK", "Set the stopped clock to the time hidden in the room."),
    ("SYMBOLS", "Find the three matching symbols and activate them in order."),
    ("PAINTING", "Find the painting that is facing the wrong way."),
    ("SOUND", "Listen for the three-note pattern and repeat it."),
)


@dataclass
class NightmareStage:
    stage: int
    roles: dict[str, str]
    puzzle_id: str
    puzzle_text: str
    solved: bool = False


@dataclass
class NightmareDirector:
    seed: int
    duration: float = 180.0
    time_left: float = 180.0
    stage: int = 0
    active: bool = False
    game_over: bool = False
    stages: list[NightmareStage] = field(default_factory=list)

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.start_stage()

    def start(self):
        self.active = True

    def start_stage(self):
        slots = ["room_a", "room_b", "room_c"]
        self.rng.shuffle(slots)
        roles = dict(zip(slots, ROLES))
        pid, ptext = self.rng.choice(PUZZLES)
        self.stages.append(NightmareStage(self.stage, roles, pid, ptext))

    @property
    def current(self) -> NightmareStage:
        return self.stages[-1]

    @property
    def pressure(self) -> float:
        if self.duration <= 0:
            return 1.0
        return max(0.0, min(1.0, 1.0 - self.time_left / self.duration))

    def update(self, dt: float) -> str | None:
        if not self.active or self.game_over:
            return None
        self.time_left = max(0.0, self.time_left - max(0.0, dt))
        if self.time_left <= 0:
            self.game_over = True
            return "timeout"
        return None

    def role_for(self, slot: str) -> str:
        return self.current.roles[slot]

    def enter(self, slot: str) -> str:
        role = self.role_for(slot)
        if role == "trap":
            return "trap"
        if role == "puzzle":
            return "puzzle"
        return "next_locked" if not self.current.solved else "next"

    def solve(self) -> bool:
        if self.current.solved:
            return True
        self.current.solved = True
        return True

    def advance(self) -> None:
        self.stage += 1
        self.start_stage()
