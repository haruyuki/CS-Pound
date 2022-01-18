from flightrising import extract_dragon_id


class TestClass:
    def test_valid_link(self):
        assert (
            extract_dragon_id(
                "http://flightrising.com/main.php?p=lair&id=430187&tab=dragon&did=52548928"
            )
            == "52548928"
        )

    def test_invalid_link(self):
        assert (
            extract_dragon_id("http://www1.flightrising.com/lair/430187/419524/1")
            is None
        )
