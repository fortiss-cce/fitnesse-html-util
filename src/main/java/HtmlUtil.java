import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    private static String getPagePathName(WikiPage wikiPage, String name) throws Exception {
        String pagePathName = "";
        WikiPage page = PageCrawlerImpl.getInheritedPage(name, wikiPage);
        if (page != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(page);
            pagePathName = PathParser.render(pagePath);
        }
        return pagePathName;
    }

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                String pageSetUpPathName = getPagePathName(wikiPage, SuiteResponder.SUITE_SETUP_NAME);
                if (!pageSetUpPathName.isEmpty()) {
                    buffer.append("!include -setup .").append(pageSetUpPathName).append("\n");
                }
            }

            String pagePageName = getPagePathName(wikiPage, "SetUp");
            if (!pagePageName.isEmpty()) {
                buffer.append("!include -setup .").append(pagePageName).append("\n");
            }
        }

        buffer.append(pageData.getContent());
        if (pageData.hasAttribute("Test")) {
            String tearDownPathName = getPagePathName(wikiPage, "TearDown");
            if (!tearDownPathName.isEmpty()) {
                buffer.append("!include -teardown .").append(tearDownPathName).append("\n");
            }

            if (includeSuiteSetup) {
                String pagePathName = getPagePathName(wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME);
                if (!pagePathName.isEmpty()) {
                    buffer.append("!include -teardown .").append(pagePathName).append("\n");
                }
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

}
