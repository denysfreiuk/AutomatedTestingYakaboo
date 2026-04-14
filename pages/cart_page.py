import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):

    @property
    def cart_header_button(self):
        # Кнопка кошика в хедері для відкриття модалки
        return self.wait_for_element((By.CSS_SELECTOR, "button.ui-btn-shopping-cart"))

    @property
    def remove_item_button(self):
        # Кнопка "Видалити" біля товару
        return self.wait_for_element((By.CSS_SELECTOR, "span.product-action-remove"))

    @property
    def empty_cart_message(self):
        # Локатор для тексту "Кошик порожній" (або чогось подібного)
        # Я використовую XPath для пошуку по тексту, бо це найчастіше працює для таких повідомлень
        return self.wait_for_element((By.XPATH, "//*[contains(text(), 'порожн') or contains(text(), 'Немає товарів')]"))

    def open_cart(self):
        """Клікає на іконку кошика в хедері"""
        # Скролимо вгору, щоб кнопка кошика точно була видима
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        self.click_element((By.CSS_SELECTOR, "button.ui-btn-shopping-cart"))
        time.sleep(1)  # Чекаємо, поки модалка виїде

    def remove_first_item(self):
        """Натискає 'Видалити' для першого товару в кошику"""
        self.click_element((By.CSS_SELECTOR, "span.product-action-remove"))
        time.sleep(2)  # Чекаємо, поки товар зникне і оновиться DOM

    def is_cart_empty(self):
        """Перевіряє, чи з'явилося повідомлення про порожній кошик"""
        try:
            return self.empty_cart_message.is_displayed()
        except:
            return False