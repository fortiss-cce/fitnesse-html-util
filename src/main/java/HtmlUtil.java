import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {

        if (!pageData.hasAttribute("Test")) {
            return pageData.getHtml();
        }

        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        if (includeSuiteSetup) {
            AppendIncludeIfSiteExist(wikiPage, SuiteResponder.SUITE_SETUP_NAME, "SetUp", buffer);
        }
        AppendIncludeIfSiteExist(wikiPage, "SetUp", "setup", buffer);

        buffer.append(pageData.getContent());
        AppendIncludeIfSiteExist(wikiPage, "TearDown", "teardown", buffer);

        if (includeSuiteSetup) {
            AppendIncludeIfSiteExist(wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME, "teardown", buffer);
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    private static void AppendIncludeIfSiteExist(WikiPage wikiPage, String pageName, String includeName, StringBuffer buffer) throws Exception {
        WikiPage inheritedPage = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (inheritedPage != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(inheritedPage);
            String pagePathName = PathParser.render(pagePath);
            String include =  String.format("!include -%s .%s\n", includeName, pageName);
            buffer.append(include);
        }
    }

}
