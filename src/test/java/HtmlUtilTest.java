import fitnesse.wiki.InMemoryPage;
import fitnesse.wiki.PageCrawler;
import fitnesse.wiki.PathParser;
import fitnesse.wiki.WikiPage;
import junit.framework.TestCase;

public class HtmlUtilTest extends TestCase {


    public void testTestableHtml() throws Exception {
        WikiPage root = InMemoryPage.makeRoot("RooT");
        PageCrawler crawler = root.getPageCrawler();
        crawler.addPage(root, PathParser.parse("SetUp"), "setup");
        crawler.addPage(root, PathParser.parse("TearDown"), "teardown");
        WikiPage page = crawler.addPage(root, PathParser.parse("TestPage"), "the content");

        String html = HtmlUtil.testableHtml(page.getData(), false);
        assertSubString(".SetUp", html);
        assertSubString("setup", html);
        assertSubString(".TearDown", html);
        assertSubString("teardown", html);
        assertSubString("the content", html);
        assertSubString("class=\"collapsable\"", html);
    }

    public static void assertSubString(String substring, String string) {
        if (!string.contains(substring)) {
            fail("substring '" + substring + "' not found.");
        }
    }

}
