import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static final String INCLUDE_SETUP_COMMAND = "!include -setup .";
    public static final String INCLUDE_TEARDOWN_COMMAND = "!include -teardown .";

    public static String generateTestableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();
        boolean hasTest = pageData.hasAttribute("Test");

        addTestSetup(hasTest, includeSuiteSetup, wikiPage, buffer);
        buffer.append(pageData.getContent());
        addTestTeardown(hasTest, includeSuiteSetup, wikiPage, buffer);

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    private static void addTestSetup(boolean hasTest, boolean includeSuiteSetup, WikiPage wikiPage, StringBuffer buffer) throws Exception {
        if (hasTest) {
            if (includeSuiteSetup) {
                appendHtml(wikiPage, buffer, SuiteResponder.SUITE_SETUP_NAME, INCLUDE_SETUP_COMMAND);
            }
            appendHtml(wikiPage, buffer, "SetUp", INCLUDE_SETUP_COMMAND);
        }
    }

    private static void addTestTeardown(boolean hasTest, boolean includeSuiteSetup, WikiPage wikiPage, StringBuffer buffer) throws Exception {
        if (hasTest) {
            appendHtml(wikiPage, buffer, "TearDown", INCLUDE_TEARDOWN_COMMAND);
            if (includeSuiteSetup) {
                appendHtml(wikiPage, buffer, SuiteResponder.SUITE_TEARDOWN_NAME, INCLUDE_TEARDOWN_COMMAND);
            }
        }
    }

    private static void appendHtml(WikiPage wikiPage, StringBuffer buffer, String pageName, String command) throws Exception {
        WikiPage inheritedPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (inheritedPage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(inheritedPage);
            String pagePathName = PathParser.render(pagePath);
            buffer.append(command).append(pagePathName).append("\n");
        }
    }

}
