import bs4
from zpov.renderer import Renderer


def test_renders_h1() -> None:
    renderer = Renderer()
    html = renderer.render("# Title\nRest")
    soup = bs4.BeautifulSoup(html, "html.parser")
    assert soup.find("h1").text == "Title"


def test_uses_smartypants() -> None:
    renderer = Renderer()
    html = renderer.render("and so ...")
    assert "&hellip;" in html


def test_renders_fenced_code() -> None:
    renderer = Renderer()
    markdown = """
Here is some python code:

```python
def foo():
    return 42
```
"""
    html = renderer.render(markdown)
    soup = bs4.BeautifulSoup(html, "html.parser")
    assert (
        soup.find("pre").text.strip() == "def foo():\n    return 42"
    ), f"incorrect html: `{html}`"


def test_renders_check_boxes() -> None:
    renderer = Renderer()
    markdown = """
My todo-list:

   * [x] Make a TODO List
   * [x] Mark some *items* as complete
   * [ ] Enjoy!

And the text continues
        """
    html = renderer.render(markdown)
    soup = bs4.BeautifulSoup(html, "html.parser")
    first_item = soup.find("li")
    assert "checked" in first_item.input.attrs
    last_item = soup.find_all("li")[-1]
    assert "checked" not in last_item.input.attrs
