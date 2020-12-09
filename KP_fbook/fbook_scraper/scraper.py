import argparse
import time
import json
import csv
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs


with open('facebook_credentials.txt') as file:
    EMAIL = file.readline().split('"')[1]
    PASSWORD = file.readline().split('"')[1]


def _extract_post_text(item):
    actualPosts = item.find_all(attrs={"data-testid": "post_message"})
    print(actualPosts)
    text = ""
    if actualPosts:
        for posts in actualPosts:
            paragraphs = posts.find_all('p')
            text = ""
            for index in range(0, len(paragraphs)):
                text += paragraphs[index].text
    return text


# class = "kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q"


def _extract_comments(item):
    postComments = item.find_all(attrs={"aria-label": "Comment"})
    comments = dict()
    for comment in postComments:
        if comment.find(class_="_6qw4") is None:
            continue

        commenter = comment.find(class_="_6qw4").text
        comments[commenter] = dict()

        comment_text = comment.find("span", class_="_3l3x")

        if comment_text is not None:
            comments[commenter]["text"] = comment_text.text

        commentList = item.find('ul', {'class': '_7791'})
        if commentList:
            comments = dict()
            comment = commentList.find_all('li')
            if comment:
                for litag in comment:
                    aria = litag.find(attrs={"aria-label": "Comment"})
                    if aria:
                        commenter = aria.find(class_="_6qw4").text
                        comments[commenter] = dict()
                        comment_text = litag.find("span", class_="_3l3x")
                        if comment_text:
                            comments[commenter]["text"] = comment_text.text
                            # print(str(litag)+"\n")

                        repliesList = litag.find(class_="_2h2j")
                        if repliesList:
                            reply = repliesList.find_all('li')
                            if reply:
                                comments[commenter]['reply'] = dict()
                                for litag2 in reply:
                                    aria2 = litag2.find(
                                        attrs={"aria-label": "Comment reply"})
                                    if aria2:
                                        replier = aria2.find(
                                            class_="_6qw4").text
                                        if replier:
                                            comments[commenter]['reply'][replier] = dict(
                                            )

                                            reply_text = litag2.find(
                                                "span", class_="_3l3x")
                                            if reply_text:
                                                comments[commenter]['reply'][replier][
                                                    "reply_text"] = reply_text.text

    if(len(comments) == 0):
        comments = ""
    print(comments)

    return comments


def _extract_html(bs_data):
    with open('./bs.html', "w", encoding="utf-8") as file:
        file.write(str(bs_data.prettify()))

    k = bs_data.find_all(class_="_5pcr userContentWrapper")
    postBigDict = list()

    for item in k:
        postDict = dict()
        postDict['Post'] = _extract_post_text(item)
        postDict['json_obj'] = _extract_comments(item)

        postBigDict.append(postDict)
        with open('./postBigDict.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(
                postBigDict, ensure_ascii=False).encode('utf-8').decode())

    return postBigDict


def _login(browser, email, password):
    browser.get("http://facebook.com")
    browser.maximize_window()
    browser.find_element_by_name("email").send_keys(email)
    browser.find_element_by_name("pass").send_keys(password)
    browser.find_element_by_name('login').click()
    time.sleep(5)


def _count_needed_scrolls(browser, infinite_scroll, numOfPost):
    if infinite_scroll:
        lenOfPage = browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;"
        )
    else:
        # roughly 8 post per scroll kindaOf
        lenOfPage = int(numOfPost / 8)
    print("Number Of Scrolls Needed " + str(lenOfPage))
    return lenOfPage


def _scroll(browser, infinite_scroll, lenOfPage):
    lastCount = -1
    match = False

    while not match:
        if infinite_scroll:
            lastCount = lenOfPage
        else:
            lastCount += 1

        # wait for the browser to load, this time can be changed slightly ~3 seconds with no difference, but 5 seems
        # to be stable enough
        time.sleep(5)

        if infinite_scroll:
            lenOfPage = browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
        else:
            browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")

        if lastCount == lenOfPage:
            match = True


