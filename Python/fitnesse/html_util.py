from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData
from fitnesse.context import PathParser, WikiPage, WikiPagePath

class HtmlUtil:

    @staticmethod
    def _write_pagepath_to_io(page: WikiPage,
                              string_io: StringIO,
                              pparser: PathParser,
                              comment: str):
        page_crawler: WikiPagePath = page.get_page_crawler()
        page_path = page_crawler.get_full_path(page)
        page_path_name: str = pparser.render(page_path)
        string_io.writelines([f"{comment}", page_path_name, "\n"])

    @staticmethod
    def write_pagepath_to_io(page: WikiPage,
                             string_io: StringIO,
                             pparser: PathParser,
                             comment: str):
        if page is not None:
            HtmlUtil._write_pagepath_to_io(page, string_io, pparser, comment)

    @staticmethod
    def testable_html(page_data: PageData,
                      include_suite_setup: bool,
                      page_crawler: PageCrawlerImpl,
                      path_parser: PathParser) -> str:

        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()

        if page_data.has_attribute("Test"):

            if include_suite_setup:
                pinfo = (SuiteResponder.SUITE_SETUP_NAME, wiki_page)
                suite_setup: WikiPage = page_crawler.get_inherited_page(pinfo)
                HtmlUtil.write_pagepath_to_io(suite_setup,
                                              string_io,
                                              path_parser,
                                              "!include -setup .")

            setup: WikiPage = page_crawler.get_inherited_page("SetUp",
                                                               wiki_page)
            HtmlUtil.write_pagepath_to_io(setup,
                                          string_io,
                                          path_parser,
                                          "!include -setup .")

            string_io.writelines([page_data.get_content()])

            teardown: WikiPage = page_crawler.get_inherited_page("TearDown",
                                                                  wiki_page)
            HtmlUtil.write_pagepath_to_io(teardown,
                                          string_io,
                                          path_parser,
                                          "!include -teardown .")

            if include_suite_setup:
                pinfo = (SuiteResponder.SUITE_TEARDOWN_NAME, wiki_page)
                suite_teardown: WikiPage = page_crawler.get_inherited_page(pinfo)
                HtmlUtil.write_pagepath_to_io(suite_teardown,
                                              string_io,
                                              path_parser,
                                              "!include -teardown .")

        else:
            string_io.writelines([page_data.get_content()])

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()
