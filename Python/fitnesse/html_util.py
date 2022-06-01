from io import StringIO
from typing import NamedTuple, Optional

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath

class NoLineError(Exception):
    pass

class NoPathNameError(Exception):
    pass
class TestItem(NamedTuple):
    include_suite_setup: Optional[bool]
    html_name: str
    suite_setup_name:  str


def get_path_name(wiki_page: WikiPage, test_item: TestItem, page_crawler : PageCrawlerImpl, path_parser: PathParser ) -> str:
    suite_setup: WikiPage = page_crawler.get_inherited_page(test_item.suite_setup_name, wiki_page)
    if suite_setup is not None:
        page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(suite_setup)
        page_path_name: str = path_parser.render(page_path)
    else:
        print(f"No path name for {test_item.suite_setup_name} ")
        raise NoPathNameError
        return None
    return page_path_name

def write_line(string_io: StringIO, wiki_page: WikiPage, test_item: TestItem, page_crawler : PageCrawlerImpl, path_parser: PathParser, include_suite_setup: bool) -> bool:
    if include_suite_setup is not None or include_suite_setup == test_item.include_suite_setup:
        path_name: str = get_path_name(wiki_page = wiki_page, test_item = test_item,  page_crawler = page_crawler, path_parser = path_parser)
        if path_name is not None:
            string_io.writelines([f"!include -{test_item.html_name} .", path_name, "\n"])
            return True
        else: 
            print(f"No line writen for {test_item.suite_setup_name} ")
            raise NoLineError
            return False
        


class HtmlUtil:
    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()
        test_items = [TestItem(True, "setup", SuiteResponder.SUITE_SETUP_NAME), 
                    TestItem(None, "setup", "SetUp"),
                    TestItem(None, "teardown", "TearDown"),
                    TestItem(True, "teardown", SuiteResponder.SUITE_TEARDOWN_NAME)]

        if page_data.has_attribute("Test"):
            for item in test_items:
                try:
                    write_line(string_io = string_io, include_suite_setup = include_suite_setup, test_item = item,  wiki_page = wiki_page, page_crawler = page_crawler, path_parser = path_parser)
                except NoLineError: 
                    pass
                except NoPathNameError:
                    pass
                   

        string_io.writelines([page_data.get_content()])
        page_data.set_content(string_io.getvalue())
        return page_data.get_html()

