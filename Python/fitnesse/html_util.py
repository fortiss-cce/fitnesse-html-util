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
                HtmlUtil.suite_setup(page_crawler, wiki_page, string_io, path_parser)

            HtmlUtil.setup(page_crawler, wiki_page, string_io, path_parser)

            string_io.writelines([page_data.get_content()])

            HtmlUtil.teardown(page_crawler, wiki_page, string_io, path_parser)
            if include_suite_setup:
                HtmlUtil.suite_teardown(page_crawler, wiki_page, string_io, path_parser)

        else:
            string_io.writelines([page_data.get_content()])           

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()


    @staticmethod
    def suite_setup(page_crawler, wiki_page, string_io, path_parser):
        suite_setup: WikiPage = page_crawler.get_inherited_page(SuiteResponder.SUITE_SETUP_NAME, wiki_page)
        if suite_setup is not None:
            HtmlUtil.write(wiki_page, string_io, path_parser, path=suite_setup, mode=Mode.SETUP)

    @staticmethod
    def setup(page_crawler, wiki_page, string_io, path_parser):
        setup: WikiPage = page_crawler.get_inherited_page("SetUp", wiki_page)
        if setup is not None:
            HtmlUtil.write(wiki_page, string_io, path_parser, path=setup, mode=Mode.SETUP)
            
    @staticmethod
    def teardown(page_crawler, wiki_page, string_io, path_parser):
        teardown: WikiPage = page_crawler.get_inherited_page("TearDown", wiki_page)
        if teardown is not None:
            HtmlUtil.write(wiki_page, string_io, path_parser, path=teardown, mode=Mode.TEARDOWN)
            
    @staticmethod
    def suite_teardown(page_crawler, wiki_page, string_io, path_parser):
        suite_teardown: WikiPage = page_crawler.get_inherited_page(SuiteResponder.SUITE_TEARDOWN_NAME, wiki_page)
        if suite_teardown is not None:
            HtmlUtil.write(wiki_page, string_io, path_parser, path=suite_teardown, mode=Mode.TEARDOWN)

    @staticmethod
    def write(wiki_page, string_io, path_parser, path: WikiPage, mode: Mode):
        page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(path)
        page_path_name: str = path_parser.render(page_path)
        string_io.writelines([f"!include -{mode.value} .", page_path_name, "\n"])
