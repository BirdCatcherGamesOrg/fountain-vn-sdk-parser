# SPDX-License-Identifier: MPL-2.0

from typing import TypedDict, List, Dict


class Narration(TypedDict, total=False):
    text: str


class Dialogue(TypedDict, total=False):
    speaker: str
    line: str


class Jump(TypedDict, total=False):
    condition: str
    scene: str

class Menu(TypedDict, total=False):
    # TODO: https://github.com/BirdCatcherGamesOrg/fountain-vn-sdk-parser/issues/1
    condition: str
    scene: str


class Cue(TypedDict, total=False):
    type: str
    actions: List[str]


class Synopsis(TypedDict, total=False):
    text: str


class Line(TypedDict, total=False):
    narration: Narration
    dialogue: Dialogue
    synopsis: Synopsis
    jump: Jump
    menu: Menu
    cue: Cue
    tags: str
    userData: str


class Scene(TypedDict, total=False):
    heading: str
    scene_number: int
    synopsis: str
    lines: List[Line]
    tags: str
    userData: str


class Character(TypedDict, total=False):
    name: str


class ParsedScript(TypedDict, total=False):
    characters: Dict[str, Character]
    scenes: List[Scene]
