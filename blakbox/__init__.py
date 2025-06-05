from .atom import BOXatom
from .log import BOXlogger
import blakbox.app as app
import blakbox.utils as utils
import blakbox.scene as scene
import blakbox.pipeline as pipeline
import blakbox.resource as resource

from .globals import os, random
import blakbox.quotes as quotes
import blakbox.version as version
if "BLAKBOX_NO_PROMT" not in os.environ:
    print(
        f'BLAKBOX {version.BLAKBOX_YEAR}.{version.BLAKBOX_MINOR}.{version.BLAKBOX_PATCH} | "{random.choice(quotes.BLAKBOX_QUOTES)}"'
    )