import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pages.base_page import BasePage


class CatalogPage(BasePage):
    TITLE_H1 = (By.CSS_SELECTOR, "div.category__name h1")
    FILTERS_BUTTON = (By.CSS_SELECTOR, "button.ui-btn-category.dark")
    CLOSE_FILTERS_BTN = (By.CSS_SELECTOR, "button.ui-btn-close")
    FILTER_COUNT_BADGE = (By.CSS_SELECTOR, "span.filter-length")

    SORT_BUTTON = (By.CSS_SELECTOR, "button.sorting__btn")
    SORT_OPTION_CHEAPEST = (By.XPATH, "//button[contains(@class, 'sort-item') and contains(text(), 'Від найдешевших')]")
    CURRENT_SORT_TEXT = (By.CSS_SELECTOR, "button.sorting__btn span")
    PRODUCT_COUNT = (By.CSS_SELECTOR, "span.category__amount")

    def get_title_text(self):
        try:
            WebDriverWait(self.driver, 10).until(lambda d: d.find_element(*self.TITLE_H1).text.strip() != "")
            return self.driver.find_element(*self.TITLE_H1).text.strip()
        except:
            return self.driver.execute_script(
                "return document.querySelector('div.category__name h1') ? document.querySelector('div.category__name h1').textContent : '';").strip()

    def open_filters_menu(self):
        self.click_element(self.FILTERS_BUTTON)
        time.sleep(2)

    def select_filter_by_text(self, filter_name):
        old_url = self.driver.current_url
        xpath = f"//span[contains(@class, 'ui-filter-checkbox__text') and text()='{filter_name}']"
        element = self.wait_for_element((By.XPATH, xpath))
        self.driver.execute_script("arguments[0].click();", element)
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != old_url)
        time.sleep(1)

    def close_filters_menu(self):
        self.click_element(self.CLOSE_FILTERS_BTN)
        time.sleep(1.5)

    def get_applied_filters_count(self):
        try:
            badge = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.FILTER_COUNT_BADGE))
            return int(badge.text.strip())
        except:
            return 0

    def open_sorting_menu(self):
        self.click_element(self.SORT_BUTTON)
        time.sleep(1)

    def select_sorting_cheapest(self):
        old_url = self.driver.current_url
        self.click_element(self.SORT_OPTION_CHEAPEST)
        WebDriverWait(self.driver, 10).until(lambda d: d.current_url != old_url)
        time.sleep(2)

    def get_active_sorting_name(self):
        return self.wait_for_element(self.CURRENT_SORT_TEXT).text.strip()

    def get_total_products_count(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: re.search(r'\d', d.find_element(*self.PRODUCT_COUNT).get_attribute("textContent"))
            )

            element = self.driver.find_element(*self.PRODUCT_COUNT)
            text = element.get_attribute("textContent").strip()

            count = re.sub(r'\D', '', text)
            print(f"[Debug] Отримано текст лічильника: '{text}', цифр знайдено: '{count}'")

            return int(count) if count else 0
        except Exception as e:
            print(f"[Error] Не вдалося зчитати кількість товарів: {e}")
            return 0

