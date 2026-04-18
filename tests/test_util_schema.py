import pytest

import cs2inspect


def test_parse_invalid_schema_path():
    """
    Test that providing an invalid path to ‘schema‘ raises FileNotFoundError.
    """
    link = "steam://run/730//+csgo_econ_action_preview%20S76561198084057307A30528246417D17141631587508493134"
    invalid_path = "non_existent_schema.json"

    with pytest.raises(FileNotFoundError) as excinfo:
        cs2inspect.parse(link, schema=invalid_path)

    assert "Schema file not found at" in str(excinfo.value)
    assert invalid_path in str(excinfo.value)

def test_parse_valid_schema_path(tmp_path):
    """
    Verify that a valid (but minimal) schema path still works.
    """
    link = "steam://run/730//+csgo_econ_action_preview%20S76561198084057307A30528246417D17141631587508493134"
    schema_file = tmp_path / "min_schema.json"
    schema_file.write_text("{}") # Minimal valid JSON

    # This should not raise an error, even if enrichment yields nothing
    result = cs2inspect.parse(link, schema=str(schema_file))
    assert isinstance(result, dict)
    assert "asset_id" in result
