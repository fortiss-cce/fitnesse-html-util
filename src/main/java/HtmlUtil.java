import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                buffer.append(getSetupString(wikiPage, SuiteResponder.SUITE_SETUP_NAME, false));
                buffer.append(getSetupString(wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME, true));
            }
            buffer.append(getSetupString(wikiPage, "SetUp", false));
            buffer.append(getSetupString(wikiPage, "TearDown", true));
        }

        buffer.append(pageData.getContent());

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    // Wrap the code in a helper function
    private static String getSetupString(WikiPage wikiPage, String pageName, boolean isTearDown) throws Exception {
        StringBuffer buffer = new StringBuffer();
        WikiPage setup = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);

        String argumentName = " -setup .";
        if (isTearDown) {
            argumentName = " -teardown .";
        }

        if (setup != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(setup);
            String pagePathName = PathParser.render(pagePath);
            buffer.append("!include").append(argumentName).append(pagePathName).append("\n");
        }
        return buffer.toString();
    }
}