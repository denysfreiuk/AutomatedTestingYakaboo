import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.catalog_page import CatalogPage
from pages.home_page import HomePage


class TestCatalog:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def test_catalog_navigation_tc004(self):
        catalog_page = CatalogPage(self.driver)
        home_page = HomePage(self.driver)

        self.driver.get("https://www.yakaboo.ua/ua/knigi/vlasnij-import.html")

        home_page.close_ad_if_present()
        time.sleep(2)

        actual_title = catalog_page.get_title_text()
        print(f"Результат: '{actual_title}'")

        expected_phrase = "іноземними мовами"
        assert expected_phrase.lower() in actual_title.lower(), \
            f"БАГ! Очікували заголовок з '{expected_phrase}', але отримали порожнечу або інший текст: '{actual_title}'"

    def test_multiple_filters_count_tc024(self):
        catalog_page = CatalogPage(self.driver)
        home_page = HomePage(self.driver)

        self.driver.get("https://www.yakaboo.ua/ua/knigi/vlasnij-import.html")
        home_page.close_ad_if_present()

        catalog_page.open_filters_menu()

        catalog_page.select_filter_by_text("Паперова")

        catalog_page.select_filter_by_text("Англійська")

        catalog_page.close_filters_menu()

        final_count = catalog_page.get_applied_filters_count()

        assert final_count == 2, f"БАГ! Очікували 2 обраних фільтри на кнопці, але бачимо: {final_count}"