import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
from selenium.common.exceptions import StaleElementReferenceException

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
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)

        input_field = self.search_input
        self.driver.execute_script("arguments[0].click();", input_field)
        time.sleep(0.5)

        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.BACKSPACE)

        input_field.send_keys(keyword)
        time.sleep(2)

        search_btn = self.wait_for_element((By.CSS_SELECTOR, "div.ui-search-form-input button.ui-btn-primary"))

        self.driver.execute_script("arguments[0].click();", search_btn)

    def get_first_book_title_text(self):
        return self.first_book_title.text.strip()

    @property
    def first_book_add_to_cart_button(self):
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

    @property
    def first_book_author(self):
        return self.wait_for_element((By.CSS_SELECTOR, "div.ui-card-author"))

    def get_first_book_author_text(self):
        try:
            return self.first_book_author.text.strip()
        except:
            return ""

    @property
    def all_book_authors(self):
        self.wait_for_element((By.CSS_SELECTOR, "div.ui-card-author"))
        return self.driver.find_elements(By.CSS_SELECTOR, "div.ui-card-author")


    def get_all_book_authors_texts(self, retries=3):
        for i in range(retries):
            try:
                self.wait_for_element((By.CSS_SELECTOR, "div.ui-card-author"))

                elements = self.driver.find_elements(By.CSS_SELECTOR, "div.ui-card-author")

                return [el.text.strip() for el in elements if el.text.strip()]

            except StaleElementReferenceException:
                if i == retries - 1:
                    print("\nНе вдалося зібрати авторів після 3 спроб (DOM постійно оновлюється).")
                    return []
                time.sleep(1)
            except Exception as e:
                print(f"\nІнша помилка при зборі авторів: {e}")
                return []

    @property
    def catalog_button(self):
        return self.wait_for_element((By.CSS_SELECTOR, "button.ui-btn-book-categories"))

    def open_catalog_and_select_foreign_books(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        self.click_element((By.CSS_SELECTOR, "button.ui-btn-book-categories"))
        time.sleep(2)

        foreign_books_locator = (By.XPATH,
                                 "//div[contains(@class, 'books-list')]//a[contains(@href, 'vlasnij-import')]")

        elements = self.driver.find_elements(*foreign_books_locator)

        target_element = None
        for el in elements:
            if el.is_displayed():
                target_element = el
                break

        if not target_element and elements:
            target_element = elements[0]

        self.driver.execute_script("arguments[0].click();", target_element)

        time.sleep(4)

    def click_go_to_checkout(self):
        locator = (By.XPATH, "//button[contains(@class, 'ui-btn-accent') and contains(text(), 'Оформити замовлення')]")

        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def get_header_cart_count(self):
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By

            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.ui-btn-shopping-cart__counter"))
            )
            count_text = self.driver.execute_script("return arguments[0].textContent;", element).strip()
            return int(count_text) if count_text else 0
        except:
            return 0

