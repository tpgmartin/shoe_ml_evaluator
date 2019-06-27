from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.header_overrides = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
driver.get("https://stockx.com/sneakers/top-selling?years=2017")
driver.delete_cookie("test_cookie")
driver.add_cookie({"name" : "cookie_policy_accepted", "value" : "true"})
time.sleep(5)
driver.refresh()

# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "dialog_box"))
#     )
#     element.click()
# finally:
#     driver.quit()

# cookie_banner = driver.find_element_by_class_name("dialog-button")
# cookie_banner.click()
# time.sleep(5)

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# driver.execute_script("return arguments[0].scrollIntoView(true);", button_element_to_click)
# load_more = driver.find_element_by_class_name("browse-load-more")
# load_more.click()
# time.sleep(5)

# html = driver.page_source
# soup = BeautifulSoup(html, "html5lib")

# browse_grid = soup.find_all(class_="browse-tile")

# print(len(browse_grid))

# driver.quit()