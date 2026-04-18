from cs2inspect._create import gen, link, link_console, link_masked, link_unmasked
from cs2inspect._parse import UnsupportedItemError, parse, unlink
from cs2inspect._proto import Builder
from cs2inspect._schema import ItemSchema, download_schema, load_schema, load_schema_path
from cs2inspect._util_hex import from_hex, to_hex
from cs2inspect._util_link import is_link_quoted, is_link_valid, link_type, quote_link, unquote_link

__all__ = [
    # Core API
    'gen',
    'link',
    'link_console',
    'link_masked',
    'link_unmasked',
    'parse',
    'unlink',
    'UnsupportedItemError',

    # Protobuf Builder
    'Builder',

    # Schema Management
    'ItemSchema',
    'download_schema',
    'load_schema',
    'load_schema_path',

    # Link Utilities
    'is_link_quoted',
    'is_link_valid',
    'link_type',
    'quote_link',
    'unquote_link',

    # Hex Utilities
    'from_hex',
    'to_hex',
]


if __name__ == '__main__':
    exit(1)
