import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.home_page import HomePage
from pages.cart_page import CartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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

        home_page.open()
        home_page.close_ad_if_present()
        home_page.search_for_book("Кобзар")
        time.sleep(3)

        home_page.add_first_book_to_cart()
        assert home_page.get_cart_item_count() == 1, "Не вдалося додати товар перед видаленням"

        cart_page.open_cart()

        cart_page.remove_first_item()

        assert cart_page.is_cart_empty(), "Повідомлення про порожній кошик не знайдено! Товар міг не видалитися."

    def test_max_quantity_tc008(self):
        home_page = HomePage(self.driver)
        cart_page = CartPage(self.driver)

        home_page.open()
        home_page.close_ad_if_present()
        home_page.search_for_book("Кобзар")
        time.sleep(3)

        home_page.add_first_book_to_cart()

        cart_page.open_cart()

        attempted_amount = "999"
        actual_amount = cart_page.set_huge_quantity_and_get_actual(attempted_amount)

        print(f"\nСпробували додати {attempted_amount} шт. Сайт автоматично скинув до: {actual_amount} шт.")

        assert actual_amount != attempted_amount, f"БАГ! Система дозволила додати {attempted_amount} товарів!"
        assert int(actual_amount) > 0, "Після введення великого числа, кількість стала нульовою або мінусовою!"

    def test_full_cart_clearance_tc013(self):
        home_page = HomePage(self.driver)

        home_page.open()
        home_page.close_ad_if_present()

        home_page.add_first_book_to_cart()

        WebDriverWait(self.driver, 10).until(lambda d: home_page.get_header_cart_count() > 0)

        cart_icon = self.driver.find_element(By.CSS_SELECTOR, "button.ui-btn-shopping-cart")
        self.driver.execute_script("arguments[0].click();", cart_icon)
        time.sleep(1)

        home_page.click_clear_cart()
        home_page.confirm_cart_clearance()

        empty_text = home_page.get_empty_cart_text()

        assert "порожній" in empty_text.lower(), f"БАГ! Кошик не порожній. Текст: {empty_text}"
        assert home_page.get_header_cart_count() == 0, "БАГ! Лічильник на іконці кошика не обнулився!"

