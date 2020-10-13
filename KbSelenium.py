from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import lxml.html as html

# 参考：
# https://chromedriver.chromium.org/logging
# https://stackoverflow.com/questions/47392423/python-selenium-devtools-listening-on-ws-127-0-0-1
# sel = mySelenium()
# sel.init('testLog.txt')
# root = sel.get("https://www.yahoo.co.jp", 'Yahoo', 'out.html')
# sel.stop()
class kbSelenium:
    def __init__(self):
        self.driver = None
    def init(self, log="mylog.txt"):
        #1. seleniumの準備
        DRIVERPATH="c:/users/takkawai/driver/chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(DRIVERPATH, 
                                options=options,
                                service_args=["--log-path=" + log ] )
    def stop(self):
        if self.driver is not None:
            self.driver.quit()
 
    def get(self, url, title, outfile="", timeout=60):
        if url != "":
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, timeout).until( EC.title_contains(title))
            except TimeoutException as te:
                print("TIMEOUT")
            if outfile != "":
                with open(outfile, 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
            root = html.fromstring(self.driver.page_source)
        else:
            root = html.parse(outfile, html.HTMLParser(encoding='utf-8'))
        return root
    def tostring(self, nodes):
        return html.tostring(nodes)
