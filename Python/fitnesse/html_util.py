from io import StringIO

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath

class Stage:
    typ: str
    page_name: Optional[str]
    include_options: list[str]

    def __init__(self, typ: str, page_name: Optional[str] = None, include_options: list[str] = []):
        assert self.typ in ('content', 'suite')
        self.typ = typ
        self.page_name = page_name
        self.include_options = include_options.copy()

class HtmlUtil:
    STAGES = [
        Stage('suite', 'setup', SuiteResponder.SUITE_SETUP_NAME),
        Stage('suite', 'setup', 'SetUp'),
        Stage('content'),
        Stage('suite', 'teardown', 'TearDown'),
        Stage('suite', 'teardown', SuiteResponder.SUITE_TEARDOWN_NAME),
    ]

    @staticmethod
    def _write_suite(page_crawler, wiki_page, stage):
        page: WikiPage = page_crawler.get_inherited_page(name, wiki_page)
        if page is None: return
        
        page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(stage.page_name)
        page_path_name: str = path_parser.render(page_path)
        options: str = ' '.join('-' + i for i in stage.include_options)
        
        string_io.writelines([f"!include {options} .", page_path_name, "\n"])
            
    @staticmethod
    def testable_html(
            page_data: PageData,
            include_suite_setup: bool,
            page_crawler: PageCrawlerImpl,
            path_parser: PathParser
    ) -> str:

        stages = [Stage('content')]
        if page_data.has_attribute("Test"):
            stages.insert(0, Stage('suite', 'setup',    'SetUp'))
            stages.append(   Stage('suite', 'teardown', 'TearDown'))

            if include_suite_setup:
                stages.insert(0, Stage('suite', 'setup',    SuiteResponder.SUITE_SETUP_NAME))
                stages.append(   Stage('suite', 'teardown', SuiteResponder.SUITE_TEARDOWN_NAME))

        wiki_page: WikiPage = page_data.get_wiki_page()
        string_io: StringIO = StringIO()
                
        for stage in stages:
            if stage.typ == 'suite':
                _write_suite(page_crawler, wiki_page, stage)
            elif stage.typ == 'content':
                string_io.writelines([page_data.get_content()])
            else:
                assert False

        page_data.set_content(string_io.getvalue())
        return page_data.get_html()
