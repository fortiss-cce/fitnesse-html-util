from fitnesse.context import SuiteResponder
from fitnesse.html_util import HtmlUtil
from tests.conftest import WikiPage, PageCrawler, PathParser, PageCrawlerImpl


def test_testable_html(wiki_page: WikiPage, path_parser: PathParser, page_crawler: PageCrawlerImpl):
    root: WikiPage = wiki_page.make_root("RooT")
    crawler: PageCrawler = root.get_page_crawler()
    crawler.add_page(root, path_parser.parse("SetUp"), "setup")
    crawler.add_page(root, path_parser.parse("TearDown"), "teardown")
    page: WikiPage = crawler.add_page(root, path_parser.parse("TestPage"), "the content")

    html: str = HtmlUtil.testable_html(page.get_data(), False, page_crawler, path_parser)
    assert ".SetUp" in html
    assert "setup" in html
    assert ".TearDown" in html
    assert "teardown" in html
    assert "the content" in html
    assert "<p>" in html

def test_testable_html_2(wiki_page: WikiPage, path_parser: PathParser, page_crawler: PageCrawlerImpl):
    root: WikiPage = wiki_page.make_root("RooT")
    crawler: PageCrawler = root.get_page_crawler()
    crawler.add_page(root, path_parser.parse("SetUp"), "setup")
    crawler.add_page(root, path_parser.parse(SuiteResponder.SUITE_SETUP_NAME), "setup")
    crawler.add_page(root, path_parser.parse(SuiteResponder.SUITE_TEARDOWN_NAME), "teardown")
    crawler.add_page(root, path_parser.parse("TearDown"), "teardown")
    page: WikiPage = crawler.add_page(root, path_parser.parse("TestPage"), "the content")

    html: str = HtmlUtil.testable_html(page.get_data(), True, page_crawler, path_parser)
    assert ".SetUp" in html
    assert ".SuiteSetUp" in html
    assert "setup" in html
    assert ".TearDown" in html
    assert ".SuiteTearDown" in html
    assert "teardown" in html
    assert "the content" in html
    assert "<p>" in html
