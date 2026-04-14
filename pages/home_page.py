import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage


class HomePage(BasePage):
    def open(self):
        self.driver.get("https://www.yakaboo.ua/")

    @property
    def search_input(self):
        return self.wait_for_element((By.ID, "search-input"))

    @property
    def search_button(self):
        return self.wait_for_element((By.CSS_SELECTOR, "button.ui-btn-primary"))

    @property
    def first_book_title(self):
        return self.wait_for_element((By.CSS_SELECTOR, "a.ui-card-title.category-card__name"))

    def close_ad_if_present(self):
        try:
            time.sleep(2)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
        except Exception as e:
            print(f"Попап не знайдено або помилка: {e}")

    def search_for_book(self, keyword):
        input_field = self.search_input
        self.driver.execute_script("arguments[0].click();", input_field)
        time.sleep(1)

        input_field.clear()
        input_field.send_keys(keyword)
        time.sleep(1)

        try:
            self.click_element((By.CSS_SELECTOR, "button.ui-btn-primary"))
        except:
            input_field.send_keys(Keys.ENTER)

    def get_first_book_title_text(self):
        return self.first_book_title.text.strip()

    @property
    def first_book_add_to_cart_button(self):
        # Локатор першої кнопки "Купити" з результатів (за data-testid)
        return self.wait_for_element((By.CSS_SELECTOR, "button[data-testid='addToCart']"))

    @property
    def cart_counter(self):
        return self.wait_for_element((By.CSS_SELECTOR, "span.ui-btn-shopping-cart__counter"))

    def add_first_book_to_cart(self):
        btn = self.first_book_add_to_cart_button
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(1)
        self.click_element((By.CSS_SELECTOR, "button[data-testid='addToCart']"))
        time.sleep(2)

    def get_cart_item_count(self):
        try:
            return int(self.cart_counter.text)
        except:

            return 0