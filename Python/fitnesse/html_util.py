from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        string_io = HtmlUtil._do_suit_setup(page_data, include_suite_setup, page_crawler, wiki_page, path_parser, string_io)

        string_io.writelines([page_data.get_content()])
        
        string_io = HtmlUtil._do_teardown(page_data, include_suite_setup, page_crawler, wiki_page, path_parser, string_io)

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()

    @staticmethod
    def _do_suit_setup(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, wiki_page: WikiPage, path_parser: PathParser, string_io: StringIO) -> StringIO:
        if page_data.has_attribute("Test"):
            if include_suite_setup:
                suite_setup: WikiPage = HtmlUtil._get_inherited_page(page_crawler, SuiteResponder.SUITE_SETUP_NAME, wiki_page)
                if suite_setup is not None:
                    page_path: WikiPagePath = HtmlUtil._get_page_crawler(suite_setup)
                    page_path_name: str = HtmlUtil._do_render(path_parser, page_path) 
                    string_io.writelines(["!include -setup .", page_path_name, "\n"])

            setup: WikiPage = HtmlUtil._get_inherited_page(page_crawler, "SetUp", wiki_page)
            if setup is not None:
                setup_path: WikiPagePath = HtmlUtil._get_page_crawler(setup)
                setup_path_name: str = HtmlUtil._do_render(path_parser, setup_path) 
                string_io.writelines(["!include -setup .", setup_path_name, "\n"])
        return string_io

    @staticmethod
    def _do_teardown(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, wiki_page: WikiPage, path_parser: PathParser, string_io: StringIO) -> StringIO:
        if page_data.has_attribute("Test"):
            teardown: WikiPage = HtmlUtil._get_inherited_page(page_crawler, "TearDown", wiki_page)
            if teardown is not None:
                tear_down_path: WikiPagePath = HtmlUtil._get_page_crawler(teardown)
                tear_down_path_name: str = HtmlUtil._do_render(path_parser, tear_down_path) 
                string_io.writelines(["!include -teardown .", tear_down_path_name, "\n"])
            if include_suite_setup:
                suite_teardown: WikiPage = HtmlUtil._get_inherited_page(page_crawler, SuiteResponder.SUITE_TEARDOWN_NAME, wiki_page)
                if suite_teardown is not None:
                    page_path: WikiPagePath = HtmlUtil._get_page_crawler(suite_teardown)
                    page_path_name: str = HtmlUtil._do_render(path_parser, page_path) 
                    string_io.writelines(["!include -teardown .", page_path_name, "\n"])
        return string_io


    @staticmethod
    def _get_inherited_page(page_crawler: PageCrawlerImpl, str_name: str, wiki_page: WikiPage) -> WikiPage:
        return page_crawler.get_inherited_page(str_name, wiki_page)

    @staticmethod
    def _get_page_crawler(wiki_page: WikiPage) -> WikiPagePath:
        return wiki_page.get_page_crawler().get_full_path(wiki_page)

    @staticmethod
    def _do_render(path_parser: PathParser, page_path: WikiPagePath) -> str:
        return path_parser.render(page_path)