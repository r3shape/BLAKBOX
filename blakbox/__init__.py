import blakbox.log as log
import blakbox.atom as atom
import blakbox.utils as utils

import blakbox.app as app
import blakbox.scene as scene
import blakbox.resource as resource
import blakbox.pipeline as pipeline

from .globals import os, random
import blakbox.quotes as quotes
import blakbox.version as version
if "BLAKBOX_NO_PROMT" not in os.environ:
    print(
        f'BLAKBOX {version.BLAKBOX_YEAR}.{version.BLAKBOX_MINOR}.{version.BLAKBOX_PATCH} | "{random.choice(quotes.BLAKBOX_QUOTES)}"'
    )