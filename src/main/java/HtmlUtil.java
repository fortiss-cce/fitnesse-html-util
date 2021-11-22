import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuilder buffer = new StringBuilder();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_SETUP_NAME, wikiPage);
                extendBuffer(suiteSetup, buffer, "-setup");
            }
            WikiPage setup = PageCrawlerImpl.getInheritedPage("SetUp", wikiPage);
            extendBuffer(setup, buffer, "-setup");
        }

        buffer.append(pageData.getContent());
        if (pageData.hasAttribute("Test")) {
            WikiPage teardown = PageCrawlerImpl.getInheritedPage("TearDown", wikiPage);
            extendBuffer(teardown, buffer, "-teardown");
            if (includeSuiteSetup) {
                WikiPage suiteTeardown = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage);
                extendBuffer(suiteTeardown, buffer, "-teardown");
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    public static void extendBuffer(WikiPage wikiPage, StringBuilder buffer, String flag) throws Exception {
        if (wikiPage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(wikiPage);
            String pagePathName = PathParser.render(pagePath);
            buffer.append("!include ").append(flag).append(" .").append(pagePathName).append("\n");
        }
    }

}
