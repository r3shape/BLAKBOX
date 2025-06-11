from .atom import NBOXatom
from .log import NBOXlogger


from .globals import os, random
import netbox.version as version
if "NETBOX_NO_PROMT" not in os.environ:
    print(f"NETBOX {version.NETBOX_YEAR}.{version.NETBOX_MINOR}.{version.NETBOX_PATCH}")

