from io import StringIO
import enum

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class Reason(enum.Enum):
    Setup = 1
    Teardown = 2

class HtmlUtil:

    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl,
                      path_parser: PathParser) -> str:
        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if page_data.has_attribute("Test"):
            HtmlUtil._suite_setup(include_suite_setup, page_crawler, wiki_page, path_parser, string_io,
                                  SuiteResponder.SUITE_SETUP_NAME, Reason.Setup)
            HtmlUtil._setup(wiki_page,path_parser, page_crawler, string_io, Reason.Setup)

        string_io.writelines([page_data.get_content()])
        if page_data.has_attribute("Test"):
            HtmlUtil._setup(wiki_page, path_parser, page_crawler, string_io, Reason.Teardown)
            HtmlUtil._suite_setup(include_suite_setup, page_crawler, wiki_page, path_parser , string_io,
                                  SuiteResponder.SUITE_TEARDOWN_NAME, Reason.Teardown)
        page_data.set_content(string_io.getvalue())
        return page_data.get_html()


    @staticmethod
    def _write_page_path_name(wiki_page: WikiPage, path_parser: PathParser, string_io: StringIO,
                              page: WikiPage, reason: Reason):
        page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(page)
        page_path_name: str = path_parser.render(page_path)
        if reason == Reason.Setup:
            string_io.writelines(["!include -setup .", page_path_name, "\n"])
        elif reason == Reason.Teardown:
            string_io.writelines(["!include -teardown .", page_path_name, "\n"])
        else:
            raise "Reason Unknown"

    @staticmethod
    def _suite_setup(include_suite_setup: bool, page_crawler: PageCrawlerImpl, wiki_page: WikiPage,
                     path_parser: PathParser, string_io: StringIO, suite_responder: SuiteResponder, reason: Reason):
        if include_suite_setup:
            suite: WikiPage = page_crawler.get_inherited_page(suite_responder, wiki_page)
            if suite is not None:
                HtmlUtil._write_page_path_name(wiki_page, path_parser, string_io, suite, reason)

    @staticmethod
    def _setup(wiki_page: WikiPage, path_parser: PathParser, page_crawler: PageCrawlerImpl, string_io: StringIO,
               reason: Reason):
        if reason == Reason.Setup:
            setup: WikiPage = page_crawler.get_inherited_page("SetUp", wiki_page)
        elif reason == Reason.Teardown:
            setup: WikiPage = page_crawler.get_inherited_page("TearDown", wiki_page)
        else:
            raise "Reason Unknown"
        if setup is not None:
            HtmlUtil._write_page_path_name(wiki_page, path_parser, string_io, setup, reason)