# SPDX-License-Identifier: MPL-2.0

from logging import getLogger, Logger
from fountain.callback_parser import CallbackParser
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path
from vnparser.renpy_sdk.renderer import Renderer

import vnparser.types

logger: Logger = getLogger(__name__)


class FountainVNParser:
    def __init__(self):
        self.script: vnparser.types.ParsedScript = {'characters': {}, 'scenes': []}
        self.currentSceneSection = []
        self.parser = CallbackParser()
        self.parser.onDialogue = self._parse_dialogue
        self.parser.onSceneHeading = self._parse_scene_heading
        self.parser.onAction = self._parse_action
        self.parser.onSection = self._parse_section
        self.parser.onSynopsis = self._parse_synopsis
        self.parser.onTransition = self._parse_transition

    def parse(self, path_to_script: Path, output_dir: Path):
        logger.info(f'Parsing {path_to_script}')
        with path_to_script.open('r') as file:
            for line in file:
                self.parser.add_line(line)
        logger.info(f'Finished parsing {path_to_script}')

        env = Environment(
            loader=PackageLoader('vnparser', 'templates'),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        logger.info(f'Rendering as RenPy')
        render = Renderer(Path('./config/assets/') / f'{path_to_script.name}.assets.json', env)
        rendered_template = render.render(self.script)

        output_path = output_dir / f'{path_to_script.name}.rpy'
        logger.info(f'Writing {output_path}')
        with output_path.open('w') as file:
            file.write(rendered_template)

    def _parse_section(self, text, level):
        text = text.replace('#', '')
        text = text.lstrip()
        self.currentSceneSection.extend([''] * (level - len(self.currentSceneSection) + 1))
        self.currentSceneSection[level - 1] = text
        del self.currentSceneSection[level:]

    def _parse_scene_heading(self, text, scene_number):
        logger.info(f'Parsing scene {text}')
        self.script['scenes'].append({
            'lines': [],
            'heading': text,
            'scene_number': scene_number,
            'synopsis': '',
            'userData': '',
            'tags': ';'.join(self.parser.script.elements[-1].tags).rstrip()})
        self.currentSceneSection = []

    def _parse_dialogue(self, speaker, extension, parenthetical, line, is_dual_dialogue):
        if speaker not in self.script['characters']:
            logger.info(f'Discovered character {speaker}')
            self.script['characters'][speaker] = {'name': speaker}

        self.script['scenes'][-1]['lines'].append({
            'dialogue': {
                'speaker': speaker,
                'line': line,
            }
        })

    def _parse_action(self, text):
        if len(self.script['scenes']) == 0:
            return
        text = text.rstrip()
        if text == '':
            return

        if 'CUE:' in text:
            cue = text.removeprefix('CUE: ').split(' ', 1)
            self.script['scenes'][-1]['lines'].append({
                'cue': {
                    'type': cue[0],
                    'actions': cue[1].split(';'),
                }
            })
            return

        self.script['scenes'][-1]['lines'].append({
            'narration': {'text': text},
        })

    def _parse_synopsis(self, text):
        text = text.rstrip()
        if not text:
            return

        scene = self.script['scenes'][-1]
        if not scene['lines'] and not scene['synopsis']:
            scene['synopsis'] = text
            return

        scene['lines'].append({
            'synopsis': {'text': text},
        })

    def _parse_transition(self, text):
        text = text.rstrip()
        if not text:
            return

        scene = self.script['scenes'][-1]
        scene['lines'].append({
            'jump': {
                'condition': '',
                'scene': text,
            }
        })
