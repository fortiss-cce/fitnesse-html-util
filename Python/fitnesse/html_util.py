from io import StringIO
from enum import Enum

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath

class Mode(Enum):
    TEARDOWN = "teardown"
    SETUP = "setup"


class HtmlUtil:

    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                HtmlUtil._suite_setup(page_crawler, wiki_page, string_io, path_parser)

            HtmlUtil._setup(page_crawler, wiki_page, string_io, path_parser)

            string_io.writelines([page_data.get_content()])

            HtmlUtil._teardown(page_crawler, wiki_page, string_io, path_parser)
            if include_suite_setup:
                HtmlUtil._suite_teardown(page_crawler, wiki_page, string_io, path_parser)

        else:
            string_io.writelines([page_data.get_content()])           

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()


    @staticmethod
    def _suite_setup(page_crawler, wiki_page, string_io, path_parser):
        HtmlUtil._write_page(page_crawler, wiki_page, string_io, path_parser, SuiteResponder.SUITE_SETUP_NAME, Mode.SETUP)

    @staticmethod
    def _suite_teardown(page_crawler, wiki_page, string_io, path_parser):
        HtmlUtil._write_page(page_crawler, wiki_page, string_io, path_parser, SuiteResponder.SUITE_TEARDOWN_NAME, Mode.TEARDOWN)

    @staticmethod
    def _setup(page_crawler, wiki_page, string_io, path_parser):
        HtmlUtil._write_page(page_crawler, wiki_page, string_io, path_parser, "SetUp", Mode.SETUP)
            
    @staticmethod
    def _teardown(page_crawler, wiki_page, string_io, path_parser):
        HtmlUtil._write_page(page_crawler, wiki_page, string_io, path_parser, "TearDown", Mode.TEARDOWN)
        
    @staticmethod
    def _write_page(page_crawler, wiki_page, string_io, path_parser, page_name, mode):
        path: WikiPage = page_crawler.get_inherited_page(page_name, wiki_page)
        HtmlUtil._write(wiki_page, string_io, path_parser, path=path, mode=mode)
        
    @staticmethod
    def _write(wiki_page, string_io, path_parser, path: WikiPage, mode: Mode):
        if path is not None:
            page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(path)
            page_path_name: str = path_parser.render(page_path)
            string_io.writelines([f"!include -{mode.value} .", page_path_name, "\n"])
