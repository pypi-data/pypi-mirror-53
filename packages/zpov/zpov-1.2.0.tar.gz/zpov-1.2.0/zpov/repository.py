import os
from typing import List, Optional

import attr
import pygit2

from .errors import Error
from .user import User

DEFAULT_MESSAGE = "automatic commit"
DEFAULT_USER = User(
    login="zpov", name="zpov", email="zpov@localhost", hashed_password=""
)


@attr.s
class Listing:
    dirs: List[str] = attr.ib()
    files: List[str] = attr.ib()


class Empty(Error):
    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return f"{self.path} is an empty repository"


class Repository:
    # Note: the data in self.repo is always up-to-date, because:
    #    - write_file() always creates a commit
    #    - read_file(), ls_files() and the like
    #      always resolve the HEAD commit through `_current_tree()`

    def __init__(self, git_repo: pygit2.Repository, user: Optional[User] = None):
        self.repo = git_repo
        if user is None:
            self.user = DEFAULT_USER
        else:
            self.user = user

    def read_file(self, path: str) -> bytes:
        tree = self._current_tree()
        if path not in tree:
            raise FileNotFoundError(path)
        entry = tree[path]
        oid = entry.id
        return self.repo.get(oid).data  # type: ignore

    def _current_tree(self) -> pygit2.Tree:
        if self.repo.is_empty:
            raise Empty(self.repo.path)
        head_oid = self.repo.head.target
        head_commit = self.repo.get(head_oid)
        return head_commit.tree

    def write_file(
        self, path: str, contents: str, *, message: Optional[str] = None
    ) -> None:
        # Note: we need to build as many 'tree' objects
        # as we need to, then add the 'blob' in the deepest
        # one, and then add all the 'tree' objects into to
        # the top tree, while making sure to keep existing
        # entries there.

        if self.repo.is_empty:
            tree = None
        else:
            tree = self._current_tree()

        if tree:
            builder = self.repo.TreeBuilder(tree)
        else:
            builder = self.repo.TreeBuilder()

        # Step 1: build a list of (sub_dir, builder) tuples
        parts = path.split("/")
        builders = []
        sub_tree = None
        builders.append(("", builder))
        for part in parts[:-1]:
            if tree:
                if part in tree:
                    sub_entry = tree[part]
                    sub_tree = self.repo.get(sub_entry.id)
            if sub_tree:
                builder = self.repo.TreeBuilder(sub_tree)
            else:
                builder = self.repo.TreeBuilder()
            builders.append((part, builder))
            tree = sub_tree

        # Step 2: Insert the newly created blob in the last builder
        blob = self.repo.create_blob(contents)
        _, last_builder = builders[-1]
        last_builder.insert(os.path.basename(path), blob, pygit2.GIT_FILEMODE_BLOB)

        # Step 3: Generate trees from all builders in reverse, until
        # top tree is reached
        builders.reverse()
        for i, (part, builder) in enumerate(builders[:-1]):
            _, above_builder = builders[i + 1]
            above_builder.insert(part, builder.write(), pygit2.GIT_FILEMODE_TREE)

        _, top_builder = builders[-1]
        tree = top_builder.write()
        if not message:
            message = f"Wrote {path}"
        self.commit(tree, message=message)

    def exists(self, name: str) -> bool:
        if self.repo.is_empty:
            return False
        tree = self._current_tree()
        return name in tree

    def commit(self, tree: pygit2.Tree, *, message: Optional[str] = None) -> None:
        """ Make a commit with a new tree. """
        # Note: the commit is *always* on top of the default branch
        if not message:
            message = DEFAULT_MESSAGE

        if self.repo.is_empty:
            parents: List[str] = []
        else:
            head_oid = self.repo.head.target
            parents = [head_oid]

        author = pygit2.Signature(self.user.name, self.user.email)
        commiter = author
        new_head = self.repo.create_commit(
            "HEAD", author, commiter, message, tree, parents
        )
        self.repo.head.set_target(new_head)

    def ls_files(self) -> List[str]:
        if self.repo.is_empty:
            return []
        tree = self._current_tree()
        res: List[str] = []
        self._walk(res, tree, "")
        return res

    def _walk(self, res: List[str], tree: pygit2.Tree, path: str) -> None:
        for entry in tree:
            if entry.type == "tree":
                subtree = self.repo.get(entry.id)
                subpath = os.path.join(path, entry.name)
                self._walk(res, subtree, subpath)
            else:
                res.append(os.path.join(path, entry.name))

    def remove(self, name: str) -> None:
        old_tree = self._current_tree()

        new_tree = self.repo.TreeBuilder()
        for entry in old_tree:
            if entry.name != name:
                new_tree.insert(entry.name, entry.id, entry.filemode)

        tree = new_tree.write()
        self.commit(tree, message=f"deleted {name}")

    def rename(self, src: str, dest: str) -> None:
        if not self.exists(src):
            raise FileNotFoundError(src)

        old_tree = self._current_tree()

        new_tree = self.repo.TreeBuilder()
        for entry in old_tree:
            entry_id = entry.id
            name = entry.name
            filemode = entry.filemode
            if name == src:
                new_tree.insert(dest, entry_id, filemode)
            else:
                new_tree.insert(name, entry_id, filemode)

        tree = new_tree.write()
        self.commit(tree, message=f"renamed {src} -> {dest}")