def extract(page, numOfPost, infinite_scroll=False, scrape_comment=False):
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    # chromedriver should be in the same folder as file
    browser = webdriver.Chrome(
        executable_path="./chromedriver", options=option)
    _login(browser, EMAIL, PASSWORD)
    browser.get(page)
    lenOfPage = _count_needed_scrolls(browser, infinite_scroll, numOfPost)
    _scroll(browser, infinite_scroll, lenOfPage)

    # click on all the comments to scrape them all!
    # TODO: need to add more support for additional second level comments
    # TODO: ie. comment of a comment

    if scrape_comment:
        # first uncollapse collapsed comments
        unCollapseCommentsButtonsXPath = '//a[contains(@class,"_666h")]'
        unCollapseCommentsButtons = browser.find_elements_by_xpath(
            unCollapseCommentsButtonsXPath)
        print(unCollapseCommentsButtons)
        for unCollapseComment in unCollapseCommentsButtons:
            print(unCollapseComment)
            action = webdriver.common.action_chains.ActionChains(browser)
            try:
                # move to where the un collapse on is
                action.move_to_element_with_offset(unCollapseComment, 5, 5)
                action.perform()
                unCollapseComment.click()
            except:
                # do nothing right here
                pass

         # second set comment ranking to show all comments
        rankDropdowns = browser.find_elements_by_class_name(
            '_2pln')  # select boxes who have rank dropdowns

        rankXPath = '//div[contains(concat(" ", @class, " "), "uiContextualLayerPositioner") and not(contains(concat(" ", @class, " "), "hidden_elem"))]//div/ul/li/a[@class="_54nc"]/span/span/div[@data-ordering="RANKED_UNFILTERED"]'
        for rankDropdown in rankDropdowns:
            # click to open the filter modal
            action = webdriver.common.action_chains.ActionChains(browser)
            try:
                action.move_to_element_with_offset(rankDropdown, 5, 5)
                action.perform()
                rankDropdown.click()
            except:
                pass

            # if modal is opened filter comments
            ranked_unfiltered = browser.find_elements_by_xpath(
                rankXPath)  # RANKED_UNFILTERED => (All Comments)
            if len(ranked_unfiltered) > 0:
                try:
                    ranked_unfiltered[0].click()
                except:
                    pass

        moreComments = browser.find_elements_by_xpath(
            '//a[@class="_4sxc _42ft"]')
        print("Scrolling through to click on more comments")
        timeout = 600
        timeout_start = time.time()

        count = numOfPost
        while len(moreComments) != 0 and timeout_start+timeout > time.time():
            for moreComment in moreComments:
                action = webdriver.common.action_chains.ActionChains(browser)
                try:
                    # move to where the comment button is
                    action.move_to_element_with_offset(moreComment, 5, 5)
                    action.perform()
                    moreComment.click()
                except:
                    # do nothing right here
                    pass

            moreComments = browser.find_elements_by_xpath(
                '//a[@class="_4sxc _42ft"]')

    print("FINISHED SCROLLING, EXTRACTING NOW")
    # Now that the page is fully scrolled, grab the source code.
    source_data = browser.page_source

    # Throw your source into BeautifulSoup and start parsing!
    bs_data = bs(source_data, 'html.parser')
    postBigDict = _extract_html(bs_data)

    print("FINISHED EXTRACTING")
    browser.close()

    return postBigDict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facebook Page Scraper")
    required_parser = parser.add_argument_group("required arguments")
    required_parser.add_argument(
        '-page', '-p', help="The Facebook Public Page you want to scrape", required=True)
    required_parser.add_argument(
        '-len', '-l', help="Number of Posts you want to scrape", type=int, required=True)
    optional_parser = parser.add_argument_group("optional arguments")
    optional_parser.add_argument('-infinite', '-i',
                                 help="Scroll until the end of the page (1 = infinite) (Default is 0)", type=int,
                                 default=0)
    optional_parser.add_argument('-usage', '-u', help="What to do with the data: "
                                                      "Print on Screen (PS), "
                                                      "Write to Text File (WT) (Default is WT)", default="CSV")

    optional_parser.add_argument('-comments', '-c', help="Scrape ALL Comments of Posts (y/n) (Default is n). When "
                                                         "enabled for pages where there are a lot of comments it can "
                                                         "take a while", default="No")
    args = parser.parse_args()

    infinite = False
    if args.infinite == 1:
        infinite = True

    scrape_comment = False
    if args.comments == 'y':
        scrape_comment = True

    postBigDict = extract(page=args.page, numOfPost=args.len,
                          infinite_scroll=infinite, scrape_comment=scrape_comment)

    # TODO: rewrite parser
    if args.usage == "WT":
        with open('output.txt', 'w') as file:
            for post in postBigDict:
                file.write(json.dumps(post))  # use json load to recover

    elif args.usage == "CSV":
        with open('../new_data/data.csv', 'a', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for post in postBigDict:
                writer.writerow([post['Post'], post['json_obj']])

        csvfile.close()

    else:
        for post in postBigDict:
            print("\n")
