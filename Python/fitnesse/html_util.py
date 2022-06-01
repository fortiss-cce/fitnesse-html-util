from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:
    def __init__(self, page_data: PageData):
        self.page_data: PageData = page_data
    
    @staticmethod
    def write_command_to_io(string_io:StringIO, wiki_page:WikiPage, path_parser:PathParser, command:str, specific_wiki_page:WikiPage):
        page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(specific_wiki_page)
        page_path_name: str = path_parser.render(page_path)
        string_io.writelines([f"!include -{command} .", page_path_name, "\n"])

    @staticmethod
    def get_page_and_write_command_to_io(page_crawler: PageCrawlerImpl, wiki_page: WikiPage, string_io: StringIO, path_parser: PathParser, page_name:str, command:str):
        teardown: WikiPage = page_crawler.get_inherited_page(page_name, wiki_page)
        if teardown is not None:
            HtmlUtil.write_command_to_io(string_io, wiki_page, path_parser, command, teardown)
        
    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        variable_dict = {"setup": [SuiteResponder.SUITE_SETUP_NAME, "SetUp"], "teardown": [SuiteResponder.SUITE_TEARDOWN_NAME, "TearDown"]}

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                HtmlUtil.get_page_and_write_command_to_io(page_crawler, wiki_page, string_io, path_parser, SuiteResponder.SUITE_SETUP_NAME, "setup")
            HtmlUtil.get_page_and_write_command_to_io(page_crawler, wiki_page, string_io, path_parser, "SetUp", "setup")

        string_io.writelines([page_data.get_content()])

        if page_data.has_attribute("Test"):
            if include_suite_setup:
                HtmlUtil.get_page_and_write_command_to_io(page_crawler, wiki_page, string_io, path_parser, SuiteResponder.SUITE_TEARDOWN_NAME, "teardown")
            HtmlUtil.get_page_and_write_command_to_io(page_crawler, wiki_page, string_io, path_parser, "TearDown", "teardown")

        page_data.set_content(string_io.getvalue())

        return page_data.get_html()
