from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                HtmlUtil.append_include_command(page_crawler, path_parser, string_io, wiki_page, SuiteResponder.SUITE_SETUP_NAME, 'setup')
            HtmlUtil.append_include_command(page_crawler, path_parser, string_io, wiki_page, 'SetUp', 'setup')

        string_io.writelines([page_data.get_content()])
        if page_data.has_attribute("Test"):
            HtmlUtil.append_include_command(page_crawler, path_parser, string_io, wiki_page, 'TearDown',
                                 'teardown')
            if include_suite_setup:
                HtmlUtil.append_include_command(page_crawler, path_parser, string_io, wiki_page, SuiteResponder.SUITE_TEARDOWN_NAME,
                                     'teardown')

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()

    @staticmethod
    def append_include_command(page_crawler, path_parser, string_io, wiki_page, page_name, include_command: str):
        suite_setup: WikiPage = page_crawler.get_inherited_page(page_name, wiki_page)
        if suite_setup is not None:
            page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(suite_setup)
            page_path_name: str = path_parser.render(page_path)
            string_io.writelines([f"!include -{include_command} .", page_path_name, "\n"])
