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

        actual_title = catalog_page.get_title_text()
        assert "іноземними мовами" in actual_title.lower()

    def test_multiple_filters_count_tc024(self):
        catalog_page = CatalogPage(self.driver)
        home_page = HomePage(self.driver)
        self.driver.get("https://www.yakaboo.ua/ua/knigi/vlasnij-import.html")
        home_page.close_ad_if_present()

        catalog_page.open_filters_menu()
        catalog_page.select_filter_by_text("Паперова")
        catalog_page.select_filter_by_text("Англійська")
        catalog_page.close_filters_menu()

        assert catalog_page.get_applied_filters_count() == 2

    def test_sort_by_price_cheapest_tc025(self):
        catalog_page = CatalogPage(self.driver)
        home_page = HomePage(self.driver)
        self.driver.get("https://www.yakaboo.ua/ua/knigi/dobirki-yakaboo.html")
        home_page.close_ad_if_present()

        catalog_page.open_sorting_menu()
        catalog_page.select_sorting_cheapest()

        active_sort = catalog_page.get_active_sorting_name()
        assert "найдешевших" in active_sort.lower()

    def test_product_count_changes_after_filters_tc032(self):
        catalog_page = CatalogPage(self.driver)
        home_page = HomePage(self.driver)

        self.driver.get("https://www.yakaboo.ua/ua/knigi/vlasnij-import.html")
        home_page.close_ad_if_present()

        time.sleep(2)

        initial_count = catalog_page.get_total_products_count()
        print(f"\nПочаткова кількість товарів: {initial_count}")
        assert initial_count > 0, f"БАГ! Лічильник показує 0 товарів на основній сторінці каталогу."

        catalog_page.open_filters_menu()
        catalog_page.select_filter_by_text("Паперова")
        catalog_page.select_filter_by_text("Англійська")

        time.sleep(3)
        filtered_count = catalog_page.get_total_products_count()
        print(f"Кількість після фільтрації: {filtered_count}")

        assert filtered_count < initial_count, "Число товарів не зменшилось після застосування фільтрів!"