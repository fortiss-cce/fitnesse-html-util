from io import StringIO
from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


class HtmlUtil:

    @staticmethod
    def testable_html(page_data: PageData, include_suite_setup: bool, page_crawler: PageCrawlerImpl, path_parser: PathParser) -> str:
        # Bail out early if test attribute does not exist
        if not page_data.has_attribute("Test"):
            string_io.writelines([page_data.get_content()])
            page_data.set_content(string_io.getvalue())
            return page_data.get_html()

        wiki_page: WikiPage = page_data.get_wiki_page()
        wiki_page_crawler: PageCrawlerImpl = wiki_page.get_page_crawler()
        string_io: StringIO = StringIO()

        # Helper to write a page
        def write_page(command: str, page_name: str, context: WikiPage):
            suite_setup: WikiPage = page_crawler.get_inherited_page(page_name, context)
            if suite_setup is None:
                return
            page_path: WikiPagePath = wiki_page_crawler.get_full_path(suite_setup)
            page_path_name: str = path_parser.render(page_path)
            string_io.writelines(["!include ", command, " .", page_path_name, "\n"])


        # Write suite setup
        if include_suite_setup:
            write_page("-setup", SuiteResponder.SUITE_SETUP_NAME, wiki_page)

        # Write page content 
        write_page("-setup", "SetUp", wiki_page)
        string_io.writelines([page_data.get_content()])
        write_page("-teardown", "TearDown", wiki_page)

        # Write suite teardown
        if include_suite_setup:
            write_page("-teardown", SuiteResponder.SUITE_TEARDOWN_NAME, wiki_page)

        # Set the page data
        page_data.set_content(string_io.getvalue())
        return page_data.get_html()
