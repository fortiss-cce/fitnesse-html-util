import pytest
from fitnesse.context import PageCrawler, PathParser, WikiPage, WikiPagePath, PageData, PageCrawlerImpl


@pytest.fixture
def page_crawler() -> PageCrawler:
    return PageCrawlerStub()


@pytest.fixture
def wiki_page() -> WikiPage:
    return WikiPageStub()


@pytest.fixture
def wiki_page_path() -> WikiPagePath:
    return WikiPagePath()


@pytest.fixture
def path_parser() -> PathParser:
    return PathParserStub()


class PageCrawlerStub(PageCrawlerImpl):

    @staticmethod
    def get_inherited_page(page_name: str, context: WikiPage) -> WikiPage:
        return context.get_parent().get_child_page(page_name)  # TODO

    def get_full_path(self, wiki_page: WikiPage) -> WikiPagePath:
        return WikiPagePathStub(wiki_page)

    def add_page(self, parent_wiki_page: WikiPage, child_wiki_page_path: WikiPagePath, child_content: str) -> WikiPage:
        child_wiki_page: WikiPage = parent_wiki_page.add_child_page(child_wiki_page_path.get_names()[-1])
        page_data: PageData = PageDataStub(child_wiki_page, child_content)
        child_wiki_page.set_data(page_data)
        return child_wiki_page


class WikiPageStub(WikiPage):

    def __init__(self, name: str = None, content: str = None, parent: WikiPage = None):
        self.name: str = name
        self.parent: WikiPage = parent
        self.page_data: PageData = PageDataStub(self, content)
        self.children: {str, WikiPage} = {}

    @staticmethod
    def make_root(name: str) -> WikiPage:
        return WikiPageStub(name, "")

    def get_page_crawler(self) -> PageCrawler:
        return PageCrawlerStub()

    def get_name(self) -> str:
        return self.name

    def get_data(self) -> PageData:
        return self.page_data

    def set_data(self, page_data: PageData):
        self.page_data = page_data

    def get_parent(self) -> WikiPage:
        return self.parent

    def add_child_page(self, name: str) -> WikiPage:
        child_wiki_page = WikiPageStub(name, "", self)
        self.children[name] = child_wiki_page
        return child_wiki_page

    def get_child_page(self, name: str) -> WikiPage:
        return self.children.get(name)

    def get_child_pages(self) -> {str, WikiPage}:
        return self.children


class PageDataStub(PageData):

    def __init__(self, wiki_page: WikiPage, content: str):
        self.content: str = ''
        self.wiki_page: WikiPage = wiki_page
        self.set_content(content)

    def get_wiki_page(self) -> WikiPage:
        return self.wiki_page

    def has_attribute(self, attribute: str) -> bool:
        return True

    def get_content(self) -> str:
        return self.content

    def set_content(self, content: str):
        self.content = content

    def get_html(self) -> str:
        html = ""
        for wiki_page in self.wiki_page.get_parent().get_child_pages().values():
            html += "<p>"
            html += wiki_page.get_data().get_content()
            html += "</p>"
        print(html)
        return html  # TODO


class PathParserStub(PathParser):

    def __init__(self):
        self.wiki_page_path: WikiPagePath = WikiPagePathStub()

    @staticmethod
    def render(path: WikiPagePath) -> str:
        names = ''
        for name in path.get_names():
            names += name
        return names

    @staticmethod
    def parse(path_name: str) -> WikiPagePath:
        path_parser = PathParserStub()
        return path_parser.make_path(path_name)

    def make_path(self, path_name) -> WikiPagePath:
        self.wiki_page_path = WikiPagePathStub()
        self.wiki_page_path.add_name(path_name)
        return self.wiki_page_path


class WikiPagePathStub(WikiPagePath):

    def __init__(self, wiki_page: WikiPage = None):
        self.names: [str] = []
        self.set_names(wiki_page)

    def set_names(self, wiki_page: WikiPage):
        if wiki_page is not None:
            i = wiki_page
            while i.get_parent() is not None:
                self.names.append(i.get_name())
                i = i.get_parent()

    def add_name(self, name: str):
        self.names.append(name)

    def get_names(self) -> [str]:
        return self.names
