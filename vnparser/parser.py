# This file is part of an MIT-licensed project: see LICENSE file or README.md for details.
# Copyright (c) 2025 BirdCatcherInteractive

from fountain.callback_parser import CallbackParser
from jinja2 import Environment, PackageLoader, select_autoescape
from vnparser.types import ParsedScript


class FountainVNParser:
    def __init__(self):
        self.script: ParsedScript = {'characters': {}, 'scenes': []}
        self.currentSceneSection = []
        self.parser = CallbackParser()
        self.parser.onDialogue = self._parse_dialogue
        self.parser.onSceneHeading = self._parse_scene_heading
        self.parser.onAction = self._parse_action
        self.parser.onSection = self._parse_section


    def parse(self, file_name, output_file_name):
        with open(file_name, 'r') as file:
            for line in file:
                self.parser.add_line(line)

        if output_file_name is None:
            output_file_name = file_name.out

        env = Environment(
            loader=PackageLoader('vnparser', 'templates'),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        template = env.get_template('string_table.jinja2')
        rendered_template = template.render(scenes=self.script['scenes'])

        with open(output_file_name, 'w') as file:
            file.write(rendered_template)


    def _parse_section(self, text, level):
        text = text.replace('#', '')
        text = text.lstrip()
        self.currentSceneSection.extend([''] * (level - len(self.currentSceneSection) + 1))
        self.currentSceneSection[level-1] = text
        del self.currentSceneSection[level:]


    def _parse_scene_heading(self, text, scene_number):
        self.script['scenes'].append({'lines': [], 'text': text, 'scene_number': scene_number, 'userData': '', 'tags': ';'.join(self.parser.script.elements[-1].tags).rstrip()})
        self.currentSceneSection = []


    def _parse_dialogue(self, character, extension, parenthetical, line, is_dual_dialogue):
        self.script['characters'][character] = {'name': character}
        self.script['scenes'][-1]['lines'].append(
            {
                'text': line,
                'section': '#'.join(s for s in self.currentSceneSection if s),
                'speaker': character,
                'tags': ';'.join(self.parser.script.elements[-1].tags).rstrip()
            }
        )


    def _parse_action(self, text):
        if len(self.script['scenes']) == 0:
            return
        text = text.rstrip()
        if text != '-':
            self.script['scenes'][-1]['lines'].append({
                'text': text,
                'section': '#'.join(s for s in self.currentSceneSection if s),
                'speaker': '',
                'tags': ';'.join(self.parser.script.elements[-1].tags).rstrip()
            })
