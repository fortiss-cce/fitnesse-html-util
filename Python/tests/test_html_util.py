from fitnesse.html_util import HtmlUtil
from tests.conftest import WikiPage, PageCrawler, PathParser, PageCrawlerImpl


def test_testable_html(wiki_page: WikiPage, path_parser: PathParser, page_crawler: PageCrawlerImpl):
    root: WikiPage = wiki_page.make_root("RooT")
    crawler: PageCrawler = root.get_page_crawler()
    crawler.add_page(root, path_parser.parse("SetUp"), "setup")
    crawler.add_page(root, path_parser.parse("TearDown"), "teardown")
    page: WikiPage = crawler.add_page(root, path_parser.parse("TestPage"), "the content")

    html_util_obj = HtmlUtil(
        page_data = page.get_data(),
        path_parser = path_parser
    )

    # html: str = HtmlUtil.testable_html(page.get_data(), False, page_crawler, path_parser)
    html = html_util_obj.testable_html(
        include_suite_setup = False, 
        page_crawler = page_crawler
    )
    assert ".SetUp" in html
    assert "setup" in html
    assert ".TearDown" in html
    assert "teardown" in html
    assert "the content" in html
    assert "<p>" in html
