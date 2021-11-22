import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();
        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup)
                getInehritedPage(wikiPage, buffer, SuiteResponder.SUITE_SETUP_NAME, "setup");
            getInehritedPage(wikiPage, buffer, "SetUp", "setup");
            
            
        }
        buffer.append(pageData.getContent());
        if (pageData.hasAttribute("Test")) {  
            
            getInehritedPage(wikiPage, buffer, "TearDown", "teardown");
            if(includeSuiteSetup)
                getInehritedPage(wikiPage, buffer, SuiteResponder.SUITE_TEARDOWN_NAME, "teardown");
        }
        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }



    public static void getInehritedPage(WikiPage wikiPage, StringBuffer buffer, String pageName, String suffix) throws Exception
    {

        WikiPage suiteType = PageCrawlerImpl.getInheritedPage(pageName, wikiPage);
        if (suiteType != null) {
            WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(suiteType);
            String pagePathName = PathParser.render(pagePath);
            //String suffix = "setup";
            buffer.append("!include -").append(suffix).append(" ." ).append(pagePathName).append("\n");
            
            //buffer.append(method1())
        }
    }

}
