import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();
        if (pageData.hasAttribute("Test")) {
            HtmlUtil.addStepUpTest(wikiPage, buffer, includeSuiteSetup);
        }

        buffer.append(pageData.getContent());

        if (pageData.hasAttribute("Test")) {
            HtmlUtil.addTearDownTest(wikiPage, buffer, includeSuiteSetup);
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    private static void addStepUpTest(WikiPage wikiPage, StringBuffer buffer, boolean includeSuiteSetup) throws Exception {
        if (includeSuiteSetup) {
            addSetUpWikiPageSuite(wikiPage, buffer);
        }
        addSetUpWikiPage(wikiPage, buffer);
    }

    private static void addTearDownTest(WikiPage wikiPage, StringBuffer buffer, boolean includeSuiteSetup) throws Exception {
        addTearDownWikiPage(wikiPage, buffer);
        if (includeSuiteSetup) {
            addTearDownWikiPageSuite(wikiPage, buffer);
        }
    }

    private static void addSetUpWikiPage(WikiPage wikiPage, StringBuffer buffer) throws Exception {
        WikiPage setup = PageCrawlerImpl.getInheritedPage("SetUp", wikiPage);
        if (setup != null) {
            WikiPagePath setupPath = wikiPage.getPageCrawler().getFullPath(setup);
            String setupPathName = PathParser.render(setupPath);
            buffer.append("!include -setup .").append(setupPathName).append("\n");
        }
    }

    private static void addTearDownWikiPage(WikiPage wikiPage, StringBuffer buffer) throws Exception {
        WikiPage teardown = PageCrawlerImpl.getInheritedPage("TearDown", wikiPage);
        if (teardown != null) {
            WikiPagePath tearDownPath = wikiPage.getPageCrawler().getFullPath(teardown);
            String tearDownPathName = PathParser.render(tearDownPath);
            buffer.append("!include -teardown .").append(tearDownPathName).append("\n");
        }
    }

    private static void addSetUpWikiPageSuite(WikiPage wikiPage, StringBuffer buffer) throws Exception {
        WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_SETUP_NAME, wikiPage);
        if (suiteSetup != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(suiteSetup);
            String pagePathName = PathParser.render(pagePath);
            buffer.append("!include -setup .").append(pagePathName).append("\n");
        }
    }

    private static void addTearDownWikiPageSuite(WikiPage wikiPage, StringBuffer buffer) throws Exception {
        WikiPage suiteTeardown = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage);
        if (suiteTeardown != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(suiteTeardown);
            String pagePathName = PathParser.render(pagePath);
            buffer.append("!include -teardown .").append(pagePathName).append("\n");
        }
    }

}
