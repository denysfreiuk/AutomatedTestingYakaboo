import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class CartPage(BasePage):

    @property
    def cart_header_button(self):
        return self.wait_for_element((By.CSS_SELECTOR, "button.ui-btn-shopping-cart"))

    @property
    def remove_item_button(self):
        return self.wait_for_element((By.CSS_SELECTOR, "span.product-action-remove"))

    @property
    def empty_cart_message(self):
        return self.wait_for_element((By.XPATH, "//*[contains(text(), 'порожн') or contains(text(), 'Немає товарів')]"))

    @property
    def quantity_input(self):
        return self.wait_for_element((By.CSS_SELECTOR, "div.product-quantity-input input"))

    def open_cart(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        self.click_element((By.CSS_SELECTOR, "button.ui-btn-shopping-cart"))
        time.sleep(1)

    def remove_first_item(self):
        self.click_element((By.CSS_SELECTOR, "span.product-action-remove"))
        time.sleep(2)

    def is_cart_empty(self):
        try:
            return self.empty_cart_message.is_displayed()
        except:
            return False

    def set_huge_quantity_and_get_actual(self, amount="999"):
        input_el = self.quantity_input
        self.driver.execute_script("arguments[0].click();", input_el)
        time.sleep(0.5)

        input_el.send_keys(Keys.CONTROL + "a")
        input_el.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)

        input_el.send_keys(amount)
        input_el.send_keys(Keys.ENTER)

        time.sleep(3)

        return input_el.get_attribute("value")