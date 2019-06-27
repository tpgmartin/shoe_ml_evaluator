from bs4 import BeautifulSoup
import pickle
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.firefox import GeckoDriverManager

# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
# driver.header_overrides = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
# driver.get("https://stockx.com/sneakers/top-selling?years=2017")
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
# driver.quit()

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.header_overrides = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
cookies = pickle.load(open("cookies.pkl", "rb"))
driver.get("https://stockx.com/sneakers/top-selling?years=2017")
# driver.add_cookie({"name" : "cookie_policy_accepted", "value" : "true"})
# driver.quit()

# driver.delete_cookie("test_cookie")
# driver.add_cookie({"name" : "cookie_policy_accepted", "value" : "true"})
# driver.add_cookie({"name" : "rCookie", "value" : "potvnxq3fpb8daotdb579l"})
# driver.add_cookie({"name" : "rskxRunCookie", "value" : "0"})
# # time.sleep(5)
# # driver.header_overrides = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
# # driver.refresh()

# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "dialog-button"))
#     )
#     element.click()
#     time.sleep(10)
# finally:
#     driver.quit()

# cookie_banner = driver.find_element_by_class_name("dialog-button")
# cookie_banner.click()
# time.sleep(5)

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
load_more = driver.find_element_by_class_name("browse-load-more")
load_more.location_once_scrolled_into_view
# print(element.location_once_scrolled_into_view)
# driver.execute_script("window.scrollTo(0, 1000);")
# driver.execute_script("return arguments[0].scrollIntoView(true);", button_element_to_click)
load_more.click()
# time.sleep(5)

# html = driver.page_source
# soup = BeautifulSoup(html, "html5lib")

# browse_grid = soup.find_all(class_="browse-tile")

# print(len(browse_grid))

# driver.quit()