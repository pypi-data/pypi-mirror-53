import pytest

from zpov.pages import PageNotFound, Pages, parent_page, up_page


def test_simple_page(pages: Pages) -> None:
    pages.repository.write_file("index.md", "# Welcome\n\nThis is the index\n")
    assert pages.total() == 1
    index_md = pages.markdown("index")
    assert "This is the index" in index_md

    index_page = pages.page("index")

    assert index_page.name == "index"
    assert index_page.title == "Welcome"


def test_listing_top(pages_with_tree: Pages) -> None:
    actual = pages_with_tree.listing(parent="")
    assert actual.dirs == ["foo", "spam"]
    assert actual.files == ["index", "a_file"]


def test_get_listing_sub_dir(pages_with_tree: Pages) -> None:
    actual = pages_with_tree.listing(parent="spam")
    assert actual.dirs == ["spam/sub"]
    assert actual.files == ["spam/index", "spam/01_one", "spam/02_two"]


def test_page_not_found(pages_with_tree: Pages) -> None:
    with pytest.raises(PageNotFound):
        pages_with_tree.page("no-such")


def test_exists(pages_with_tree: Pages) -> None:
    assert pages_with_tree.exists("index")
    assert not pages_with_tree.exists("no-such")


def test_parent_page() -> None:
    assert parent_page("spam") == ""
    assert parent_page("spam/foo") == "spam"
    assert parent_page("spam/foo/bar") == "spam/foo"


def test_up_page() -> None:
    assert up_page("") is None
    assert up_page("spam") == "index"
    assert up_page("spam/foo") == "spam/index"
    assert up_page("spam/foo/bar") == "spam/foo/index"
