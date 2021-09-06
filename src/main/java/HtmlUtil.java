import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.PageCrawler;
import fitnesse.wiki.PageCrawlerImpl;
import fitnesse.wiki.PageData;
import fitnesse.wiki.PathParser;
import fitnesse.wiki.WikiPage;
import fitnesse.wiki.WikiPagePath;


public class HtmlUtil {

    /**
     * Generate a wiki page html and wrapper its content with the test suite.
     * If `includeSuiteSetup` is true, wrapper it again with the test suite setup includes.
     *
     * @param pageData: the wiki page to generate and anotate
     * @param includeSuiteSetup: if test suite setup includes should be added
     */
    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuilder buffer = new StringBuilder();

        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                HtmlUtil.suiteInclude(buffer, SuiteResponder.SUITE_SETUP_NAME,
                                      wikiPage, SuiteResponder.SUITE_SETUP_NAME);
            }

            HtmlUtil.suiteInclude(buffer, "SetUp", wikiPage, SuiteResponder.SUITE_SETUP_NAME);
        }

        buffer.append(pageData.getContent());

        if (pageData.hasAttribute("Test")) {
            HtmlUtil.suiteInclude(buffer, "TearDown", wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME);

            if (includeSuiteSetup) {
                HtmlUtil.suiteInclude(buffer, SuiteResponder.SUITE_TEARDOWN_NAME,
                                      wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME);
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    /**
     * Append includes in wikipage for test suite setup and teardown.
     *
     * @param buffer: buffer to format to
     * @param pageName: page to fetch the suite page from
     * @param wikiPage: wiki entry to to operate on
     * @param setup: which variant of setup/teardown to chose
     */
    public static void suiteInclude(StringBuilder buffer, String pageName,
                                    WikiPage wikiPage, String setup) throws Exception {
        WikiPage suitePage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);

        if (suitePage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(suitePage);
            String pagePathName = PathParser.render(pagePath);

            if (setup == SuiteResponder.SUITE_SETUP_NAME) {
                buffer.append("!include -setup .");
            }
            else if (setup == SuiteResponder.SUITE_TEARDOWN_NAME) {
                buffer.append("!include -teardown .");
            }
            else {
                throw new Exception("unknown suite setup variant");
            }
            buffer.append(pagePathName).append("\n");
        }
    }
}
