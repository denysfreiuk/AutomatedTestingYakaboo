from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class CatalogPage(BasePage):
    FILTERS_BUTTON = (By.CSS_SELECTOR, "button.ui-btn-category.dark")
    CLOSE_FILTERS_BTN = (By.CSS_SELECTOR, "button.ui-btn-close")
    FILTER_COUNT_BADGE = (By.CSS_SELECTOR, "span.filter-length")
    TITLE_H1 = (By.CSS_SELECTOR, "div.category__name h1")

    def get_title_text(self):
        try:
            WebDriverWait(self.driver, 10).until(lambda d: d.find_element(*self.TITLE_H1).text.strip() != "")
            return self.driver.find_element(*self.TITLE_H1).text.strip()
        except:
            return self.driver.execute_script(
                "return document.querySelector('div.category__name h1').textContent;").strip()

    def open_filters_menu(self):
        self.click_element(self.FILTERS_BUTTON)
        time.sleep(2)

    def select_filter_by_text(self, filter_name):
        old_url = self.driver.current_url
        xpath = f"//span[contains(@class, 'ui-filter-checkbox__text') and text()='{filter_name}']"
        element = self.wait_for_element((By.XPATH, xpath))

        self.driver.execute_script("arguments[0].click();", element)

        try:
            WebDriverWait(self.driver, 10).until(lambda d: d.current_url != old_url)
        except:
            print(f"Попередження: URL не змінився після вибору '{filter_name}'")

        time.sleep(1)

    def close_filters_menu(self):
        self.driver.execute_script(
            "document.querySelector('.sidebar-filters__content') ? document.querySelector('.sidebar-filters__content').scrollTop = 0 : window.scrollTo(0,0);")
        time.sleep(1)
        self.click_element(self.CLOSE_FILTERS_BTN)
        time.sleep(2)

    def get_applied_filters_count(self):
        try:
            badge = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.FILTER_COUNT_BADGE))
            return int(badge.text.strip())
        except:
            return 0