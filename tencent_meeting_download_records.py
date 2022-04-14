import asyncio
from time import sleep
from pyppeteer import launch, connect, browser


url = "https://meeting.tencent.com/user-center/meeting-record"


async def is_downloading(browser: browser.Browser):
    page = await browser.newPage()
    await page.goto("chrome://downloads/")

    await page.bringToFront()
    progress = await page.evaluate(
        """
    () => {
    var tag = document.querySelector('downloads-manager').shadowRoot;
    var count = 0
    for (const tag_root of tag.querySelectorAll('downloads-item')) {
        intag = tag_root.shadowRoot;
        console.log(intag);
        var pauseOrResume = intag.getElementById('pauseOrResume');
        count = count + 1
        console.log(pauseOrResume);
        if (pauseOrResume !== null){
            return true
        }
    }
    if (count != 0){
        return false
    }
    return true
    }
    """
    )
    await page.close()
    print(progress)
    return progress


async def main():
    # browser = await launch(executablePath="/usr/bin/google-chrome-stable")
    # browser = await launch(
    #     executablePath="/usr/bin/google-chrome-stable",
    #     headless=False,
    # )
    # google-chrome --remote-debugging-port=9222 --user-data-dir=/dev/shm/temp-workspaces/tencent_meeting_chrome/
    browser = await connect(browserURL="http://127.1:9222", defaultViewport=None)

    page = await browser.newPage()
    await page.goto(url)
    input("Please set page")
    items = await page.waitForSelector("div.tea-table__body > table > tbody > tr")
    items = await page.querySelectorAll("div.tea-table__body > table > tbody > tr")
    for i in items:
        record_date = await page.evaluate(
            "(i) => i.innerText", await i.querySelector(".meeting_start_time")
        )
        print(record_date)
        await page.evaluate(
            "(i) => i.click()",
            await i.querySelector(".oparation-list > .more-dropdown"),
        )
        download_button = await page.waitForSelector(
            ".meeting-record-more-dropdown > ul > li > a"
        )

        await page.evaluate("(i) => i.click()", download_button)
        await page.mouse.move(10, 10)
        await page.mouse.click(10, 10)
        sleep(1)
        downloading = await is_downloading(browser)
        while downloading == True:
            sleep(1)
            downloading = await is_downloading(browser)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
