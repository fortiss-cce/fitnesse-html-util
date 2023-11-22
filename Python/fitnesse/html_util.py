from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    wiki_page: WikiPage
    string_io: StringIO
    page_crawler: PageCrawlerImpl
    path_parser: PathParser
    

    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        HtmlUtil.wiki_page = page_data.get_wiki_page()
        HtmlUtil.string_io = StringIO()
        HtmlUtil.page_crawler = page_crawler
        HtmlUtil.path_parser = path_parser

        if page_data.has_attribute("Test"):
            _write_setup(include_suite_setup)
        HtmlUtil.string_io.writelines([page_data.get_content()])
        if page_data.has_attribute("Test"):
            _write_teardown(include_suite_setup)
        page_data.set_content(HtmlUtil.string_io.getvalue())
        return page_data.get_html()
    
    def _write_setup(include_suite_setup: bool):
        if include_suite_setup:
            _write_page(SuiteResponder.SUITE_SETUP_NAME, "setup")
        _write_page("SetUp", "setup")

    def _write_teardown(include_suite_setup: bool):
        _write_page("TearDown", "teardown")
        if include_suite_setup:
            _write_page(SuiteResponder.SUITE_TEARDOWN_NAME, "teardown")

    def _write_page(page_name : str, option : str): 
        page: WikiPage = HtmlUtil.page_crawler.get_inherited_page(page_name)
        if page is not None: 
            _write_path(page, option)
    
    def _write_path(page : WikiPage, option : str):
        page_path: WikiPagePath = HtmlUtil.wiki_page.get_page_crawler().get_full_path(page)
        page_path_name: str = HtmlUtil.path_parser.render(page_path)
        HtmlUtil.string_io.writelines(["!include -", option, " .", page_path_name, "\n"])
