from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    types = {
        "SetUp": str,
        "TearDown": str,
    }
    def __init__(self, page_data: PageData, page_crawler: PageCrawlerImpl, path_parser: PathParser):
        self._page_data = page_data
        self._page_crawler = page_crawler
        self._path_parser = path_parser

    def testable_html(self, include_suite_setup: bool) -> str:
        wiki_page: WikiPage = self._page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if self._check_page_attribute("Test"):
            for type in types

        if self._page_data.has_attribute("Test"):
            if include_suite_setup:
                suite_setup: WikiPage = self._page_crawler.get_inherited_page(SuiteResponder.SUITE_SETUP_NAME, wiki_page)
                if suite_setup is not None:
                    string_io=self._write_pathname_to_IO(self,string_io,suite_setup, wiki_page,"setup")

            setup: WikiPage = self._page_crawler.get_inherited_page("SetUp", wiki_page)
            if setup is not None:
                string_io=self._write_pathname_to_IO(self,string_io,setup, wiki_page,"setup")

        string_io.writelines([self._page_data.get_content()])
        if self._page_data.has_attribute("Test"):
            teardown: WikiPage = self._page_crawler.get_inherited_page("TearDown", wiki_page)
            if teardown is not None:
                string_io=self._write_pathname_to_IO(self,string_io,teardown, wiki_page,"teardown")
            if include_suite_setup:
                suite_teardown: WikiPage = self._page_crawler.get_inherited_page(SuiteResponder.SUITE_TEARDOWN_NAME, wiki_page)
                if suite_teardown is not None:
                    string_io=self._write_pathname_to_IO(self,string_io,suite_teardown, wiki_page,"teardown")

        self._page_data.set_content(string_io.getvalue())
        return self._page_data.get_html()
    
    def _check_page_attribute(self, attribute: str) -> bool:
        return self._page_data.has_attribute(attribute)
          
    """
    @param type: can be "setup" or "teardown" 
    """
    def _write_pathname_to_IO(self,string_io: StringIO,search_page: WikiPage, wiki_page: WikiPage, type: str) -> StringIO:
        page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(search_page)
        page_path_name: str = self._path_parser.render(page_path)
        string_io.writelines(["!include -",type," .", page_path_name, "\n"])
