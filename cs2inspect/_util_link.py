import urllib.parse

from cs2inspect._util_base import RE_MASKED_LINK, RE_UNMASKED_LINK


def _link_valid_and_type(inspect: str) -> tuple[bool, str | None]:
    """
    Check a given inspect link and return its validity and link type.

    :param inspect: The string to check.
    :type inspect: str

    :return: A tuple containing a boolean indicating validity and the type string ('masked' or 'unmasked') if valid.
    :rtype: tuple[bool, str | None]
    """

    if not is_link_quoted(inspect):
        inspect = quote_link(inspect)

    patterns = {
        'unmasked': RE_UNMASKED_LINK,
        'masked': RE_MASKED_LINK,
    }

    for link_type_str, pattern in patterns.items():
        if pattern.search(inspect):
            return True, link_type_str

    return False, None


def link_type(inspect: str) -> str | None:
    """
    Get the type of an inspect link (masked or unmasked).

    :param inspect: The inspect link to check.
    :type inspect: str

    :return: The link type ('masked' or 'unmasked') if valid, else None.
    :rtype: str | None
    """

    is_valid, link_type_str = _link_valid_and_type(inspect)
    if is_valid:
        return link_type_str

    return None


def is_link_valid(inspect: str) -> bool:
    """
    Validate a given inspect link.

    :param inspect: The inspect link to validate.
    :type inspect: str

    :return: True if the link is a valid format, False otherwise.
    :rtype: bool
    """

    is_valid, _ = _link_valid_and_type(inspect)

    return is_valid


def is_link_quoted(inspect: str) -> bool:
    """
    Check if an inspect link is URL encoded.

    :param inspect: The inspect link to check.
    :type inspect: str

    :return: True if the link contains url-encoded characters like '%20'.
    :rtype: bool
    """

    return "%20" in inspect


def unquote_link(inspect: str) -> str:
    """
    Unquote the given inspect link.

    :param inspect: The inspect link to unquote.
    :type inspect: str

    :return: The unquoted string.
    :rtype: str
    """

    return urllib.parse.unquote(inspect)


def quote_link(inspect: str) -> str:
    """
    Quote the given inspect link (applies inspect-link specific URL encoding).

    :param inspect: The inspect link to quote.
    :type inspect: str

    :return: The specifically quoted string.
    :rtype: str
    """

    return urllib.parse.quote(inspect, safe=":/+")


if __name__ == '__main__':
    exit(1)
