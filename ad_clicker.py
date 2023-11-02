import os
import zipfile
from selenium import webdriver
import time
import pyautogui
from fake_useragent import UserAgent
PROXY_HOST = '91.239.130.34'
PROXY_PORT = 44443
PROXY_USER = 'mr26642sLkD'
PROXY_PASS = 'MbeAJPmBhr' 


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(os.path.join(path, './chromedriver'),chrome_options=chrome_options)
    return driver

def main():
    ua = UserAgent()
    user_agent = ua.random
    driver = get_chromedriver(use_proxy=True,user_agent=user_agent)
    
    #driver.get("https://ipinfo.io/json") #used to check that proxy is changing or not

    driver.get("") #add website
    time.sleep(2)
    pyautogui.click(1000, 350, duration=1) #change values according to your ad location in webpage
    time.sleep(4)
    pyautogui.click(605, 46, duration=1) #change values according to your ad location in webpage
    time.sleep(1)
    driver.quit()
    

if __name__ == '__main__':
    for i in range(0,10):
        main()