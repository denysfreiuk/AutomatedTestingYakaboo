import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage


class TestSearch:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def test_search_exact_title_tc001(self):
        home_page = HomePage(self.driver)

        home_page.open()

        home_page.close_ad_if_present()

        book_title = "Кобзар"
        home_page.search_for_book(book_title)

        time.sleep(4)

        current_url = self.driver.current_url.lower()
        assert "search" in current_url or "kobzar" in current_url, f"Пошук не спрацював, поточний URL: {current_url}"

        actual_title = home_page.get_first_book_title_text()
        assert book_title.lower() in actual_title.lower(), f"Очікували '{book_title}' у назві, але отримали '{actual_title}'"