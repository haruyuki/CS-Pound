from library import multi_replace


def test_results():
    assert (
        multi_replace(
            "this is a long string\n with a new line",
            {"this": "This", "\n": "", "line": "line."},
        )
        == "This is a long string with a new line."
    )
