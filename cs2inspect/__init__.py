__author__ = "Lukas Mahler"
__version__ = "0.0.0"
__date__ = "26.10.2025"
__email__ = "m@hler.eu"
__status__ = "Development"


from cs2inspect._creation import gen, link, link_masked, link_unmasked
from cs2inspect._hex import from_hex, to_hex
from cs2inspect._link_util import is_link_quoted, is_link_valid, link_type, quote_link, unquote_link
from cs2inspect._proto import Builder

__all__ = [
    'Builder',

    'gen',
    'link',
    'link_masked',
    'link_unmasked',

    'link_type',
    'is_link_valid',
    'is_link_quoted',
    'quote_link',
    'unquote_link',

    'to_hex',
    'from_hex',
]


if __name__ == '__main__':
    exit(1)
