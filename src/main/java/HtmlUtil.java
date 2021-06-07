import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static final String INCLUDE_SETUP_COMMAND = "!include -setup .";
    public static final String INCLUDE_TEARDOWN_COMMAND = "!include -teardown .";

    public static String generateTestableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuilder stringBuilder = new StringBuilder();
        boolean hasTest = pageData.hasAttribute("Test");

        addTestSetup(hasTest, includeSuiteSetup, wikiPage, stringBuilder);
        stringBuilder.append(pageData.getContent());
        addTestTeardown(hasTest, includeSuiteSetup, wikiPage, stringBuilder);

        pageData.setContent(stringBuilder.toString());
        return pageData.getHtml();
    }

    private static void addTestSetup(boolean hasTest, boolean includeSuiteSetup, WikiPage wikiPage, StringBuilder stringBuilder) throws Exception {
        if (hasTest) {
            if (includeSuiteSetup) {
                appendHtml(wikiPage, stringBuilder, SuiteResponder.SUITE_SETUP_NAME, INCLUDE_SETUP_COMMAND);
            }
            appendHtml(wikiPage, stringBuilder, "SetUp", INCLUDE_SETUP_COMMAND);
        }
    }

    private static void addTestTeardown(boolean hasTest, boolean includeSuiteSetup, WikiPage wikiPage, StringBuilder stringBuilder) throws Exception {
        if (hasTest) {
            appendHtml(wikiPage, stringBuilder, "TearDown", INCLUDE_TEARDOWN_COMMAND);
            if (includeSuiteSetup) {
                appendHtml(wikiPage, stringBuilder, SuiteResponder.SUITE_TEARDOWN_NAME, INCLUDE_TEARDOWN_COMMAND);
            }
        }
    }

    private static void appendHtml(WikiPage wikiPage, StringBuilder stringBuilder, String pageName, String command) throws Exception {
        WikiPage inheritedPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (inheritedPage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(inheritedPage);
            String pagePathName = PathParser.render(pagePath);
            stringBuilder.append(command).append(pagePathName).append("\n");
        }
    }

}
