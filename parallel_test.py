import time
import os
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

username = os.environ.get("LT_USERNAME")
access_key = os.environ.get("LT_ACCESS_KEY")


def get_browser(caps):
    # Use modern Selenium 4 syntax with Options and LT:Options
    options = Options()
    lt_options = {
        "build": caps.get("build", "PyunitTest sample build"),
        "name": caps.get("name", "LambdaTest Parallel Test"),
        "platformName": caps.get("platform", "Windows 10"),
        "browserName": caps.get("browserName", "chrome"),
        "browserVersion": caps.get("version", "latest"),
        "selenium_version": caps.get("selenium_version", "4.1.0"),
    }

    options.set_capability("LT:Options", lt_options)

    return webdriver.Remote(
        command_executor=f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub",
        options=options
    )


# ✅ Define your test configurations
browsers = [
    {
        "build": "PyunitTest sample build",
        "name": "Test 1",
        "platform": "Windows 10",
        "browserName": "chrome",
        "version": "latest",
        "selenium_version": "4.1.0"
    },
    {
        "build": "PyunitTest sample build",
        "name": "Test 2",
        "platform": "Windows 10",
        "browserName": "MicrosoftEdge",
        "version": "latest",
        "selenium_version": "4.1.0"
    }
]

browsers_waiting = []


def get_browser_and_wait(browser_data):
    print(f"Starting {browser_data['name']}")
    driver = get_browser(browser_data)
    driver.set_window_size(1600, 1200)
    driver.get("https://lambdatest.com")
    browsers_waiting.append({"data": browser_data, "driver": driver})
    print(f"{browser_data['name']} ready")

    while len(browsers_waiting) < len(browsers):
        print(f"Browser {browser_data['name']} sending heartbeat while waiting")
        driver.get("https://lambdatest.com")
        time.sleep(3)


# ✅ Run parallel threads
thread_list = []
for browser in browsers:
    t = Thread(target=get_browser_and_wait, args=[browser])
    thread_list.append(t)
    t.start()

for t in thread_list:
    t.join()

# ✅ After all browsers finish
for b in browsers_waiting:
    print(f"Browser {b['data']['name']}'s title: {b['driver'].title}")
    b["driver"].quit()
