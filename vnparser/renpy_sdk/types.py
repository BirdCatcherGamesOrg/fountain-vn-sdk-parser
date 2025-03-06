# SPDX-License-Identifier: MPL-2.0

from typing import Dict, List, NotRequired, TypedDict


class Scene(TypedDict, total=False):
    """Scene maps the generic VN asset to a record of the label, bg, and music that will play in the scene. For example,
    a scene like INT. ELLIS ROOM - NIGHT might map onto
    {
        "label": "int_ellis_room_night",
        "bg": "bedroom_night",
        "music": "calm.mp3"
    }

    Defaults to using the scene name for all fields, i.e.
    {
        "label": "int_ellis_room_night",
        "bg": "int_ellis_room_night",
        "music": "int_ellis_room_night.mp3"
    }
    """
    label: str
    bg: str
    music: str


class Speaker(TypedDict, total=False):
    """Speaker maps the generic VN asset to a Character RenPy class by name. For example, Ellis in the script may map
    onto a character 'e'. Defaults to using the first letter.
    """
    name: str


class AssetConfiguration(TypedDict, total=False):
    """AssetConfiguration maps the generic VN assets to user managed game assets.
    """
    speakers: Dict[str, Speaker]
    scenes: Dict[str, Scene]


class RenderMenu(TypedDict, total=False):
    """RenderMenu is unimplemented.
    TODO: https://github.com/BirdCatcherGamesOrg/fountain-vn-sdk-parser/issues/1
    """
    pass


class RenderScene(TypedDict, total=False):
    """RenderScene is the processed VN Asset scene into how it will appear in the rpy file.
    """
    label: str
    synopsis: str
    bg: str
    music: str
    lines: List[List[str]]
    menu: RenderMenu

