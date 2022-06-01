from io import StringIO
import typing

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    Pages = {
        "page_data": PageData,
        "include_suite_setup": bool,
        "page_crawler": PageCrawlerImpl,
        "path_parser": PathParser
    }

    _suite_setup: WikiPage
    _pages: Pages
    _page_path_name: str
    _setup: WikiPage
    _setup_path_name: str

    def __init__(self):
        self._suite_setup = None
        self._setup = None
        self._pages = None
        self._setup_path_name = None

    #@staticmethod
    def testable_html(self, pages: Pages) -> str:
        self._pages.page_data = pages.page_data
        wiki_page: WikiPage = self._pages.page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if self._pages.page_data.has_attribute("Test"):
            try:
                self._check_include_suite_setup(wiki_page)
            except Exception as e:
                print(f"The suite setup cannot be found!")

            _page_path_name = self._get_page_path_name(wiki_page)
            string_io.writelines(["!include -setup .", _page_path_name, "\n"])

            try:
                self._check_setup(wiki_page)
            except Exception as e:
                print(f"The setup cannot be found!")
            self._setup_path_name = self._get_setup_path_name(wiki_page)
            string_io.writelines(["!include -setup .", self._setup_path_name, "\n"])

        string_io.writelines([self._pages.page_data.get_content()])
        if self._pages.page_data.has_attribute("Test"):
            teardown: WikiPage = self._pages.page_crawler.get_inherited_page("TearDown", wiki_page)
            if teardown is not None:
                tear_down_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(teardown)
                tear_down_path_name: str = self._pages.path_parser.render(tear_down_path)
                string_io.writelines(["!include -teardown .", tear_down_path_name, "\n"])
            try:
                self._check_include_suite_setup(wiki_page)
            except Exception as e:
                print(f"The suite setup cannot be found!")
            suite_teardown: WikiPage = self._pages.page_crawler.get_inherited_page(SuiteResponder.SUITE_TEARDOWN_NAME, wiki_page)
            if suite_teardown is not None:
                page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(suite_teardown)
                page_path_name: str = self._pages.path_parser.render(page_path)
                string_io.writelines(["!include -teardown .", page_path_name, "\n"])

        self._pagespage_data.set_content(string_io.getvalue())
        return self._pages._page_data.get_html()

    def _fetch_suite_setup(self, wiki_page) -> WikiPage:
        return self._pages.page_crawler.get_inherited_page(SuiteResponder.SUITE_SETUP_NAME, wiki_page)

    def _check_include_suite_setup(self, wiki_page):
        self._suite_setup = self._fetch_suite_setup(wiki_page)
        if self._suite_setup is None:
            raise Exception

    def _get_page_path_name(self, wiki_page) -> str:
        return self._pages.path_parser.render(wiki_page.get_page_crawler().get_full_path(self._suite_setup))

    def _fetch_setup(self, wiki_page) -> WikiPage:
        return self._pages.page_crawler.get_inherited_page("SetUp", wiki_page)

    def _check_setup(self, wiki_page):
        self._setup = self._fetch_setup(wiki_page)
        if self._setup is None:
            raise Exception

    def _get_setup_path_name(self, wiki_page) -> str:
        return self._pages.path_parser.render(wiki_page.get_page_crawler().get_full_path(self._setup))


