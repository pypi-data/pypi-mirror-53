import pygit2
import pytest
from path import Path

from zpov.repository import Repository


@pytest.fixture
def bare_repo(tmp_path: Path) -> pygit2.Repository:
    repo = pygit2.init_repository(str(tmp_path), bare=True)
    return repo


def test_empty(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    files = repository.ls_files()
    assert files == []


def test_create_top_file(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a.txt", "this is a\n")
    files = repository.ls_files()
    assert files == ["a.txt"]


def test_create_two_top_files(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a.txt", "this is a\n")
    repository.write_file("b.txt", "this is b\n")
    files = repository.ls_files()
    assert files == ["a.txt", "b.txt"]


def test_create_files_in_subdir(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a_dir/a.txt", "this is a\n")
    repository.write_file("a_dir/b.txt", "this is b\n")
    files = repository.ls_files()
    assert files == ["a_dir/a.txt", "a_dir/b.txt"]


def test_create_file_in_deep_subdir(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a/b/c.txt", "this is c\n")
    files = repository.ls_files()
    assert files == ["a/b/c.txt"]


def test_read_top_file(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a.txt", "this is a\n")
    actual = repository.read_file("a.txt")
    assert actual == b"this is a\n"


def test_read_file_in_subdir(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a/b/c.txt", "this is c\n")
    actual = repository.read_file("a/b/c.txt")
    assert actual == b"this is c\n"


def test_walk(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("index.md", "# Welcome\n\nindex matches foo\n")
    repository.write_file("bar/foo.md", "# Bar\n\nbar/foo also matches foo\n")
    repository.write_file("bar/index.md", "# Bar Index\n\nbar does not match\n")
    actual = repository.ls_files()
    assert set(actual) == {"index.md", "bar/index.md", "bar/foo.md"}


def test_delete_blob(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a.txt", "this is a test file\n")
    repository.write_file("b.txt", "this is an other test file\n")
    assert repository.ls_files() == ["a.txt", "b.txt"]

    repository.remove("a.txt")
    assert repository.ls_files() == ["b.txt"]


def test_rename_blob(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a.txt", "this is a test file\n")
    assert repository.ls_files() == ["a.txt"]

    repository.rename("a.txt", "b.txt")
    assert repository.ls_files() == ["b.txt"]


def test_delete_tree(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a.txt", "this is a test file\n")
    repository.write_file("bar/one.txt", "this is one\n")
    repository.write_file("foo/two.txt", "this is two\n")
    repository.write_file("foo/three.txt", "this is three\n")

    repository.remove("foo")

    assert set(repository.ls_files()) == {"a.txt", "bar/one.txt"}


def test_rename_tree(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("a.txt", "this is a test file\n")
    repository.write_file("foo/one.txt", "this is one\n")
    repository.write_file("foo/two.txt", "this is two\n")

    repository.rename("foo", "foo2")

    assert set(repository.ls_files()) == {"a.txt", "foo2/one.txt", "foo2/two.txt"}


def test_no_such_entry(bare_repo: pygit2.Repository) -> None:
    repository = Repository(bare_repo)
    repository.write_file("foo", "this is foo\n")
    with pytest.raises(FileNotFoundError):
        repository.read_file("bar.md")
