from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    # Should everything remain static?
    _wiki_page = WikiPage   # Temp
    _page_data = PageData() # Cannot instantiate abstract class... needed for exercise...
    _string_io = StringIO() # Temp

    # string_io and wiki_page could be attributes of the class...
    @staticmethod
    def whatever_this_does(page_crawler, suit_responder, path_parser, phase_type):
        suite_setup: WikiPage = page_crawler.get_inherited_page(suit_responder, HtmlUtil._wiki_page)
        if (suite_setup is not None):
            page_path: WikiPagePath = HtmlUtil._wiki_page.get_page_crawler().get_full_path(suite_setup)
            page_path_name: str = path_parser.render(page_path)
            HtmlUtil._string_io.writelines([f"!include -{phase_type} .", page_path_name, "\n"])


    @staticmethod
    def setup_phase(include_suite_setup, page_crawler, path_parser):
        if (HtmlUtil._page_data.has_attribute("Test")):
            if (include_suite_setup):
                HtmlUtil.whatever_this_does(page_crawler, SuiteResponder.SUITE_SETUP_NAME, path_parser, "setup")
            HtmlUtil.whatever_this_does(page_crawler, "SetUp", path_parser, "setup")


    @staticmethod
    def teardown_phase(include_suite_setup, page_crawler, path_parser):
        if (HtmlUtil._page_data.has_attribute("Test")):
            HtmlUtil.whatever_this_does(page_crawler, "TearDown", path_parser, "teardown")
            if (include_suite_setup):
                HtmlUtil.whatever_this_does(page_crawler, SuiteResponder.SUITE_TEARDOWN_NAME, path_parser, "teardown")


    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        # Temporarily setup static varilables (assumed overwritten each time)
        HtmlUtil._wiki_page = page_data.get_wiki_page()
        HtmlUtil._page_data = page_data
        HtmlUtil._string_io = StringIO()

        HtmlUtil.setup_phase(include_suite_setup, page_crawler, path_parser)
        HtmlUtil._string_io.writelines([HtmlUtil._page_data.get_content()])
        HtmlUtil.teardown_phase(include_suite_setup, page_crawler, path_parser)

        HtmlUtil._page_data.set_content(HtmlUtil._string_io.getvalue())
        return HtmlUtil._page_data.get_html()
