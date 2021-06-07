import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    private static String suiteSetup(WikiPage wikiPage, boolean includeSuiteSetup) throws Exception{
        StringBuffer buffer = new StringBuffer();

        if (includeSuiteSetup) {
            WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_SETUP_NAME, wikiPage);
            if (suiteSetup != null) {
                String pagePathName = extractWikiPagePath(wikiPage, suiteSetup);
                buffer.append("!include -setup .").append(pagePathName).append("\n");
            }
        }

        WikiPage setup = PageCrawlerImpl.getInheritedPage("SetUp", wikiPage);
        if (setup != null) {
            String setupPathName = extractWikiPagePath(wikiPage, setup);
            buffer.append("!include -setup .").append(setupPathName).append("\n");
        }

        return buffer.toString();
    }

    private static String tearDown(WikiPage wikiPage, boolean includeSuiteSetup) throws Exception {
        StringBuffer buffer = new StringBuffer();
        WikiPage teardown = PageCrawlerImpl.getInheritedPage("TearDown", wikiPage);

        if (teardown != null) {
            String tearDownPathName = extractWikiPagePath(wikiPage, teardown);
            buffer.append("!include -teardown .").append(tearDownPathName).append("\n");
        }

        if (includeSuiteSetup) {
            WikiPage suiteTeardown = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage);
            if (suiteTeardown != null) {
                String pagePathName = extractWikiPagePath(wikiPage, suiteTeardown);
                buffer.append("!include -teardown .").append(pagePathName).append("\n");
            }
        }

        return buffer.toString();
    }

    private static String extractWikiPagePath(WikiPage mainWikiPage, WikiPage page) throws Exception {
        WikiPagePath path = mainWikiPage.getPageCrawler().getFullPath(page);
        return PathParser.render(path);
    }

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            buffer.append(suiteSetup(wikiPage, includeSuiteSetup));
        }

        buffer.append(pageData.getContent());

        if (pageData.hasAttribute("Test")) {
            buffer.append(tearDown(wikiPage, includeSuiteSetup));
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

}
