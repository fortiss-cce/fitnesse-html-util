from fitnesse.html_util import HtmlUtil
from tests.conftest import WikiPage, PageCrawler, PathParser, PageCrawlerImpl, PageData
import typing


def test_testable_html(wiki_page: WikiPage, path_parser: PathParser, page_crawler: PageCrawlerImpl):
    root: WikiPage = wiki_page.make_root("RooT")
    crawler: PageCrawler = root.get_page_crawler()
    crawler.add_page(root, path_parser.parse("SetUp"), "setup")
    crawler.add_page(root, path_parser.parse("TearDown"), "teardown")
    page: WikiPage = crawler.add_page(root, path_parser.parse("TestPage"), "the content")

    Pages = {
        page.get_data(),
        False,
        page_crawler,
        path_parser
    }

    HtmlUtilInst = HtmlUtil()
    html: str = HtmlUtilInst.testable_html(pages=Pages)
    assert ".SetUp" in html
    assert "setup" in html
    assert ".TearDown" in html
    assert "teardown" in html
    assert "the content" in html
    assert "<p>" in html
