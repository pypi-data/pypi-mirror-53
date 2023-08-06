from typing import Any, Optional

import flask
from flask_httpauth import HTTPBasicAuth
import jinja2
import nacl.exceptions
import nacl.pwhash
import pygit2
import werkzeug  # noqa

from .config import Config, parse_config  # noqa
from .errors import Error
from .helpers import cleanup_text
from .pages import Page, PageNotFound, Pages, up_page
from .searcher import Searcher
from .repository import Repository
from .renderer import Renderer
from .user import User


def create_auth(config: Config) -> HTTPBasicAuth:
    auth = HTTPBasicAuth()

    @auth.verify_password
    def verify_password(login: str, password: str) -> bool:
        if config.public_access:
            return True
        user = config.users.get(login)
        if not user:
            print("Unknow user:", login)
            return False
        try:
            nacl.pwhash.verify(user.hashed_password.encode(), password.encode())
        except nacl.exceptions.InvalidkeyError:
            print("Bad password for user:", login)
            return False

        flask.session["login"] = login
        return True

    return auth


def create_app(config: Optional[Config] = None) -> flask.Flask:  # noqa
    app = flask.Flask(__name__)
    app.jinja_env.undefined = jinja2.StrictUndefined

    if not config:
        config = parse_config()

    auth = create_auth(config)

    app.secret_key = config.secret_key

    repo_path = config.repo_path
    try:
        git_repo = pygit2.Repository(repo_path)
    except pygit2.GitError:
        raise RepoNotFound(repo_path)

    if not git_repo.is_bare:
        raise NonBareRepo(repo_path)

    searcher = Searcher(repo_path / ".whoosh")

    renderer = Renderer()

    def get_user() -> Optional[User]:
        assert config
        login = flask.session.get("login")
        if not login:
            return None
        return config.users[login]

    def get_repository() -> Repository:
        user = get_user()
        return Repository(git_repo, user=user)

    def get_pages() -> Pages:
        repository = get_repository()
        return Pages(repository, searcher)

    def redirect_to_page(name: str) -> Any:
        url = flask.url_for("view", name=name)
        return flask.redirect(url)

    @app.route("/")
    @auth.login_required
    def home() -> Any:
        return redirect_to_page("index")

    @app.route("/favicon.ico")
    @auth.login_required
    def favicon() -> Any:
        return flask.url_for("static", filename="favicon.ico")

    @app.route("/search")
    @auth.login_required
    def search() -> Any:
        pattern = flask.request.args.get("pattern")
        if not pattern:
            return flask.render_template("search_form.html")
        pages = get_pages()
        results = list(pages.search(pattern))
        return flask.render_template(
            "search_results.html", results=results, pattern=pattern
        )

    # This route is used in two different ways:
    #  * either we are GET'ing an existing page
    #  * or we're coming back from the preview, and we
    #    want to re-set the text to what was typed before
    @app.route("/edit/<path:name>", methods=["GET", "POST"])
    @auth.login_required
    def edit(name: str) -> Any:
        pages = get_pages()
        page = pages.page(name)
        text = flask.request.form.get("text")
        if not text:
            text = page.markdown
        num_lines = len(text.splitlines())
        return flask.render_template(
            "edit_form.html", page=page, num_lines=num_lines, text=text
        )

    @app.route("/save/<path:name>", methods=["POST"])
    @auth.login_required
    def save(name: str) -> Any:
        text = flask.request.form["text"]
        message = flask.request.form.get("message")
        text = cleanup_text(text)
        pages = get_pages()
        pages.save(name, text, message=message)
        return redirect_to_page(name)

    @app.route("/preview/<path:name>", methods=["POST"])
    @auth.login_required
    def preview(name: str) -> Any:
        text = flask.request.form["text"]
        text = cleanup_text(text)
        html = renderer.render(text)
        return flask.render_template("preview.html", html=html, name=name, text=text)

    @app.route("/add", methods=["GET", "POST"])
    @auth.login_required
    def add() -> Any:
        pages = get_pages()
        if flask.request.method == "GET":
            name = flask.request.args.get("name")
            return flask.render_template("add_form.html", name=name)
        else:
            name = flask.request.form["name"]
            title = flask.request.form["title"]
            if pages.exists(name):
                raise PageExists(name)
            text = "# " + title + "\n"
            pages.save(name, text)
            return redirect_to_page(name)

    @app.route("/view/<path:name>")
    @auth.login_required
    def view(name: str) -> Any:
        pages = get_pages()
        page = pages.page(name)
        return view_page(page)

    def view_page(page: Page) -> Any:
        pages = get_pages()
        parent = page.parent
        listing = pages.listing(parent=parent)
        up = up_page(parent)
        siblings = [pages.page(x) for x in listing.files[1:]]  # skip index
        children = [pages.page(x + "/index") for x in listing.dirs]
        total = pages.total()
        html = renderer.render(page.markdown)

        return flask.render_template(
            "page.html",
            up=up,
            page=page,
            html=html,
            siblings=siblings,
            children=children,
            total=total,
        )

    @app.route("/new")
    @auth.login_required
    def new_page() -> Any:
        name = flask.request.args["name"]
        blank_page = Page(name=name, markdown="")
        return flask.render_template("edit_form.html", page=blank_page, num_lines=10)

    @app.route("/rename/<path:old_name>", methods=["POST"])
    @auth.login_required
    def rename(old_name: str) -> Any:
        new_name = flask.request.form["new_name"]
        repository = get_repository()
        repository.rename(old_name + ".md", new_name + ".md")
        return redirect_to_page(new_name)

    @app.route("/remove/<path:name>", methods=["POST"])
    @auth.login_required
    def remove(name: str) -> Any:
        repository = get_repository()
        repository.remove(name + ".md")
        return redirect_to_page("index")

    @app.errorhandler(PageNotFound)
    def page_not_found(error: PageNotFound) -> Any:
        return flask.render_template("page_not_found.html", name=error.name), 404

    @app.errorhandler(PageExists)
    def page_exists(error: PageExists) -> Any:
        # TODO: flash?
        return flask.render_template("page_exists.html", name=error.name), 409

    return app


class PageExists(Error):
    def __init__(self, name: str):
        self.name = name


class RepoNotFound(Error):
    pass


class NonBareRepo(Error):
    pass
