import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;

/*
 * Description ...
 */
public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                appendPathName(wikiPage, buffer, SuiteResponder.SUITE_SETUP_NAME, "!include -setup .");
            }
            appendPathName(wikiPage, buffer, "SetUp", "!include -setup .");
        }

        buffer.append(pageData.getContent());
        //TODO remove duplicated if
        if (pageData.hasAttribute("Test")) {
            appendPathName(wikiPage, buffer, "TearDown", "!include -teardown .");
            if (includeSuiteSetup) {
                appendPathName(wikiPage, buffer, SuiteResponder.SUITE_TEARDOWN_NAME, "!include -teardown .");
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    private static void appendPathName(WikiPage wikiPage, StringBuffer buffer, String pageName, String appendKey) throws Exception {
        WikiPage setup = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (setup != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(setup);
            String pagePathName = PathParser.render(pagePath);
            buffer.append(appendKey).append(pagePathName).append("\n");
        }
    }
}
