import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


/*

 */

public class HtmlUtil {

    private static WikiPage wikiPage;
    private static StringBuffer buffer;


    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        wikiPage = pageData.getWikiPage();
        buffer = new StringBuffer();

        String attribute = "Test";

        if (pageData.hasAttribute(attribute)) {
            if (includeSuiteSetup) {
                append_page_to_buffer(SuiteResponder.SUITE_SETUP_NAME, "!include -setup .");
            }
            append_page_to_buffer("SetUp", "!include -setup .");
        }

        buffer.append(pageData.getContent());

        if (pageData.hasAttribute(attribute)) {

            append_page_to_buffer("TearDown", "!include -teardown .");

            if (includeSuiteSetup) {
                append_page_to_buffer(SuiteResponder.SUITE_TEARDOWN_NAME, "!include -teardown .");
            }
        }

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }




    /*

     */

    private static void append_page_to_buffer(String name, String description) throws Exception
    {
        WikiPage page = PageCrawlerImpl.getInheritedPage(name, wikiPage);

        if (page != null) {
            WikiPagePath path = wikiPage.getPageCrawler().getFullPath(page);
            String pathName = PathParser.render(path);
            buffer.append(description).append(pathName).append("\n");
        }

    }

}
