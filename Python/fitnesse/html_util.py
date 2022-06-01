from io import StringIO
from re import A
from stringprep import in_table_c21_c22

from fitnesse.context import SuiteResponder, PageCrawlerImpl, PageData, PathParser, WikiPage, WikiPagePath


# QUESTIONS
# 


class HtmlUtil:
    """ FILL IN CLASS DESCRIPTION. """

    def __init__(self, page_data : PageData, path_parser : PathParser) -> None:
        self.page_data = page_data
        self.wiki_page = self.page_data.get_wiki_page()
        self.path_parser = path_parser
        self.string_io = StringIO()


    def page_action_function(self, suite, action : str) -> None: 
        """ Setup or teardown. Specify as input with string. """

        assert action in ['setup', 'teardown']

        page_path: WikiPagePath = self.wiki_page.get_page_crawler().get_full_path(suite)
        page_path_name: str = self.path_parser.render(page_path)
        self.string_io.writelines([f"!include -{action} .", page_path_name, "\n"])

    # @staticmethod
    def testable_html(self, include_suite_setup: bool, page_crawler: PageCrawlerImpl) -> str:
        #wiki_page: WikiPage = page_data.get_wiki_page()
        # string_io: StringIO = StringIO()

        if self.page_data.has_attribute("Test"):
            if include_suite_setup:
                suite_setup: WikiPage = page_crawler.get_inherited_page(SuiteResponder.SUITE_SETUP_NAME, self.wiki_page)
                # if suite_setup is not None:
                    #page_path: WikiPagePath = wiki_page.get_page_crawler().get_full_path(suite_setup)
                    #page_path_name: str = path_parser.render(page_path)
                    #string_io.writelines(["!include -setup .", page_path_name, "\n"])
                #self.setup_function(suite_setup = suite_setup)
                self.page_action_function(suite = suite_setup, action = 'setup')
                    

            setup: WikiPage = page_crawler.get_inherited_page("SetUp", self.wiki_page)
            #if setup is not None:
                # setup_path: WikiPagePath = self.wiki_page.get_page_crawler().get_full_path(setup)
                #setup_path_name: str = self.path_parser.render(setup_path)
                #self.string_io.writelines(["!include -setup .", setup_path_name, "\n"])
            self.page_action_function(suite = setup, action = 'setup')

            self.string_io.writelines([self.page_data.get_content()])

            teardown: WikiPage = page_crawler.get_inherited_page("TearDown", self.wiki_page)
            #if teardown is not None:
                #tear_down_path: WikiPagePath = self.wiki_page.get_page_crawler().get_full_path(teardown)
                #tear_down_path_name: str = self.path_parser.render(tear_down_path)
                #self.string_io.writelines(["!include -teardown .", tear_down_path_name, "\n"])
            #self.teardown_function(suite_teardown = teardown)
            self.page_action_function(suite = teardown, action = 'teardown')
            if include_suite_setup:
                suite_teardown: WikiPage = page_crawler.get_inherited_page(SuiteResponder.SUITE_TEARDOWN_NAME, self.wiki_page)
            #    if suite_teardown is not None:
                    #page_path: WikiPagePath = self.wiki_page.get_page_crawler().get_full_path(suite_teardown)
                    #page_path_name: str = self.path_parser.render(page_path)
                    #self.string_io.writelines(["!include -teardown .", page_path_name, "\n"])
                #self.teardown_function(suite_teardown = suite_teardown)
                self.page_action_function(suite = suite_teardown, action = 'teardown')

        #self.string_io.writelines([self.page_data.get_content()])
        #if self.page_data.has_attribute("Test"): # WHY TWICE?
            #teardown: WikiPage = page_crawler.get_inherited_page("TearDown", self.wiki_page)
            #if teardown is not None:
                #tear_down_path: WikiPagePath = self.wiki_page.get_page_crawler().get_full_path(teardown)
                #tear_down_path_name: str = self.path_parser.render(tear_down_path)
                #self.string_io.writelines(["!include -teardown .", tear_down_path_name, "\n"])
            #self.teardown_function(suite_teardown = teardown)
            #self.action_function(suite = teardown, action = 'teardown')
            #if include_suite_setup:
             #   suite_teardown: WikiPage = page_crawler.get_inherited_page(SuiteResponder.SUITE_TEARDOWN_NAME, self.wiki_page)
            #    if suite_teardown is not None:
                    #page_path: WikiPagePath = self.wiki_page.get_page_crawler().get_full_path(suite_teardown)
                    #page_path_name: str = self.path_parser.render(page_path)
                    #self.string_io.writelines(["!include -teardown .", page_path_name, "\n"])
                #self.teardown_function(suite_teardown = suite_teardown)
              #  self.action_function(suite = suite_teardown, action = 'teardown')

        self.page_data.set_content(self.string_io.getvalue())
        return self.page_data.get_html()
