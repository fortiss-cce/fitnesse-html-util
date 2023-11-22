from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath

class TestType:
    SETUP: "SetUp"
    TEARDOWN: "TearDown"
class HtmlUtil:

    @staticmethod
    def get_Path(page_name: str, wiki_page: WikiPage):
        inherit_Page: WikiPage = page_crawler.get_inherited_page(page_name, wiki_page)
        if inherit_Page is not None:
            path: wiki_page.get_page_crawler().get_full_path(setup)
            path_name: str = path_parser.render(page_path)
            return path_name

    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                page_path_name = HtmlUtil.get_Path(wiki_page=wiki_page, page_name=SuiteResponder.SUITE_SETUP_NAME)
                string_io.writelines(["!include -setup .", page_path_name, "\n"])

            setup_path_name = HtmlUtil.get_Path(wiki_page=wiki_page, page_name=TestType.SETUP)
            string_io.writelines(["!include -setup .", page_path_name, "\n"])

        string_io.writelines([page_data.get_content()])
        if page_data.has_attribute("Test"):
            tear_down_path_name: str = HtmlUtil.get_Path(wiki_page=wiki_page, page_name=TestType.TEARDOWN)
            string_io.writelines(["!include -teardown .", tear_down_path_name, "\n"])
            if include_suite_setup:
                page_path_name: str = HtmlUtil.get_Path(wiki_page=wiki_page, page_name=SuiteResponder.SUITE_TEARDOWN_NAME)
                string_io.writelines(["!include -teardown .", page_path_name, "\n"])

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()

   