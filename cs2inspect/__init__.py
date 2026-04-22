import importlib.metadata

try:
    __version__ = importlib.metadata.version("cs2inspect")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

from ._create import gen, link, link_console, link_masked, link_unmasked
from ._parse import UnsupportedItemError, parse, unlink
from ._proto import Builder
from ._schema import ItemSchema, download_schema, load_schema, load_schema_path
from ._util_hex import from_hex, to_hex
from ._util_link import is_link_quoted, is_link_valid, link_type, quote_link, unquote_link

__all__ = [
    # Core API
    "gen",
    "link",
    "link_console",
    "link_masked",
    "link_unmasked",
    "parse",
    "unlink",
    "UnsupportedItemError",
    # Protobuf Builder
    "Builder",
    # Schema Management
    "ItemSchema",
    "download_schema",
    "load_schema",
    "load_schema_path",
    # Link Utilities
    "is_link_quoted",
    "is_link_valid",
    "link_type",
    "quote_link",
    "unquote_link",
    # Hex Utilities
    "from_hex",
    "to_hex",
]
