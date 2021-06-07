import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    /**
     * This function parses the HTML page and searches for "tests" that could be executed.
     * If no tests are found, the HTML content is returned as is.
     * @param pageData
     * @param includeSuiteSetup
     * @return
     * @throws Exception
     */
    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {

        if (pageData.hasAttribute("Test")) {
            String wrappedContent = wrapTestableHtmlContent(pageData, includeSuiteSetup);
            pageData.setContent(wrappedContent);
        }
        return pageData.getHtml();
    }

    /**
     * This function wraps the content of a page that contains tests into the appropriate setup and teardown blocks.
     * @param pageData
     * @param includeSuiteSetup
     * @return
     * @throws Exception
     */
    private static String wrapTestableHtmlContent(PageData pageData, boolean includeSuiteSetup) throws Exception {

        WikiPage wikiPage = pageData.getWikiPage();

        StringBuffer buffer = new StringBuffer();
        appendSetupContent(buffer, wikiPage, includeSuiteSetup);
        buffer.append(pageData.getContent());
        appendTeardownContent(buffer, wikiPage, includeSuiteSetup);

        return buffer.toString();
    }

    private static void appendSetupContent(StringBuffer buffer, WikiPage wikiPage, boolean includeSuiteSetup)
            throws Exception {
        String contentFlag = "setup";
        if (includeSuiteSetup) {
            appendContentBlock(buffer, wikiPage, SuiteResponder.SUITE_SETUP_NAME, contentFlag);
        }
        appendContentBlock(buffer, wikiPage,"SetUp", contentFlag);
    }

    private static void appendTeardownContent(StringBuffer buffer, WikiPage wikiPage, boolean includeSuiteSetup)
            throws Exception{
        String contentFlag = "teardown";
        appendContentBlock(buffer, wikiPage, "TearDown", contentFlag);

        if (includeSuiteSetup) {
            appendContentBlock(buffer, wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME, contentFlag);
        }
    }

    private static void appendContentBlock(StringBuffer buffer, WikiPage wikiPage, String pageName, String contentFlag)
            throws Exception {
        WikiPage page = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (page != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(page);
            String pagePathName = PathParser.render(pagePath);
            buffer.append("!include -").append(contentFlag).append(" .").append(pagePathName).append("\n");
        }
    }
}
