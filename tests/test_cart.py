import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage
from pages.cart_page import CartPage  # Додали імпорт!


class TestCart:
    def setup_method(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def test_add_item_to_cart_tc002(self):
        home_page = HomePage(self.driver)

        home_page.open()
        home_page.close_ad_if_present()

        home_page.search_for_book("Кобзар")
        time.sleep(3)

        initial_count = home_page.get_cart_item_count()
        assert initial_count == 0, f"На початку тесту кошик не порожній! Товарів: {initial_count}"

        home_page.add_first_book_to_cart()

        new_count = home_page.get_cart_item_count()
        assert new_count == 1, f"Очікували 1 товар у кошику, але маємо {new_count}"

    def test_remove_item_from_cart_tc006(self):
        home_page = HomePage(self.driver)
        cart_page = CartPage(self.driver)

        # 1. Відкриваємо сайт і шукаємо товар
        home_page.open()
        home_page.close_ad_if_present()
        home_page.search_for_book("Кобзар")
        time.sleep(3)

        # 2. Додаємо товар до кошика
        home_page.add_first_book_to_cart()
        assert home_page.get_cart_item_count() == 1, "Не вдалося додати товар перед видаленням"

        # 3. Відкриваємо кошик
        cart_page.open_cart()

        # 4. Видаляємо товар
        cart_page.remove_first_item()

        # 5. Перевіряємо, що кошик порожній
        assert cart_page.is_cart_empty(), "Повідомлення про порожній кошик не знайдено! Товар міг не видалитися."