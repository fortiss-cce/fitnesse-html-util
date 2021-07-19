import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;





public class HtmlUtil {


    //TODO : static or not?
    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        getSection(pageData, includeSuiteSetup, wikiPage, buffer, "SetUp");
        getContent(buffer, pageData.getContent());
        getSection(pageData, includeSuiteSetup, wikiPage, buffer, "TearDown"); // TODO: discuss down /Down

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }


    private static void getSection(final PageData pageData, final boolean includeSuiteSetup, final WikiPage wikiPage, final StringBuffer buffer, String sectionName) throws Exception {

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(SuiteResponder.SUITE_SETUP_NAME, wikiPage);
                if (suiteSetup != null) {
                    appendPage(wikiPage, buffer, suiteSetup, sectionName.toLowerCase());
                }
            }
            WikiPage setup = PageCrawlerImpl.getInheritedPage(sectionName, wikiPage);
            if (setup != null) {
                appendPage(wikiPage, buffer, setup, sectionName.toLowerCase());
            }
        }
    }


    private static void appendPage(final WikiPage wikiPage, final StringBuffer buffer, final WikiPage suiteSetup, String s) throws Exception {

        s = "!include -"+ s + " .";
        WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(suiteSetup);
        String pagePathName = PathParser.render(pagePath);
        buffer.append(s).append(pagePathName).append("\n");
    }

    private static void getContent(final StringBuffer buffer, final String content) {
        buffer.append(content);
    }

}
