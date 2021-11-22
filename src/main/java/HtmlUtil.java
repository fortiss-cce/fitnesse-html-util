import fitnesse.responders.run.SuiteResponder;
import fitnesse.wiki.*;

public class HtmlUtil {
	private static String SETUP_NAME = "SetUp";
	private static String TEARDOWN_NAME = "TearDown";

    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
		WikiPage wikiPage = pageData.getWikiPage();
		StringBuffer buffer = new StringBuffer();

		if (pageData.hasAttribute("Test")) {
			if (includeSuiteSetup) {
				addPart(buffer, "!include -setup .", wikiPage, SuiteResponder.SUITE_SETUP_NAME);
			}
			addPart(buffer, "!include -setup .", wikiPage, SETUP_NAME);
			buffer.append(pageData.getContent());
			addPart(buffer, "!include -teardown .", wikiPage, TEARDOWN_NAME);
			if (includeSuiteSetup) {
				addPart(buffer, "!include -teardown .", wikiPage, SuiteResponder.SUITE_TEARDOWN_NAME);
			}
		} else {
			buffer.append(pageData.getContent());
		}

		pageData.setContent(buffer.toString());
		return pageData.getHtml();
	}

	public static void addPart(StringBuffer buffer, String includeText, WikiPage wikiPage, String pagePartName)
			throws Exception {
		WikiPage pagePart = PageCrawlerImpl.getInheritedPage(pagePartName, wikiPage);
		if (pagePart != null) {
			WikiPagePath pagePath = wikiPage.getPageCrawler().getFullPath(pagePart);
			String pagePathName = PathParser.render(pagePath);
			buffer.append(includeText).append(pagePathName).append("\n");
		}
	}

}