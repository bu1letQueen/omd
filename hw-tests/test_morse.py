import pytest

from morse import decode


@pytest.mark.parametrize(
    "morse_message, expected",
    [
        ("... --- ...", "SOS"),
        ("..--- ----- .---- ----.", "2019"),
        ("-- .- .. .--. -.-- - .... --- -.", "MAIPYTHON"),
    ],
)
def test_decode(morse_message, expected):
    assert decode(morse_message) == expected