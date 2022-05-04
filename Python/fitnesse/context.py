from __future__ import annotations
import abc


class SuiteResponder:
    SUITE_SETUP_NAME = "SuiteSetUp"
    SUITE_TEARDOWN_NAME = "SuiteTearDown"


class PageCrawler(abc.ABC):

    @abc.abstractmethod
    def get_full_path(self, wiki_page: WikiPage) -> WikiPagePath:
        pass

    @abc.abstractmethod
    def add_page(self, wiki_page: WikiPage, wiki_page_path: WikiPagePath, content: str) -> WikiPage:
        pass


class PageCrawlerImpl(PageCrawler):

    @staticmethod
    @abc.abstractmethod
    def get_inherited_page(page_name: str, context: WikiPage) -> WikiPage:
        pass


class WikiPage(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def make_root(name: str) -> WikiPage:
        pass

    @abc.abstractmethod
    def get_page_crawler(self) -> PageCrawler:
        pass

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_data(self) -> PageData:
        pass

    @abc.abstractmethod
    def set_data(self, page_data: PageData):
        pass

    @abc.abstractmethod
    def get_parent(self) -> WikiPage:
        pass

    @abc.abstractmethod
    def add_child_page(self, name: str) -> WikiPage:
        pass

    @abc.abstractmethod
    def get_child_page(self, name: str) -> WikiPage:
        pass

    @abc.abstractmethod
    def get_child_pages(self) -> {str, WikiPage}:
        pass


class WikiPagePath(abc.ABC):

    @abc.abstractmethod
    def add_name(self, name: str):
        pass

    @abc.abstractmethod
    def get_names(self) -> []:
        pass


class PageData(abc.ABC):

    @abc.abstractmethod
    def get_wiki_page(self) -> WikiPage:
        pass

    @abc.abstractmethod
    def has_attribute(self, attribute: str) -> bool:
        pass

    @abc.abstractmethod
    def get_content(self) -> str:
        pass

    @abc.abstractmethod
    def set_content(self, content: str):
        pass

    @abc.abstractmethod
    def get_html(self) -> str:
        pass


class PathParser(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def render(path: WikiPagePath) -> str:
        pass

    @staticmethod
    @abc.abstractmethod
    def parse(path_name: str) -> WikiPagePath:
        pass
