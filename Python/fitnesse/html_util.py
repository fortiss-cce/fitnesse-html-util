from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    def write_pagepath_to_IO(page: WikiPage, string_io: StringIO, comment: str):
        page_crawler: WikiPagePath = wiki_page.get_page_crawler()
        page_path: page_crawler.get_full_path(page)
        page_path_name: str = path_parser.render(page_path)
        string_io.writelines([f"{comment}", page_path_name, "\n"])

    @staticmethod
    def testable_html(page_data: PageData,
                      include_suite_setup: bool,
                      page_crawler: PageCrawlerImpl,
                      path_parser: PathParser) -> str:

        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                suite_setup: WikiPage = page_crawler.get_inherited_page(SuiteResponder.SUITE_SETUP_NAME, wiki_page)
                if suite_setup is not None:
                    page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(suite_setup)
                    page_path_name: str = path_parser.render(page_path)
                    string_io.writelines(["!include -setup .", page_path_name, "\n"])

            setup: WikiPage = page_crawler.get_inherited_page("SetUp", wiki_page)
            if setup is not None:
                setup_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(setup)
                setup_path_name: str = path_parser.render(setup_path)
                string_io.writelines(["!include -setup .", setup_path_name, "\n"])

        string_io.writelines([page_data.get_content()])

        if page_data.has_attribute("Test"):
            teardown: WikiPage = page_crawler.get_inherited_page("TearDown", wiki_page)
            if teardown is not None:
                tear_down_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(teardown)
                tear_down_path_name: str = path_parser.render(tear_down_path)
                string_io.writelines(["!include -teardown .", tear_down_path_name, "\n"])
            if include_suite_setup:
                suite_teardown: WikiPage = page_crawler.get_inherited_page(SuiteResponder.SUITE_TEARDOWN_NAME, wiki_page)
                if suite_teardown is not None:
                    page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(suite_teardown)
                    page_path_name: str = path_parser.render(page_path)
                    string_io.writelines(["!include -teardown .", page_path_name, "\n"])

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()
