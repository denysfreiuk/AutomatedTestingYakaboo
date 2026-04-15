import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage
from pages.catalog_page import CatalogPage


class TestSecurity:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def test_search_sql_injection_basic_tc011(self):
        home_page = HomePage(self.driver)
        catalog_page = CatalogPage(self.driver)

        home_page.open()
        home_page.close_ad_if_present()

        injection_payload = "'''"
        home_page.search_for_book(injection_payload)

        time.sleep(3)

        result_count = catalog_page.get_total_products_count()

        assert result_count == 0, \
            f"БАГ! Система повернула {result_count} результатів на запит {injection_payload}. " \
            f"Мало бути 0. Можлива вразливість або некоректна обробка спецсимволів."