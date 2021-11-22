import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuite) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            // suite setup
            if (includeSuite) {
                parseInheritedPage(SuiteResponder.SUITE_SETUP_NAME, wikiPage, buffer, "-setup");
            }

            // page setup
            parseInheritedPage("SetUp", wikiPage, buffer, "-setup");

            // page content
            buffer.append(pageData.getContent());

            // page teardown
            parseInheritedPage("TearDown", wikiPage, buffer, "-teardown");

            // suite teardown
            if (includeSuite) {
                parseInheritedPage(SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage, buffer, "-teardown");
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    private static void parseInheritedPage(String pageName, WikiPage wikiPage, StringBuffer buffer, String bufferAppendParam) throws Exception {
        WikiPage inheritedPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (inheritedPage != null) {
            appendPagePathName(inheritedPage, buffer, bufferAppendParam);
        }
    }

    private static void appendPagePathName(WikiPage wikiPage, StringBuffer buffer, String bufferAppendParam) throws Exception {
        WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(wikiPage);
        String pagePathName = PathParser.render(pagePath);
        buffer.append("!include " + bufferAppendParam + " .").append(pagePathName).append("\n");
    }
}
