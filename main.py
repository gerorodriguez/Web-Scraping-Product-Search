from selenium import webdriver
import chromedriver_autoinstaller
import time
import helium as he

chromedriver_autoinstaller.install()

he.start_chrome("https://www.google.com/")

search_box = he.find_all(he.S("[aria-label='Buscar']"))[0]

he.write("dolarhoy", into=search_box)

he.press(he.ENTER)

time.sleep(6)

search_results = he.find_all(he.S("h3"))

he.wait_until(search_results[-1].exists)

for search_result in search_results:
    if "dolarhoy" not in search_result.web_element.text.lower():
        continue
    he.click(search_result)
    break

input()

he.kill_browser()
