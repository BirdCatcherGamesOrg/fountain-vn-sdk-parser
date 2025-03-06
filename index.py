# SPDX-License-Identifier: MIT OR MPL-2.0

from pathlib import Path
from vnparser.config.config import ConfigLoader
from vnparser.script_parser import FountainVNParser

import logging.config
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s - %(message)s')

CONFIG_PATH = Path('config/config.json')

if __name__ == '__main__':
    config = ConfigLoader(CONFIG_PATH).load_or_create()
    parser = FountainVNParser()
    parser.parse(Path(config['path_to_script']), Path(config['output_dir']))
