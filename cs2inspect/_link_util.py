__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "11.08.2024"
__email__ = "m@hler.eu"
__status__ = "Development"

import re
import urllib.parse
from typing import Optional


def _link_valid_and_type(inspect: str) -> tuple[bool, Optional[str]]:
    """Check a given inspect link and return validity and if valid the type of the inspect link"""

    if not is_link_quoted(inspect):
        inspect = quote_link(inspect)

    unmasked = re.compile(
        r"^steam://rungame/730/\d+/[+ ]csgo_econ_action_preview(?: ?|%20)([SM])(\d+)A(\d+)D(\d+)$")
    masked = re.compile(r"^steam://rungame/730/\d+/[+ ]csgo_econ_action_preview(?: ?|%20)[0-9A-F]+$")
    patterns = {
        'unmasked': unmasked,
        'masked': masked
    }

    for link_type_str, pattern in patterns.items():
        if pattern.search(inspect):
            return True, link_type_str

    return False, None


def link_type(inspect: str) -> Optional[str]:
    """Get the type of inspect link (masked or unmasked)"""

    is_valid, link_type_str = _link_valid_and_type(inspect)
    if is_valid:
        return link_type_str

    return None


def is_link_valid(inspect: str) -> bool:
    """Validate a given inspect link"""

    is_valid, _ = _link_valid_and_type(inspect)

    return is_valid


def is_link_quoted(inspect: str) -> bool:
    """Check if an inspect link is url encoded"""
    return "%20" in inspect


def unquote_link(inspect: str) -> str:
    """Unquote the given inspection link"""

    return urllib.parse.unquote(inspect)


def quote_link(inspect: str) -> str:
    """Quote the given inspection link (this is inspect link specific!)"""

    return urllib.parse.quote(inspect, safe=":/+")


if __name__ == '__main__':
    exit(1)
