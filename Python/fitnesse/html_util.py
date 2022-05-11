from io import StringIO
from typing import Tuple

from fitnesse.context import (
    SuiteResponder,
    PageCrawlerImpl,
    PageData,
    PathParser,
    WikiPage,
    WikiPagePath,
)


class HtmlUtil:
    @staticmethod
    def _add_subpage(
        object_data: Tuple[PageCrawlerImpl, PathParser, WikiPage, StringIO],
        command: str,
        subpage_name: str,
    ):
        page_crawler, path_parser, wiki_page, string_io = object_data
        suite: WikiPage = page_crawler.get_inherited_page(subpage_name, wiki_page)
        if suite is not None:
            page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(suite)
            page_path_name: str = path_parser.render(page_path)
            string_io.writelines([f"!include -{command} .", page_path_name, "\n"])

    @staticmethod
    def testable_html(
        page_data: PageData,
        include_suite_setup: bool,
        page_crawler: PageCrawlerImpl,
        path_parser: PathParser,
    ) -> str:
        if page_data is None:
            raise ValueError("Page Data missing")
        if page_crawler is None:
            raise ValueError("Page Crawler is missing")
        if path_parser is None:
            raise ValueError("Path Parser is missing")

        wiki_page: WikiPage = page_data.get_wiki_page()
        if wiki_page is None:
            raise ValueError("Creating wiki page failed")
        string_io: StringIO = StringIO()

        object_data: Tuple[PageCrawlerImpl, PathParser, WikiPage, StringIO] = (
            page_crawler,
            path_parser,
            wiki_page,
            string_io,
        )

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                HtmlUtil._add_subpage(
                    object_data,
                    "setup",
                    SuiteResponder.SUITE_SETUP_NAME,
                )
            HtmlUtil._add_subpage(
                object_data,
                "setup",
                "SetUp",
            )

            string_io.writelines([page_data.get_content()])
            HtmlUtil._add_subpage(
                object_data,
                "teardown",
                "TearDown",
            )
            if include_suite_setup:
                HtmlUtil._add_subpage(
                    object_data,
                    "teardown",
                    SuiteResponder.SUITE_TEARDOWN_NAME,
                )

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()
