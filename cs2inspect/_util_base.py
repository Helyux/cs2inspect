import re

# Base prefixes for matching links and their inner payload segment
_LINK_PREFIX = r"^(?:steam://(?:run|rungame)/730/(?:\d*/)*)?(?:\+?\s*)?"
_PAYLOAD_PREFIX = r"csgo_econ_action_preview(?:\s+|%20|)"

# The payload body definitions
_MASKED_BODY = r"([0-9A-F]+)$"
_UNMASKED_BODY = r"([SM])(\d+)A(\d+)D(\d+)$"

# Exact validations used by _util_link.py
RE_MASKED_LINK = re.compile(_LINK_PREFIX + r"csgo_econ_action_preview(?: ?|%20)" + _MASKED_BODY)
RE_UNMASKED_LINK = re.compile(_LINK_PREFIX + r"csgo_econ_action_preview(?: ?|%20)" + _UNMASKED_BODY)

# Loose payload captures used by _util_parse.py
RE_MASKED_PAYLOAD = re.compile(_PAYLOAD_PREFIX + _MASKED_BODY, re.IGNORECASE)
RE_UNMASKED_PAYLOAD = re.compile(_PAYLOAD_PREFIX + _UNMASKED_BODY, re.IGNORECASE)

# Inspect link defaults
INSPECT_BASE_DEFAULT = "steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20"
INSPECT_BASE_NEW = "steam://run/730//+csgo_econ_action_preview%20"
INSPECT_BASE = INSPECT_BASE_DEFAULT

# Remote Schema
SCHEMA_URL = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/en/all.json"

# Hex parsing
MAX_HEX_PAYLOAD_SIZE = 100_000
