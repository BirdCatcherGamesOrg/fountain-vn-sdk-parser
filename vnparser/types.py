# This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
# Copyright (c) 2025 BirdCatcherInteractive

from typing import TypedDict, List, Dict


class Line(TypedDict):
    text: str
    section: str
    speaker: str
    tags: str
    userData: str


class Scene(TypedDict):
    text: str
    scene_number: int
    lines: List[Line]
    tags: str
    userData: str


class Character(TypedDict):
    name: str


class ParsedScript(TypedDict):
    characters: Dict[str, Character]
    scenes: List[Scene]
