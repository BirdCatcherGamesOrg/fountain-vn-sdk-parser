# SPDX-License-Identifier: MPL-2.0

import json
import logging
from pathlib import Path
from typing import List

import vnparser.types as vn_types
from jinja2 import Environment

import vnparser.renpy_sdk.types as rpy_types
from bci.model.line import Line
from bci.model.scene import Scene

logger: logging.Logger = logging.getLogger(__name__)

class Renderer:
    def __init__(self, asset_configuration_path: Path, env: Environment):
        self.template = env.get_template('renpy.jinja2')
        self.asset_configuration_path = asset_configuration_path
        self.asset_configuration: rpy_types.AssetConfiguration = {
            'speakers': {},
            'scenes': {},
        }

        if asset_configuration_path.exists():
            with asset_configuration_path.open('r') as file:
                self.asset_configuration = json.loads(file.read())


    def render(self, script: vn_types.ParsedScript):
        render_scenes = []
        for parsed_scene in script['scenes']:
            render_scenes.append(self._make_scene(parsed_scene))

        rendered_template = self.template.render(scenes=render_scenes)

        with self.asset_configuration_path.open('w') as file:
            file.write(json.dumps(self.asset_configuration, indent=4))

        return rendered_template


    def _make_scene(self, scene: Scene) -> rpy_types.RenderScene:
        scene_name = scene['heading'].split('#')[0].strip()
        logger.info(f"Rendering {scene_name}")
        scene_name =(
            scene_name.replace(' -', '').replace(' ', '_').replace('.', '').replace('\'', '').lower())
        config_scene: rpy_types.Scene = self.asset_configuration['scenes'].setdefault(scene_name, {
            'label': scene_name,
            'bg': scene_name,
            'music': str(Path('audio') / f'{scene_name}.mp3'),
        })

        # If the first line of the scene is a synopsis, move it to be the first comment under the label.
        lines_to_render = scene['lines']
        render_scene: rpy_types.RenderScene = {}
        if synopsis := scene['lines'][0].get('synopsis'):
            render_scene['synopsis'] = synopsis['text']
            lines_to_render = lines_to_render[1:-1]

        render_scene['lines'] = [self._make_line(line) for line in lines_to_render]

        if label := config_scene.get('label'):
            render_scene['label'] = label

        if bg := config_scene.get('bg'):
            render_scene['bg'] = bg

        if music := config_scene.get('music'):
            render_scene['music'] = music

        return render_scene


    def _make_line(self, line: Line) -> List[str]:
        lines = []
        if narration := line.get('narration'):
            lines.append(f"\"{narration['text']}\"")

        if dialogue := line.get('dialogue'):
            character = self._make_character(dialogue['speaker'])
            lines.append(f"{character['name']} \"{dialogue['line']}\"")

        if synopsis:= line.get('synopsis'):
            lines.append(f"# {synopsis['text']}")

        if jump := line.get('jump'):
            lines.append(f"jump {jump['scene'].replace(' -', '').replace(' ', '_').replace('.', '').lower()}")

        if menu := line.get('menu'):
            pass

        if cue := line.get('cue'):
            if cue['type'] == 'ENTER':
                lines.extend([
                    ' '.join(['show'] +
                             [self._make_character(entrance[0])['name']] +
                             ([entrance[1].lower()] if entrance[1] else []))
                    for action in cue['actions']
                    if (entrance := (action.split(', ') + [""])[:2])
                ])

        return lines


    def _make_character(self, speaker: str) -> rpy_types.Speaker:
        return self.asset_configuration['speakers'].setdefault(speaker.strip().lower(), {
            'name': speaker.strip().lower()[0],
        })

