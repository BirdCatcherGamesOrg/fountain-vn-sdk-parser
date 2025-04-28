# SPDX-License-Identifier: MPL-2.0

from typing import TypedDict, List, Dict

from bci.model.character import Character
from bci.model.scene import Scene


class ParsedScript(TypedDict, total=False):
    characters: Dict[str, Character]
    scenes: List[Scene]
