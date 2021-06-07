import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    /**
     *  Add setup teardown pages to WikiPage
     */
    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();

        if (pageData.hasAttribute("Test")) {
            StringBuffer buffer = new StringBuffer();
            if (includeSuiteSetup) {
                appendContentToPage(wikiPage, SuiteResponder.SUITE_SETUP_NAME, buffer, "!include -teardown .");
            }
            appendContentToPage(wikiPage, "SetUp", buffer, "!include -setup .");

            buffer.append(pageData.getContent());
            appendContentToPage(wikiPage, "TearDown", buffer, "!include -teardown .");

            if (includeSuiteSetup) {
                 appendContentToPage(wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME, buffer, "!include -teardown .");
            }
            pageData.setContent(buffer.toString());
        }

        return pageData.getHtml();
    }

    private static void appendContentToPage(WikiPage wikiPage, String pageName, StringBuffer buffer, String content) throws Exception {
        WikiPage subPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (subPage != null){
            WikiPagePath tearDownPath = wikiPage.getPageCrawler().getFullPath(subPage);
            String renderPath = PathParser.render(tearDownPath);
            buffer.append(content).append(renderPath).append("\n");
        }
    }

}
