from path import Path
from zpov.searcher import Searcher


def test_search(tmp_path: Path) -> None:
    searcher = Searcher(tmp_path / ".whoosh")
    searcher.add_page(
        name="index", text="# Welcome\n\nindex matches foo\n", title="Welcome"
    )
    searcher.add_page(
        name="bar/foo", text="# Bar Foo \n\nbar/foo also matches foo\n", title="Bar Foo"
    )
    searcher.add_page(
        name="bar/index", text="# Bar Index\n\nbar does not match\n", title="Bar Index"
    )
    actual = list(searcher.search("foo"))
    assert len(actual) == 2
    actual_names = [x.name for x in actual]
    assert actual_names == ["bar/foo", "index"]
    actual_titles = [x.title for x in actual]
    assert actual_titles == ["Bar Foo", "Welcome"]
