import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {
    private static StringBuffer buffer;

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_SETUP_NAME, wikiPage);
                if (suiteSetup != null) {
                    appendPagePath(wikiPage, suiteSetup,"!include -setup .");
                }
            }
            WikiPage setup = PageCrawlerImpl.getInheritedPage("SetUp", wikiPage);
            if (setup != null) {
                //WikiPagePath setupPath = wikiPage.getPageCrawler().getFullPath(setup);
                //String setupPathName = PathParser.render(setupPath);
                //buffer.append("!include -setup .").append(setupPathName).append("\n");
                appendPagePath(wikiPage, setup,"!include -setup .");
            }
        }

        buffer.append(pageData.getContent());
        if (pageData.hasAttribute("Test")) {
            WikiPage teardown = PageCrawlerImpl.getInheritedPage("TearDown", wikiPage);
            if (teardown != null) {
                //WikiPagePath tearDownPath = wikiPage.getPageCrawler().getFullPath(teardown);
                //String tearDownPathName = PathParser.render(tearDownPath);
                //buffer.append("!include -teardown .").append(tearDownPathName).append("\n");
                appendPagePath(wikiPage, teardown, "!include -teardown .");
            }
            if (includeSuiteSetup) {
                WikiPage suiteTeardown = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage);
                if (suiteTeardown != null) {
                    //WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(suiteTeardown);
                    //String pagePathName = PathParser.render(pagePath);
                    //buffer.append("!include -teardown .").append(pagePathName).append("\n");
                    appendPagePath(wikiPage, suiteTeardown, "!include -teardown .");
                }
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    private static void appendPagePath(WikiPage wikiPage, WikiPage crawler, String header) throws Exception {
        WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(crawler);
        String pathName = PathParser.render(pagePath);
        buffer.append(header).append(pathName).append("\n");
    }

}
