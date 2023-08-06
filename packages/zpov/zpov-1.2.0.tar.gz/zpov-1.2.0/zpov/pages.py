from typing import List, Iterator, Optional, Set
import attr
import posixpath


from .errors import Error
from .repository import Repository
from .searcher import Searcher, SearchResult


def parent_page(name: str) -> str:
    if "/" in name:
        return posixpath.dirname(name)
    else:
        return ""


def up_page(name: str) -> Optional[str]:
    if not name:
        return None
    if "/" not in name:
        return "index"
    return posixpath.dirname(name) + "/index"


@attr.s
class Page:
    name: str = attr.ib()
    markdown: str = attr.ib(default="")
    title: str = attr.ib(default="")

    @property
    def parent(self) -> str:
        return parent_page(self.name)


@attr.s
class PagesListing:
    dirs: List[str] = attr.ib()
    files: List[str] = attr.ib()


def num_slashes(name: str) -> int:
    return len([c for c in name if c == "/"])


def name_sorter(name: str) -> str:
    """ Make sure index is always first in the list """
    if name.endswith("index"):
        return "\0"
    else:
        return name


class Pages:
    def __init__(self, repository: Repository, searcher: Searcher):
        self.repository = repository
        self.searcher = searcher

    def names(self) -> List[str]:
        return [x[:-3] for x in self.repository.ls_files() if x.endswith(".md")]

    def listing(self, parent: str = "") -> PagesListing:
        if parent:
            return self._sub_listing(parent)
        else:
            return self._top_listing()

    def _top_listing(self) -> PagesListing:
        top_names = [x for x in self.names() if 0 <= num_slashes(x) <= 1]

        subdirs: Set[str] = set()
        files: List[str] = []

        for name in top_names:
            if "/" in name:
                dir_name = name.split("/")[0]
                subdirs.add(dir_name)
            else:
                files.append(name)

        files.sort(key=name_sorter)
        dirs = sorted(subdirs)
        return PagesListing(dirs=dirs, files=files)

    def _sub_listing(self, parent: str) -> PagesListing:
        prefix = parent + "/"
        n = num_slashes(parent)
        all_names = [
            x
            for x in self.names()
            if x.startswith(prefix) and n <= num_slashes(x) <= n + 2
        ]

        subdirs: Set[str] = set()
        files: List[str] = []

        for name in all_names:
            if num_slashes(name) == n + 2:
                dir_name = posixpath.dirname(name)
                subdirs.add(dir_name)
            else:
                files.append(name)

        files.sort(key=name_sorter)
        dirs = sorted(subdirs)
        return PagesListing(dirs=dirs, files=files)

    def total(self) -> int:
        return len(self.names())

    def page_title(self, name: str) -> str:
        markdown = self.markdown(name)
        return self.parse_title(markdown)

    def markdown(self, name: str) -> str:
        filename = name + ".md"
        try:
            contents = self.repository.read_file(filename)
        except FileNotFoundError:
            raise PageNotFound(name=name)

        return contents.decode()

    def save(self, name: str, text: str, message: Optional[str] = None) -> None:
        filename = name + ".md"
        self.repository.write_file(filename, text, message=message)
        title = self.parse_title(text)
        self.searcher.add_page(title=title, name=name, text=text)

    def exists(self, name: str) -> bool:
        filename = name + ".md"
        return self.repository.exists(filename)

    def parse_title(self, markdown: str) -> str:
        first_line = markdown.splitlines()[0]
        return first_line.replace("# ", "")

    def page(self, name: str) -> Page:
        markdown = self.markdown(name)
        title = self.parse_title(markdown)
        return Page(name=name, markdown=markdown, title=title)

    def search(self, pattern: str) -> Iterator[SearchResult]:
        return self.searcher.search(pattern)


class PageNotFound(Error):
    def __init__(self, name: str):
        self.name = name
