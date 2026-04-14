import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException # Додали імпорт

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def wait_for_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_element(self, locator, retries=3):
        for i in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.5)
                fresh_element = self.driver.find_element(*locator)
                fresh_element.click()
                return
            except StaleElementReferenceException:
                if i == retries - 1:
                    raise
                time.sleep(1)
            except Exception:
                fresh_element = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].click();", fresh_element)
                return