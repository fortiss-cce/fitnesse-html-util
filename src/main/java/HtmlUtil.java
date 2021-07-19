import fitnesse.fixtures.TearDown;
import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                buffer.append(instrument(wikiPage, SuiteResponder.SUITE_SETUP_NAME, "setup"));
            }
            buffer.append(instrument(wikiPage, "SetUp", "setup"));
        }

        buffer.append(pageData.getContent());
        if (pageData.hasAttribute("Test")) {
            buffer.append(instrument(wikiPage, "TearDown", "teardown"));
            if (includeSuiteSetup) {
                buffer.append(instrument(wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME, "teardown"));
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }
    public static String instrument (WikiPage wikiPage, String pageName, String prefix) throws Exception {
        WikiPage inheritedPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        String buffer = new String();
        if (inheritedPage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(inheritedPage);
            String pagePathName = PathParser.render(pagePath);
            buffer = buffer+"!include -";
            buffer = buffer+prefix;
            buffer = buffer+" .";
            buffer = buffer+pagePathName;
            buffer = buffer+"\n";
        }
        return buffer;
    }
}
