import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    private enum Phase {
        Setup,
        Teardown
    }

    private static StringBuffer injectPagePath(WikiPage wikiPage, String tag, String pageName) throws Exception {
        StringBuffer result = new StringBuffer();

        WikiPage inheritedPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (inheritedPage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(inheritedPage);
            String pagePathName = PathParser.render(pagePath);
            result.append(tag).append(pagePathName).append("\n");
        }

        return result;
    }

    private static StringBuffer injectSetup(WikiPage wikiPage, boolean includeSuiteSetup) throws Exception {
        StringBuffer result = new StringBuffer();

        if (includeSuiteSetup) {
            result.append(injectPagePath(wikiPage, "!include -setup .", SuiteResponder.SUITE_SETUP_NAME));
        }
        result.append(injectPagePath(wikiPage, "!include -setup .", "SetUp"));

        return result;
    }

    private static StringBuffer injectTeardown(WikiPage wikiPage, boolean includeSuiteSetup) throws Exception {
        StringBuffer result = new StringBuffer();

        result.append(injectPagePath(wikiPage, "!include -teardown .", "TearDown"));
        if (includeSuiteSetup) {
            result.append(injectPagePath(wikiPage, "!include -teardown .", SuiteResponder.SUITE_TEARDOWN_NAME));
        }

        return result;
    }

    private static StringBuffer inject(PageData pageData, boolean includeSuiteSetup, Phase phase) throws Exception {
        StringBuffer result = new StringBuffer();

        if (pageData.hasAttribute("Test")) {
            WikiPage wikiPage = pageData.getWikiPage();
            switch (phase) {
                case Setup:
                    result.append(injectSetup(wikiPage, includeSuiteSetup));
                    break;
                case Teardown:
                    result.append(injectTeardown(wikiPage, includeSuiteSetup));
                    break;
            }
        }

        return result;
    }

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        StringBuffer buffer = new StringBuffer();

        buffer.append(inject(pageData, includeSuiteSetup, Phase.Setup));
        buffer.append(pageData.getContent());
        buffer.append(inject(pageData, includeSuiteSetup, Phase.Teardown));

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }
}
