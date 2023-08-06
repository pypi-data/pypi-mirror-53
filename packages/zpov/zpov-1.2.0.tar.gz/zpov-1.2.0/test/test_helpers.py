from zpov.helpers import remove_blank_lines_at_eof


def test_remove_blank_lines_at_eof() -> None:
    test = "a\nb\n\nc\n\n\n"
    assert remove_blank_lines_at_eof(test) == "a\nb\n\nc\n"
