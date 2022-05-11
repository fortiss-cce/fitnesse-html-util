import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;


public class HtmlUtil {
    public static final String TEST = "Test";
    public static final String SETUP = "SetUp";
    public static final String TEARDOWN = "TearDown";

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();

        // Look for inherited setup page, if found, append this zto the buffer
        if (pageData.hasAttribute(TEST)) {
            if (includeSuiteSetup) {
                buffer = HtmlUtil.addInheritedPageToBuffer(SuiteResponder.SUITE_SETUP_NAME, wikiPage, buffer);
                buffer = HtmlUtil.addInheritedPageToBuffer(SuiteResponder.SUITE_TEARDOWN_NAME, wikiPage, buffer);
            }
            buffer = HtmlUtil.addInheritedPageToBuffer(SETUP, wikiPage, buffer);
            buffer = HtmlUtil.addInheritedPageToBuffer(TEARDOWN, wikiPage, buffer);
        }

        buffer.append(pageData.getContent());

        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }

    /***
     * Build the buffer based in the wiki page provided information
     * @param wikiPageName The name of the wiki page
     * @param wikiPage The wiki page
     * @param buffer The buffer used to append the wiki page information
     * @return The result buffer containing new information
     * @throws Exception
     */
    private static StringBuffer addInheritedPageToBuffer(String wikiPageName, WikiPage wikiPage, StringBuffer buffer) throws Exception {
        WikiPage foundPage = PageCrawlerImpl.getInheritedPage(wikiPageName, wikiPage);
        if (foundPage != null) {
            WikiPagePath foundPagePath = wikiPage.getPageCrawler().getFullPath(foundPage);
            String foundPagePathName = PathParser.render(foundPagePath);

            // Check which type of the page we want to append
            String bufferAppendix = HtmlUtil.getBufferAppendix(wikiPageName);
            buffer.append(bufferAppendix).append(foundPagePathName).append("\n");
        }

        return buffer;
    }

    /***
     * Define the buffer appendix based on the wiki page name
     * @param wikiPageName The name of the wiki page
     * @return The buffer appendix as string
     */
    private static String getBufferAppendix(String wikiPageName) {
        String bufferAppendix = "";

        switch (wikiPageName) {
            case "SetUp":
            case SuiteResponder.SUITE_SETUP_NAME:
                bufferAppendix = "!include -setup .";
                break;
            case "TearDown":
            case SuiteResponder.SUITE_TEARDOWN_NAME:
                bufferAppendix = "!include -teardown .";
                break;
        }

        return bufferAppendix;
    }

}
