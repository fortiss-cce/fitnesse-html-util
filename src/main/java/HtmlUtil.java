import fitnesse.responders.run.SuiteResponder;

import fitnesse.wiki.PageCrawlerImpl;
import fitnesse.wiki.PageData;
import fitnesse.wiki.PathParser;
import fitnesse.wiki.WikiPage;
import fitnesse.wiki.WikiPagePath;


public class HtmlUtil {
    // TODO: please add documentation!

    private static String getPagePathName(String pageName, WikiPage wikiPage) throws Exception{
        String pagePathName = null;
        WikiPage inheritedWikiPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (inheritedWikiPage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(inheritedWikiPage);
            pagePathName = PathParser.render(pagePath);
        }
        return pagePathName;
    }

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                buffer.append("!include -setup .").append(getPagePathName(SuiteResponder.SUITE_SETUP_NAME, wikiPage)).append("\n");
            }

            buffer.append("!include -setup .").append(getPagePathName("SetUp", wikiPage)).append("\n");
        }

        buffer.append(pageData.getContent());

        if (pageData.hasAttribute("Test")) {
            buffer.append("!include -teardown .").append(getPagePathName("TearDown", wikiPage)).append("\n");

            if (includeSuiteSetup) {
                buffer.append("!include -teardown .").append(getPagePathName(SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage)).append("\n");
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }
}
