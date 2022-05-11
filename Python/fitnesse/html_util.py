from dataclasses import dataclass
from io import StringIO
from typing import List, Optional

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


@dataclass
class Stage:
    typ: str
    page_name: Optional[str] = None
    include_options: list[str] = None

    def __post_init__(self):
        assert self.typ in ["suite", "content"]
        if self.include_options is None:
            self.include_options = []


class HtmlUtil:
    STAGES = [
        Stage('suite', SuiteResponder.SUITE_SETUP_NAME, ['setup']),
        Stage('suite', 'SetUp', ['setup']),
        Stage('content'),
        Stage('suite', 'TearDown', ['teardown']),
        Stage('suite', SuiteResponder.SUITE_TEARDOWN_NAME, ['teardown']),
    ]

    @staticmethod
    def get_inherited_path(wiki_page: WikiPage, page_crawler: PageCrawlerImpl, page_name: str) -> WikiPagePath:
        """Returns the full path of the page with the given name that is inherited from the given wiki_page"""
        inherited_page: WikiPage = page_crawler.get_inherited_page(page_name, wiki_page)
        if inherited_page is None:
            raise ValueError(f"There is not inherited page {page_name} for {wiki_page.get_name()}")
        return wiki_page.get_page_crawler().get_full_path(inherited_page)

    @staticmethod
    def include_options(page_path: WikiPagePath, path_parser: PathParser, string_io: StringIO, option: str):
        """Adds the statement '!include -option . <page_path_name>' to the string_io"""
        page_path_name: str = path_parser.render(page_path)
        string_io.writelines([f"!include {option} .", page_path_name, "\n"])
            
    @staticmethod
    def testable_html(
            page_data: PageData,
            include_suite_setup: bool,
            page_crawler: PageCrawlerImpl,
            path_parser: PathParser
    ) -> str:
        """
        Creates a string that contains a valid html page, usable for testing
        :param page_data: Page content
        :param include_suite_setup: Boolean argument whether to include suite setup statements at the start and end of
          tha return string (only if the page_data has a "Test" attribute, though)
        :param page_crawler: Page crawler needed to get the suite setup and teardown pages
        :param path_parser: Path parser needed to render the page path (for inherited pages, for example)
        :return: A string that contains a valid html page
        """
        stages = [Stage('content')]
        if page_data.has_attribute("Test"):
            stages.insert(0, Stage('suite', 'SetUp', ['setup']))
            stages.append(   Stage('suite', 'TearDown', ['teardown']))

            if include_suite_setup:
                stages.insert(0, Stage('suite',    SuiteResponder.SUITE_SETUP_NAME, ['setup']))
                stages.append(   Stage('suite', SuiteResponder.SUITE_TEARDOWN_NAME, ['teardown']))

        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()
                
        for stage in stages:
            if stage.typ == 'suite':
                page_path = HtmlUtil.get_inherited_path(wiki_page, page_crawler, stage.page_name)
                options: str = ' '.join('-' + i for i in stage.include_options)
                HtmlUtil.include_options(page_path, path_parser, string_io, options)
            elif stage.typ == 'content':
                string_io.writelines([page_data.get_content()])
            else:
                raise ValueError("Unknown stage type")

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()
