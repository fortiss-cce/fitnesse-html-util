from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    @staticmethod
    def get_inherited_path(wiki_page: WikiPage, page_crawler: PageCrawlerImpl, page_name: str) -> WikiPagePath:
        """Returns the full path of the page with the given name that is inherited from the given wiki_page"""
        inherited_page: WikiPage = page_crawler.get_inherited_page(page_name, wiki_page)
        if inherited_page is None:
            raise ValueError(f"There is not inherited page {page_name} for {wiki_page.get_name()}")
        return wiki_page.get_page_crawler().get_full_path(inherited_page)

    @staticmethod
    def include_setup(page_path: WikiPagePath, path_parser: PathParser, string_io: StringIO):
        """Adds the statement '!include -setup . <page_path_name>' to the string_io"""
        HtmlUtil._add_include_statement(page_path, path_parser, string_io, '-setup')

    @staticmethod
    def include_teardown(page_path: WikiPagePath, path_parser: PathParser, string_io: StringIO):
        """Adds the statement '!include -teardown . <page_path_name>' to the string_io"""
        HtmlUtil._add_include_statement(page_path, path_parser, string_io, '-teardown')

    @staticmethod
    def _add_include_statement(page_path: WikiPagePath, path_parser: PathParser, string_io: StringIO, statement: str):
        page_path_name: str = path_parser.render(page_path)
        string_io.writelines([f"!include {statement} .", page_path_name, "\n"])

    @staticmethod
    def testable_html(page_data: PageData,
                      include_suite_setup: bool,
                      page_crawler: PageCrawlerImpl,
                      path_parser: PathParser) -> str:
        """
        Creates a string that contains a valid html page, usable for testing
        :param page_data: Page content
        :param include_suite_setup: Boolean argument whether to include suite setup statements at the start and end of
          tha return string (only if the page_data has a "Test" attribute, though)
        :param page_crawler: Page crawler needed to get the suite setup and teardown pages
        :param path_parser: Path parser needed to render the page path (for inherited pages, for example)
        :return: A string that contains a valid html page
        """

        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                suite_setup_path = HtmlUtil.get_inherited_path(wiki_page, page_crawler, SuiteResponder.SUITE_SETUP_NAME)
                HtmlUtil.include_setup(suite_setup_path, path_parser, string_io)

            setup_path = HtmlUtil.get_inherited_path(wiki_page, page_crawler, "SetUp")
            HtmlUtil.include_setup(setup_path, path_parser, string_io)

        string_io.writelines([page_data.get_content(), '\n'])

        if page_data.has_attribute("Test"):
            tear_down_path: WikiPagePath = HtmlUtil.get_inherited_path(wiki_page, page_crawler, "TearDown")
            HtmlUtil.include_teardown(tear_down_path, path_parser, string_io)

            if include_suite_setup:
                suite_teardown_path: WikiPagePath = HtmlUtil.get_inherited_path(wiki_page, page_crawler,
                                                                                SuiteResponder.SUITE_TEARDOWN_NAME)
                HtmlUtil.include_teardown(suite_teardown_path, path_parser, string_io)

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()
