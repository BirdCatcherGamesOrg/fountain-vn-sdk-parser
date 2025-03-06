# SPDX-License-Identifier: MIT OR MPL-2.0

import json
from logging import getLogger, Logger
from pathlib import Path
from typing import TypedDict

logger: Logger = getLogger(__name__)

class RenpySDK(TypedDict, total=False):
    """RenpySDK are reserved settings for the RenPy SDK.
    """
    pass


class GodotSDK(TypedDict, total=False):
    """GodotSDK are reserved settings for the Godot SDK.
    """
    pass


class BCIVNDK(TypedDict, total=False):
    """BCIVNDK are reserved settings for the BCIVNDK.
    """
    pass


class Configuration(TypedDict, total=False):
    """Configuration stores the common settings for each run. Supports a single project/script,
    but it will be expanded to account for multiple projects with different paths and an "init" cli argument.
    """
    path_to_script: Path
    output_dir: Path
    preferred_sdk: str
    renpysdk: RenpySDK
    godotsdk: GodotSDK
    bcivndk: BCIVNDK


class ConfigLoader:
    """ConfigLoader loads or creates the lightweight bespoke configuration file.
    """
    def __init__(self, path: Path):
        self.path = path

    def load_or_create(self) -> Configuration:
        """load_or_create loads the configuration file if it exists, or prompts the user for an initial setup.
        """
        logger.info(f'Loading configuration from {self.path}')
        config: Configuration
        if not self.path.exists():
            logger.info(f'Configuration not found.')

            path_to_script = input('Enter path to the script .fountain file: ').strip()
            output_dir = input('Enter path to the output directory: ').strip()
            sdk = input('Enter the preferred SDK (renpy/bcivndk/godot): ').strip()

            config = {
                'path_to_script': Path(path_to_script),
                'output_dir': Path(output_dir),
                'preferred_sdk': sdk,
                'renpysdk': {},
                'godotsdk': {},
                'bcivndk': {},
            }

            serializable_config = {
                'path_to_script': str(config['path_to_script']),
                'output_dir': str(config['output_dir']),
                'renpysdk': config['renpysdk'],
                'godotsdk': config['godotsdk'],
                'bcivndk': config['bcivndk'],
            }
            self.path.write_text(json.dumps(serializable_config, indent=4))

            logger.info(f"Config file created at {self.path}")
            return config

        return json.loads(self.path.read_text())

